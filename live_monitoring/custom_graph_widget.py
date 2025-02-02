import pyqtgraph as pg
from time import time

#TODO. FIX FOR JSON DATA. Currently expecting binary data and therefore crashing.
class custom_graph_widget(pg.PlotWidget):
    def __init__(self, names: tuple, start=0):
        super().__init__()
        self.names = names

        self.graphed_values_num = 40

        self.start_time = start

        self.graph_lines = {} # name -> ([array of time], [array of data], graphitem)

    def setup_connection(self, current_frame):
        self.plotItem.addLegend()
        
        self.current_frame = current_frame
        for index, name in enumerate(self.names):
            self.graph_lines[name] = ([], [], self.plot([], [], pen=(index, len(self.names)), name=name))
        
        
    def update_lines(self):
        for name, graph_line in self.graph_lines.items():
            self.graph_lines[name][0].append(time()-self.start_time)
            print("CurrentFrame")
            print(self.current_frame)
            self.graph_lines[name][1].append(self.current_frame[name])

            self.graph_lines[name][2].setData(self.graph_lines[name][0][-self.graphed_values_num:], self.graph_lines[name][1][-self.graphed_values_num:])

    def show_history(self):
        for name, graph_line in self.graph_lines.items():
            self.graph_lines[name][2].setData(self.graph_lines[name][0], self.graph_lines[name][1])
