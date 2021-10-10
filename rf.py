from data_packet import *
import serial


class RF():
    def __init__(self, port):
        self._comport = serial.Serial(port, 115200)

    def close(self):
        self._comport.close()

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
        packet.euler = (components[6], components[7], components[8])
        packet.y = (components[9], components[10],
                    components[11], components[12])
        packet.x = (components[13], components[14], components[15],
                    components[16], components[17], components[18])
        packet.dx = (components[19], components[20], components[21],
                     components[22], components[23], components[24])
        packet.yaw = components[25]
        packet.current_u = (components[26], components[27])
        packet.servo_u = (components[28], components[29])
        return packet

    def arm(self):
        self._comport.write(bytes('arm\n', 'utf8'))

    def abort(self):
        self._comport.write(bytes('abort\n', 'utf8'))

    def is_open(self):
        return self._comport.isOpen()
