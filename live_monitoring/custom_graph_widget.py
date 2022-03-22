import pyqtgraph as pg

class custom_graph_widget(pg.PlotWidget):
    def __init__(self, indexes_in_struct: tuple, names: tuple):
        super().__init__()
        self.indexes = indexes_in_struct
        self.names = names

        self.graphed_values_num = 100

        self.values = {}

    def setup_connection(self, current_frame):
        self.plotItem.addLegend()
        
        self.current_frame = current_frame
        for count, index in enumerate(self.indexes):
            self.values[index] = ([0], [0], self.plot([0], [0], pen=(count, len(self.indexes)), name=self.names[count]))
        
        
    def update_lines(self):
        for index in self.indexes:
            self.values[index][0].append(self.values[index][0][-1]+1)
            self.values[index][1].append(self.current_frame[index])

            self.values[index][2].setData(self.values[index][0][-self.graphed_values_num:], self.values[index][1][-self.graphed_values_num:])

    def show_history(self):
        for index in self.indexes:
            self.values[index][2].setData(self.values[index][0], self.values[index][1])
