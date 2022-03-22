import sys
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets

from state_management_widget import state_management_widget
from file_management_widget import file_management_widget
from custom_graph_widget import custom_graph_widget
from custom_number_display import custom_number_display
from commanding_panel import commanding_pannel


#https://www.pythonguis.com/tutorials/plotting-pyqtgraph/



class GroundControlWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("AIAA PL Ground Control")
        self.layout = QtWidgets.QGridLayout(self)
        self._thread_pool = QtCore.QThreadPool.globalInstance()
        
        pg.setConfigOption('background', 'w')
        
        self.setup_number_displays()
        self.setup_graphs()
        self.init_widgets()

    def init_widgets(self):
        #File input
        self.file_management_panel = file_management_widget(self.output)
        self.layout.addWidget(self.file_management_panel, 1, 0)
        
        #Text view
        self.console = QtWidgets.QTextBrowser()
        self.layout.addWidget(self.console, 1, 1, 3, 1)

        #State management
        self.state_management_panel = state_management_widget(self.output, self.file_management_panel, self._thread_pool, self.graphs, self.numerical_displays)
        self.layout.addWidget(self.state_management_panel, 2, 0)

        #Communication output
        self.command_panel = commanding_pannel()
        self.layout.addWidget(self.command_panel, 1, 2, 3, 1)
        self.command_panel.command_signal.connect(self.state_management_panel.send_command)
    

    def setup_number_displays(self):
        self.numerical_displays = []
        self.numerical_displays.append(custom_number_display(1, "Mode:"))
        self.layout.addWidget(self.numerical_displays[0], 3, 0)

    def setup_graphs(self):
        self.graphs = []

        self.graphs.append(custom_graph_widget(indexes_in_struct=(2, 3, 4), names=('euler_x', 'euler_y', 'euler_z')))
        self.graphs.append(custom_graph_widget(indexes_in_struct=(6, 8, 11), names=('x[1]', 'x[3]', 'x[6]')))
        self.graphs.append(custom_graph_widget(indexes_in_struct=(9, 10, 12), names=('x[4]', 'x[5]', 'x[7]')))

        self.layout.addWidget(self.graphs[0], 0, 1)
        self.layout.addWidget(self.graphs[1], 0, 0)
        self.layout.addWidget(self.graphs[2], 0, 2)

    def output(self, text):
        self.console.append(text)

    def closeEvent(self, event):
        self.state_management_panel.stop_and_save()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = GroundControlWindow()
    window.resize(800, 600)
    window.show()
    

    sys.exit(app.exec())