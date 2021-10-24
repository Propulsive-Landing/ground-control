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
