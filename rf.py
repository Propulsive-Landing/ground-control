from multiprocessing import Process, Queue

from data_packet import *
import serial
import tkinter as tk
from struct import *





class RF():
    def __init__(self, port, baud, backlog_threshold = 6000, telem_string='=IhL4d4l26d19d20dI'):
        self._comport = serial.Serial(port, baud)
        self._backlog_bytes_num = backlog_threshold #how many bytes to be in list for a backlog

        self._bytes_received = [] #This list holds recieved bytes and this list is searched through to find packets
        self._history = []
        self._TELEM_HEADER =  [239, 190, 173, 222] #4 byte heaeder to indicate telem frame, 0xDEADBEEF
        self._STRING_HEADER = [206, 250, 186, 186] #4 byte header to indicate string data, 0xBABAFACE
        self._FOOTER = 3405707998 #4 byte uint32_t to indicate ending of string or telem frame // 202, 254, 250, 222

        self._telem_struct = telem_string
        self._sizeofstruct = calcsize(self._telem_struct)

        self._comport.reset_input_buffer()


        self.telem_frame_queue = Queue()
        self.log_queue = Queue()

    def close(self):
        self._comport.close()

    def handle_string_received(self, str):
        self.log_queue.put(str)

    def handle_string_error(self, str):
        self.log_queue.put(str)

    def handle_telem_error(self, error_msg, frame):
        self.log_queue.put(error_msg)
        self.log_queue.put(frame)

    def handle_alignment_notice(self, bytes_skipped):
        self.log_queue.put(str(bytes_skipped) + " required to align")


    #Should be called with high frequency to ensure propper readings
    def read_binary(self):
        if(self._comport.in_waiting >= 5): #waits until there is data of at least the size of the struct because if there is not that much data, there cannot be a complete struct
            
            received = self._comport.read(self._comport.in_waiting) #reads all available data from input buffer into bytearray
            self._bytes_received.extend(list(received)) #adds recieved data to a list
            self._history.extend(list(received))
            
            #print(self._bytes_received)

            if(len(self._bytes_received) > self._backlog_bytes_num):
                #Backlog condition
                self._bytes_received.clear()
                self.log_queue.put("backlog")

            if(len(self._bytes_received) < 10):
                return
            if(self._bytes_received[0:4] != self._TELEM_HEADER and self._bytes_received[0:4] != self._STRING_HEADER): #if the first four bytes received do not match the struct magic number, then alignment must be done
                stra = f'aligned: {self._bytes_received} '
                
                iterations = 0
                while(len(self._bytes_received) >= 4 and (self._bytes_received[0:4] != self._TELEM_HEADER and self._bytes_received[0:4] != self._STRING_HEADER)): #removes from the front of the struct until a head is found
                    self._bytes_received.pop(0)
                    iterations += 1
                stra += f'{iterations} byes'
                self.log_queue.put(stra)

            if(len(self._bytes_received) < 4):
                return

            if((self._bytes_received[0:4] == self._TELEM_HEADER and len(self._bytes_received) >= self._sizeofstruct)): #When there is a valid header and enough bytes are in the list, data is then read.
                res = bytearray(self._bytes_received[0:self._sizeofstruct])
                del self._bytes_received[0:self._sizeofstruct]
                frame = unpack(self._telem_struct, res)
                
                
                if(frame[-1:][0] != self._FOOTER):
                    self.handle_telem_error("invalid frame", frame)
                else:
                    self.telem_frame_queue.put(frame)
                    

            if(self._bytes_received[0:4] == self._STRING_HEADER and len(self._bytes_received) >= 9):
                byte_after_header = bytearray(self._bytes_received[4:5]) #first four bytes are header, 5th byte is size
                length = unpack('=B', byte_after_header)[0]

                if(len(self._bytes_received[5:]) >= length + 5):
                    incomingString = bytearray(self._bytes_received[5:5+length+4]) #length of footer is 4
                    del self._bytes_received[0:5+length+4]
                    string_with_struct = '=' + str(length) + 'cI'
                    parsedString = unpack(string_with_struct, incomingString)
                    
                    if(parsedString[-1:][0] != self._FOOTER):
                        self.handle_string_error("Invalid String, no footer" + str(parsedString))
                    else:
                        try:
                            byte_chars = [s.decode() for s in parsedString[:-1]]
                            output_string = "".join(byte_chars)
                            self.handle_string_received(output_string)
                        except:
                            self.handle_string_error("Character value exceeds ascii values" + str(parsedString))


    def arm(self):
        self._comport.write(bytes('arm\n', 'utf8'))

    def abort(self):
        self._comport.write(bytes('abort\n', 'utf8'))

    def is_open(self):
        return self._comport.isOpen()