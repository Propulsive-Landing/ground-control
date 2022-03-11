from PySide6 import QtCore, QtWidgets
from multiprocessing import Queue
from itertools import chain

class log_handler(QtCore.QRunnable):
    def __init__(self, path : str, output_function, log_queue: Queue):
        super().__init__()
        self.path = path
        self.output_function = output_function
        self.log_queue = log_queue

    def run(self):
        self.output_function('GUI: Start logging')
        with open(self.path, 'a') as file:
            while(True):
                message = self.log_queue.get()
                if(message == 'STOP'):
                    break
        
                print(str(message))
                file.write(str(message))
                file.write('\n')

                self.output_function("Received: " + str(message))

        self.output_function('GUI: End Logging, Saved')

class telem_frame_handler(QtCore.QRunnable):
    def __init__(self, path : str, output_function, frame_queue: Queue):
        super().__init__()
        self.path = path
        self.output_function = output_function
        self.frame_queue = frame_queue

    def run(self):
        self.output_function('GUI: Start data logging')
        with open(self.path, 'a') as file:
            while(True):
                message = self.frame_queue.get()
                if(message == 'STOP'):
                    break
        
                for x in message:
                    file.write(str(x) + ",")
                file.write('\n')

        self.output_function('GUI: End data logging, Saved')