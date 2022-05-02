import pyqtgraph as pg
from time import time

class custom_graph_widget(pg.PlotWidget):
    def __init__(self, indexes_in_struct: tuple, names: tuple, start=0):
        super().__init__()
        self.indexes = indexes_in_struct
        self.names = names

        self.graphed_values_num = 40

        self.start_time = start

        self.values = {}

    def setup_connection(self, current_frame):
        self.plotItem.addLegend()
        
        self.current_frame = current_frame
        for count, index in enumerate(self.indexes):
            self.values[index] = ([], [], self.plot([], [], pen=(count, len(self.indexes)), name=self.names[count]))
        
        
    def update_lines(self):
        for index in self.indexes:
            self.values[index][0].append(time()-self.start_time)
            self.values[index][1].append(self.current_frame[index])

            self.values[index][2].setData(self.values[index][0][-self.graphed_values_num:], self.values[index][1][-self.graphed_values_num:])

    def show_history(self):
        for index in self.indexes:
            self.values[index][2].setData(self.values[index][0], self.values[index][1])
