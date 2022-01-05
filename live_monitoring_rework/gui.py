import sys
from PySide6 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg
import numpy as np
from multiprocessing import Value, Array, Queue

from rf import RF

#https://www.pythonguis.com/tutorials/plotting-pyqtgraph/

class MyWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self._data = { 'current_frame': Array('d', 7), 'log_queue' : Queue(), 'frame_queue': Queue()}
        self.looping_for_data = Value('i', 1)

        RF.listen_on_rf('COM11', 9600, self.looping_for_data, self._data['current_frame'], self._data['frame_queue'], self._data['log_queue'], backlog_threshold = 6000, telem_string='=IiffffI')



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())