import os
from data_packet import *


class Log():
    def __init__(self):
        if not os.path.isdir('./logs/'):
            os.mkdir('./logs/')
        self._number = 1
        self._path = './logs/log_' + str(self._number) + '.csv'
        while os.path.isfile(self._path) or os.path.isfile(self._path):
            self._number += 1
            self._path = './logs/log_' + str(self._number) + '.csv'
        self._file = open(self._path, 'w')

        line = ''
        packet = DataPacket()
        for member in dir(packet):
            length = 0
            if member.startswith('_') or callable(getattr(packet, member)):
                continue
            elif type(getattr(packet, member)) == tuple or type(getattr(packet, member)) == list:
                length = len(getattr(packet, member))
            if length == 0:
                line += str(member) + ','
            else:
                line += str(member) + ',' * length
        line = line.removesuffix(',')
        line += '\n'
        self._file.write(line)

    def close(self):
        self._file.close()

    def log(self, packet):
        line = ''
        for member in dir(packet):
            if member.startswith('_') or callable(getattr(packet, member)):
                continue
            elif type(getattr(packet, member)) == tuple or type(getattr(packet, member)) == list:
                for x in getattr(packet, member):
                    line += str(x) + ','
            else:
                line += str(getattr(packet, member)) + ','
        line = line.removesuffix(',')
        line += '\n'
        self._file.write(line)
