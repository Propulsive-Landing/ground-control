from multiprocessing import Queue, Value, Process, Pipe
from time import sleep
import json

import serial
from struct import *


class RF():
    def __init__(self, port : str, baud : int, current_value, telem_frame_queue, log_queue, handled_most_recent : Value):

        self.port = port
        self.baud = baud

        self._delay_between_packets = .05 #Delay (in s) if there is not enough data in input buffer to be read into something meaningful



        self.input_receiver, self.input_transmitter = Pipe()

        self.handled_most_recent = handled_most_recent

        self._current_telem_frame = current_value
        self._telem_frame_queue = telem_frame_queue
        self._log_queue = log_queue

    def connect_serial(self, port: str, baud: int) -> bool:
        try:
            self._comport = serial.Serial(port, baud, timeout=0.2)
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
                self._comport.write(bytes((val).encode('ascii', 'replace')))
            self.read_json()
        
        self._comport.close()

    #Starts a separate process that will connect serial port then listen for data
    def start_listen_loop(self, running: Value):
        self.process = Process(target=self._listen_loop, args=(running,), name="Data Search Loop")
        self.process.start()


    #Should be called with high frequency to ensure propper readings
    def read_json(self):
        if(self._comport.in_waiting < 1):
            sleep(self._delay_between_packets)
            return

        
        received = self._comport.readline() #reads all available data from input buffer into bytearray
        
        try:
            data = json.loads(received)
            print(data)

            if(data["data_type"] == "string"):
                self._log_queue.put(data["payload"])
            elif(data["data_type"] == "telem"):
                self._telem_frame_queue.put(data["payload"])
                self._current_telem_frame.update(data["payload"])
                self.handled_most_recent.value = 0
        except Exception as e:
            print(e)
        
