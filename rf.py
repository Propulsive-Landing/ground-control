from data_packet import *
import serial
from struct import *


class RF():
    def __init__(self, port):
        self._comport = serial.Serial(port, 115200)
        self._bytes_received = []
        self._TELEM_HEADER =  [239, 190, 173, 222] #4 byte heaeder to indicate telem frame, 0xDEADBEEF
        self._STRING_HEADER = [206, 250, 186, 186] #4 byte header to indicate string data, 0xBABAFACE
        self._FOOTER = 3405707998 #4 byte uint to indicate ending of string or telem frame
        self._telem_struct = '=IhL4d4l26d19d20dI'
        self._sizeofstruct = calcsize(self._telem_struct)
        self._backlog_bytes_num = 600_000 #how many bytes to be in list for a backlog

    def close(self):
        self._comport.close()

    def handle_telem_received(self, telem_frame):
        print(telem_frame)

    def handle_string_received(self, str):
        print(str)

    def handle_telem_error(self, error_msg, frame):
        print(error_msg)
        print(frame)

    def handle_alignment_notice(self, bytes_skipped):
        print(str(bytes_skipped) + " required to align")

    #Should be called with high frequency to ensure propper readings
    def read_binary(self):
        if(self._comport.in_waiting >= 5): #waits until there is data of at least the size of the struct because if there is not that much data, there cannot be a complete struct
            
            received = self._comport.read(self._comport.in_waiting) #reads all available data from input buffer into bytearray
            self._bytes_received.extend(list(received)) #adds recieved data to a list
            
            if(len(self._bytes_received) > self._backlog_bytes_num):
                #Backlog condition
                self._bytes_received.clear()

            if(len(self._bytes_received) < 4):
                return
            if(self._bytes_received[0:4] != self._TELEM_HEADER and self._bytes_received[0:4] != self._STRING_HEADER): #if the first four bytes received do not match the struct magic number, then alignment must be done
                print(self._bytes_received)
                
                iterations = 0
                while(len(self._bytes_received) >=4 and (self._bytes_received[0:4] != self._TELEM_HEADER and self._bytes_received[0:4] != self._STRING_HEADER)): #removes from the front of the struct until a head is found
                    self._bytes_received.pop(0)
                    iterations += 1
                self.handle_alignment_notice(iterations)

            if(len(self._bytes_received) < 4):
                return

            if((self._bytes_received[0:4] == self._TELEM_HEADER and len(self._bytes_received) >= self._sizeofstruct)): #When there is a valid header and enough bytes are in the list, data is then read.
                res = bytearray(self._bytes_received[0:self._sizeofstruct])
                del self._bytes_received[0:self._sizeofstruct]
                frame = unpack(self._telem_struct, res)
                
                
                if(frame[-1:][0] != self._FOOTER):
                    self.handle_telem_error("invalid frame", frame)
                else:
                    self.handle_telem_received(frame)
                    

            if(self._bytes_received[0:4] == self._STRING_HEADER and len(self._bytes_received) >= 5):
                byte_after_header = bytearray(self._bytes_received[4:5]) #first four bytes are header, 5th byte is size
                length = unpack('=B', byte_after_header)[0]

                if(len(self._bytes_received[5:]) >= length + 4):
                    incomingString = bytearray(self._bytes_received[5:5+length+4]) #length of footer is 4
                    del self._bytes_received[0:5+length+4]
                    string_with_struct = '=' + str(length) + 'cI'
                    parsedString = unpack(string_with_struct, incomingString)
                    
                    if(parsedString[-1:][0] != self._FOOTER):
                        self.handle_string_error("Invalid String, no footer", parsedString)
                    else:
                        try:
                            byte_chars = [s.decode() for s in parsedString[:-1]]
                            output_string = "".join(byte_chars)
                            self.handle_string_received(output_string)
                        except:
                            self.handle_string_error("Character value exceeds ascii values", parsedString)

    def read(self):
        line = self._comport.readline()
        components = line.split(',')
        if len(components) != 30:
            raise RuntimeError()

        packet = DataPacket()
        packet.mode = components[0]
        packet.loop_number = components[1]
        packet.current_time = components[2]
        packet.dt = components[3]
        packet.voltage_a = components[4]
        packet.voltage_b = components[5]
        packet.dt_telem = components[6]
        packet.dt_observer = components[7]
        packet.dt_controller = components[8]
        packet.dt_change_mode = components[9]
        packet.euler_raw = (components[10], components[11], components[12])
        packet.quaternion_raw = (components[13], components[14], components[15], components[16])
        packet.acc_raw = (components[17], components[18], components[19])
        packet.gyro_raw = (components[20], components[21], components[22])
        packet.cbn = (components[23], components[24], components[25],
                      components[26], components[27], components[28], 
                      components[29], components[30], components[31])
        packet.euler = (components[32], components[33], components[34])
        packet.quaternion = (components[35], components[36], components[37], components[38])
        packet.velocity = (components[39], components[40], components[41])
        packet.y = (components[42], components[43],
                    components[44], components[45])
        packet.x = (components[46], components[47], components[48],
                    components[49], components[50], components[51])
        packet.dx = (components[52], components[53], components[54],
                     components[55], components[56], components[57])
        packet.current_u = (components[58], components[59])
        packet.servo_u = (components[60], components[61])
        return packet

    def arm(self):
        self._comport.write(bytes('arm\n', 'utf8'))

    def abort(self):
        self._comport.write(bytes('abort\n', 'utf8'))

    def is_open(self):
        return self._comport.isOpen()
