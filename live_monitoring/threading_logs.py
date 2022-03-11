from PySide6 import QtCore, QtWidgets
from multiprocessing import Queue
from itertools import chain

class log_signals(QtCore.QObject):
    log_signal = QtCore.Signal(str)

class log_handler(QtCore.QRunnable):
    def __init__(self, path : str, log_queue: Queue):
        super().__init__()
        self.path = path
        self.log_queue = log_queue
        self.signals = log_signals()

    def run(self):
        self.signals.log_signal.emit('GUI: Start logging')
        with open(self.path, 'a') as file:
            while(True):
                message = self.log_queue.get()
                if(message == 'STOP'):
                    break
        
                print(str(message))
                file.write(str(message))
                file.write('\n')

                self.signals.log_signal.emit("Received: " + str(message))

        self.signals.log_signal.emit('GUI: End Logging, Saved')

class telem_signals(QtCore.QObject):
    telem_signal = QtCore.Signal(str)

class telem_frame_handler(QtCore.QRunnable):
    def __init__(self, path : str, frame_queue: Queue):
        super().__init__()
        self.path = path
        self.signals = telem_signals()
        self.frame_queue = frame_queue

    def run(self):
        self.signals.telem_signal.emit('GUI: Start data logging')
        with open(self.path, 'a') as file:
            while(True):
                message = self.frame_queue.get()
                if(message == 'STOP'):
                    break
        
                for x in message:
                    file.write(str(x) + ",")
                file.write('\n')

        self.signals.telem_signal.emit('GUI: End data logging, Saved')