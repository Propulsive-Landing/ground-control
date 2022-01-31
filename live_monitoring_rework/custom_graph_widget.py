from PySide6 import QtCore, QtWidgets
import pyqtgraph as pg
from multiprocessing import Array

class custom_graph_widget(pg.PlotWidget):
    def __init__(self, indexes: tuple):
        super().__init__()
        self.indexes = indexes

        self.values = {}

    def setup_connection(self, current_frame):
        self.current_frame = current_frame
        for index in self.indexes:
            self.values[index] = ([0], [0], self.plot([0], [0]))
        
    def update_lines(self):
        for index in self.indexes:
            self.values[index][0].append(self.values[index][0][-1]+1)
            self.values[index][1].append(self.current_frame[index])

            self.values[index][2].setData(self.values[index][0][-20:], self.values[index][1][-20:])

    def show_history(self):
        for index in self.indexes:
            self.values[index][2].setData(self.values[index][0], self.values[index][1])
