import sys
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets
from threading import Lock

from state_management_widget import state_management_widget
from file_management_widget import file_management_widget
from custom_graph_widget import custom_graph_widget
from custom_number_display import custom_number_display


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

    
    def output(self, text):
        self.console.append(text)


        

    def closeEvent(self, event):
        self.state_management_panel.stop_and_save()

    def init_widgets(self):
        #File input
        self.file_management_panel = file_management_widget(self.output)
        self.layout.addWidget(self.file_management_panel, 1, 0)
        
        #Text view
        self.console = QtWidgets.QTextBrowser()
        self.console_lock = Lock()
        self.layout.addWidget(self.console, 1, 1, 3, 1)

        #Communication output
                
        def send_command(command: str):
            try:
                self.state_management_panel.rf.input_transmitter.send(command)
            except AttributeError:
                self.output("Serial not Connected")

        def send_and_clear_command():
            send_command(self.command.text())
            self.command.setText("")

        self.command = QtWidgets.QLineEdit()
        self.command.setPlaceholderText("Enter Command")
        self.layout.addWidget(self.command, 1, 2)

        self.send_command_button = QtWidgets.QPushButton("Send Command")
        self.layout.addWidget(self.send_command_button, 2, 2)
        self.send_command_button.clicked.connect(send_and_clear_command)
        
        #Output Buttons
        abort_button= QtWidgets.QPushButton("ABORT")
        abort_button.setStyleSheet("background: red; color: white; font-size: 13px;")
        self.layout.addWidget(abort_button, 4, 2)

        countdown_button = QtWidgets.QPushButton("GO FOR COUNTDOWN")
        countdown_button.setStyleSheet("background: lime; font-size: 13px;")
        self.layout.addWidget(countdown_button, 3, 2)

        countdown_button.clicked.connect(lambda: send_command("COMMAND: set_mode 1"))
        abort_button.clicked.connect(lambda : send_command("COMMAND: ABORT"))

        #State management
        self.state_management_panel = state_management_widget(self.output, self.file_management_panel, self._thread_pool, self.graphs, self.numerical_displays, transmitting_buttons=[self.send_command_button])
        self.layout.addWidget(self.state_management_panel, 2, 0, 2, 1)

    def setup_number_displays(self):
        self.numerical_displays = []
        self.numerical_displays.append(custom_number_display(1, "Mode"))
        self.layout.addWidget(self.numerical_displays[0], 4, 1)

    def setup_graphs(self):
        self.graphs = []

        self.graphs.append(custom_graph_widget((2, 3, 4), names=('euler_x', 'euler_y', 'euler_z')))
        self.graphs.append(custom_graph_widget((6, 8, 11), names=('x[1]', 'x[3]', 'x[6]')))
        self.graphs.append(custom_graph_widget((9, 10, 12), names=('x[4]', 'x[5]', 'x[7]')))

        self.layout.addWidget(self.graphs[0], 0, 1)
        self.layout.addWidget(self.graphs[1], 0, 0)
        self.layout.addWidget(self.graphs[2], 0, 2)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = GroundControlWindow()
    window.resize(800, 600)
    window.show()
    

    sys.exit(app.exec())