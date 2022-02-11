import sys
from PySide6 import QtCore, QtWidgets

from state_management_widget import state_management_widget
from file_management_widget import file_management_widget
from custom_graph_widget import custom_graph_widget


#https://www.pythonguis.com/tutorials/plotting-pyqtgraph/



class GroundControlWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("AIAA PL Ground Control")
        self.layout = QtWidgets.QGridLayout(self)
        self._thread_pool = QtCore.QThreadPool.globalInstance()
        
        
        self.setup_graphs()
        self.init_widgets()

    def output(self, text):
        self.console_scroll_bar.setValue(self.console_scroll_bar.maximum())
        self.console.append(text)

    def closeEvent(self, event):
        self.state_management_panel.stop_and_save()

    def init_widgets(self):
        #File input
        self.file_management_panel = file_management_widget(self.output)
        self.layout.addWidget(self.file_management_panel, 1, 0)
        
        #Text view
        self.console = QtWidgets.QTextBrowser()
        self.console_scroll_bar = self.console.verticalScrollBar() 
        self.layout.addWidget(self.console, 1, 1, 4, 1)

        #Communication output
                
        def send_and_clear_command():
            self.state_management_panel.rf.input_transmitter.send(self.command.text())
            self.command.setText("")

        self.command = QtWidgets.QLineEdit()
        self.command.setPlaceholderText("Enter Command")
        self.layout.addWidget(self.command, 1, 2)

        self.send_command_button = QtWidgets.QPushButton("Send Command")
        self.layout.addWidget(self.send_command_button, 2, 2)
        self.send_command_button.clicked.connect(send_and_clear_command)

        #State management
        self.state_management_panel = state_management_widget(self.output, self.file_management_panel, self._thread_pool, self.graphs, transmitting_buttons=[self.send_command_button])
        self.layout.addWidget(self.state_management_panel, 2, 0, 2, 1)


    def setup_graphs(self):
        self.graphs = []

        self.graphs.append(custom_graph_widget((5, 6, 7), names=('euler_x', 'euler_y', 'euler_z')))
        self.graphs.append(custom_graph_widget((2, 3, 4), names=('velocity_x', 'velocity_y', 'velocity_z')))
        self.graphs.append(custom_graph_widget((11, 12), names=('current_u[x]', 'current_u[y]')))


        self.layout.addWidget(self.graphs[0], 0, 2)
        self.layout.addWidget(self.graphs[1], 0, 0)
        self.layout.addWidget(self.graphs[2], 0, 1)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = GroundControlWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())