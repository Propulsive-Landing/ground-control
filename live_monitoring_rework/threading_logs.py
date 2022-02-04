from PySide6 import QtCore, QtWidgets
from multiprocessing import Queue
from itertools import chain

class log_handler(QtCore.QRunnable):
    def __init__(self, path : str, text_box : QtWidgets.QTextBrowser, log_queue: Queue):
        super().__init__()
        self.path = path
        self.text_box = text_box
        self.log_queue = log_queue

    def run(self):
        self.text_box.append('Start logging')
        with open(self.path, 'a') as file:
            while(True):
                message = self.log_queue.get()
                if(message == 'STOP'):
                    break
        
                file.write(str(message))

                self.text_box.append(str(message))

        self.text_box.append('End Logging, Saved')

class telem_frame_handler(QtCore.QRunnable):
    def __init__(self, path : str, text_box : QtWidgets.QTextBrowser, frame_queue: Queue):
        super().__init__()
        self.path = path
        self.text_box = text_box
        self.frame_queue = frame_queue

    def run(self):
        self.text_box.append('Start data logging')
        with open(self.path, 'a') as file:
            while(True):
                message = self.frame_queue.get()
                if(message == 'STOP'):
                    break
        
                for x in message:
                    file.write(str(x) + ",")
                file.write('\n')

        self.text_box.append('End data logging, Saved')