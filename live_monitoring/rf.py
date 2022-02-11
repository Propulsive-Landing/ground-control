from multiprocessing import Queue, Array, Value, Process, Pipe
from time import sleep

import serial
from struct import *


class RF():
    def __init__(self, port : str, baud : int, current_value: Array, telem_frame_queue: Queue, log_queue: Queue, handled_most_recent : Value, backlog_threshold = 6000, telem_string='=IiffffI'):

        self.port = port
        self.baud = baud

        self._bytes_received = [] #This list holds recieved bytes and this list is searched through to find packets
        self._history = []

        self._delay_between_packets = 5 #Delay (in ms) if there is not enough data in input buffer to be read into something meaningful

        self._transmittion_constants = {
            'TELEM_HEADER': [239, 190, 173, 222], #4 byte heaeder to indicate start of telem frame, 0xDEADBEEF
            'STRING_HEADER': [206, 250, 186, 186], #4 byte header to indicate start of string data, 0xBABAFACE
            'FOOTER': 3405707998, #4 byte value to indicate ending of string or telem frame 0xCAFEFADE
            'backlog_threshold' : backlog_threshold #how many bytes to be in list for a backlog
        }

        self._telem_struct_unpacking_values = {
            'telem_struct_string': telem_string,
            'size_of_telem_struct': calcsize(telem_string)
        }

        self.input_receiver, self.input_transmitter = Pipe()

        self.handled_most_recent = handled_most_recent

        self._current_telem_frame = current_value
        self._telem_frame_queue = telem_frame_queue
        self._log_queue = log_queue

    def connect_serial(self, port: str, baud: int) -> bool:
        try:
            self._comport = serial.Serial(port, baud)
            self._comport.reset_input_buffer()
            return True
        except serial.SerialException:
            return False

    def disconnect_serial(self):
        try:
            self._comport.close()
            return True
        except ValueError:
            return False


    def _listen_loop(self, running: Value):
        self._comport = serial.Serial(self.port, self.baud)
        self._comport.reset_input_buffer()

        while(running.value == 1):
            if(self.input_receiver.poll()):
                val = self.input_receiver.recv()
                self._comport.write(bytes(val.encode('ascii', 'replace')))
            self.read_binary()
        
        self._comport.close()

    #Starts a separate process that will connect serial port then listen for data
    def start_listen_loop(self, running: Value):
        process = Process(target=self._listen_loop, args=(running,), name="Data Search Loop")
        process.start()

    def handle_alignment_notice(self, bytes_skipped):
        self._log_queue.put(str(bytes_skipped) + " required to align")


    #Should be called with high frequency to ensure propper readings
    def read_binary(self):
        if(self._comport.in_waiting < 5):
            sleep(.005)
        else: #waits until there is data of at least the size of the struct because if there is not that much data, there cannot be a complete struct
            
            received = self._comport.read(self._comport.in_waiting) #reads all available data from input buffer into bytearray
            self._bytes_received.extend(list(received)) #adds recieved data to a list
            self._history.extend(list(received))
            
            #print(self._bytes_received)

            if(len(self._bytes_received) > self._transmittion_constants['backlog_threshold']):
                #Backlog condition
                self._bytes_received.clear()
                self._log_queue.put("backlog")

            if(len(self._bytes_received) < 10):
                return
            if(self._bytes_received[0:4] != self._transmittion_constants['TELEM_HEADER'] and self._bytes_received[0:4] != self._transmittion_constants['STRING_HEADER']): #if the first four bytes received do not match the struct magic number, then alignment must be done
                stra = f'aligned: {self._bytes_received} '
                
                iterations = 0
                while(len(self._bytes_received) >= 4 and (self._bytes_received[0:4] != self._transmittion_constants['TELEM_HEADER'] and self._bytes_received[0:4] != self._transmittion_constants['STRING_HEADER'])): #removes from the front of the struct until a head is found
                    self._bytes_received.pop(0)
                    iterations += 1
                stra += f'{iterations} bytes'
                self._log_queue.put(stra)

            if(len(self._bytes_received) < 4):
                return

            if((self._bytes_received[0:4] == self._transmittion_constants['TELEM_HEADER'] and len(self._bytes_received) >= self._telem_struct_unpacking_values['size_of_telem_struct'])): #When there is a valid header and enough bytes are in the list, data is then read.
                res = bytearray(self._bytes_received[0:self._telem_struct_unpacking_values['size_of_telem_struct']])
                del self._bytes_received[0:self._telem_struct_unpacking_values['size_of_telem_struct']]
                frame = unpack(self._telem_struct_unpacking_values['telem_struct_string'], res)
                
                
                if(frame[-1:][0] != self._transmittion_constants['FOOTER']):
                    self._log_queue.put("invalid frame")
                else:
                    self._telem_frame_queue.put(frame)
                    self._current_telem_frame[:] = frame
                    self.handled_most_recent.value = 0
                    

            if(self._bytes_received[0:4] == self._transmittion_constants['STRING_HEADER'] and len(self._bytes_received) >= 9):
                byte_after_header = bytearray(self._bytes_received[4:5]) #first four bytes are header, 5th byte is size
                length = unpack('=B', byte_after_header)[0]

                if(len(self._bytes_received[5:]) >= length + 5):
                    incomingString = bytearray(self._bytes_received[5:5+length+4]) #length of footer is 4
                    del self._bytes_received[0:5+length+4]
                    string_with_struct = '=' + str(length) + 'cI'
                    parsedString = unpack(string_with_struct, incomingString)
                    
                    if(parsedString[-1:][0] != self._transmittion_constants['FOOTER']):
                        self._log_queue.put("Invalid String, no footer" + str(parsedString))
                    else:
                        try:
                            byte_chars = [s.decode() for s in parsedString[:-1]]
                            output_string = "".join(byte_chars)
                            self._log_queue.put(output_string)
                        except:
                            self._log_queue.put("Character value exceeds ascii values" + str(parsedString))
