import sys
from PySide6 import QtCore, QtWidgets
import pyqtgraph as pg
import struct
from multiprocessing import Value, Array, Queue
from recordclass import recordclass

from threading_logs import telem_frame_handler, log_handler
from rf import RF
from file_management_widget import file_management_widget

#https://www.pythonguis.com/tutorials/plotting-pyqtgraph/


class GroundControlWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("AIAA PL Ground Control")

        self.layout = QtWidgets.QGridLayout(self)

        telem_frame_string = '=IiffffI'
        telem_attribute_num = len(struct.unpack(telem_frame_string,bytearray(struct.calcsize(telem_frame_string)*[0])))

        self._data = {
            'current_frame': Array('d', telem_attribute_num), #Most recent data frame received
            'log_queue' : Queue(), #queue of all logs
            'frame_queue': Queue() #queue of all data frames received
        }
        self.looping_for_data = Value('i', 1) #Controls whether the listenig process is running.

        self.rf = RF(self._data['current_frame'], self._data['frame_queue'], self._data['log_queue'], backlog_threshold = 6000, telem_string='=IiffffI')
        self.graph_widget_data = recordclass('Graph_Widget', 'item_num widget x y line')

        self._thread_pool = QtCore.QThreadPool.globalInstance()
        self.log_path = 'a'
        self.data_path = 'b'

        self.init_widgets()

    def output(self, text):
        self.console.append(text)

    def closeEvent(self, event):
        self.stop_and_save()

    def init_widgets(self):
        # Setup Euler_X graph
        self.euler_x = self._initialize_graph_data(20)
        self.layout.addWidget(self.euler_x.widget, 0, 0)

        # Setup Euler_Y graph
        self.euler_y = self._initialize_graph_data(20)
        self.layout.addWidget(self.euler_y.widget, 0, 1)

        #File input

        self.file_management_panel = file_management_widget(self.output)
        self.layout.addWidget(self.file_management_panel, 1, 0)

        #port input
        self.port_input = QtWidgets.QLineEdit()
        self.port_input.setPlaceholderText("Enter Port")
        self.layout.addWidget(self.port_input, 2, 0)

        #connect button
        self.connect_serial_button = QtWidgets.QPushButton("Connect Serial and Listen")
        self.layout.addWidget(self.connect_serial_button, 3, 0)
        self.connect_serial_button.clicked.connect(self.connect_and_listen)

        #stop and save button
        self.stop_listening_and_save_button = QtWidgets.QPushButton("Stop Listening and Save")
        self.layout.addWidget(self.stop_listening_and_save_button, 4, 0)
        self.stop_listening_and_save_button.clicked.connect(self.stop_and_save)
        self.stop_listening_and_save_button.setEnabled(False)

        #Text view
        self.console = QtWidgets.QTextBrowser()
        self.layout.addWidget(self.console, 1, 1, 4, 1)

        self._start_animation_timer()

    def connect_and_listen(self):
        if(not self.rf.connect_serial(self.port_input.text(), 9600)):
            self.output("Invalid Serial Port")
            return

        self.looping_for_data.value = 1
        self.rf.start_listen_loop()

        self._thread_pool.start(log_handler(self.log_path, self.console, self._data['log_queue']))
        self._thread_pool.start(telem_frame_handler(self.data_path, self.console, self._data['frame_queue']))
        self.stop_listening_and_save_button.setEnabled(True)
    
    def stop_and_save(self):
        self._data['log_queue'].put('STOP')
        self._data['frame_queue'].put('STOP')
        self.looping_for_data.value = 0

    
    def _update_plot_data(self):
        self.euler_x.y = self.euler_x.y[1:]
        self.euler_x.y.append(self._data['current_frame'][2])
        self.euler_x.line.setData(self.euler_x.x, self.euler_x.y)

    def _start_animation_timer(self):
        self.animation_timer = QtCore.QTimer()
        self.animation_timer.setInterval(100)
        self.animation_timer.timeout.connect(self._update_plot_data)
        self.animation_timer.start()

    def _initialize_graph_data(self, item_num):
        data = self.graph_widget_data(item_num=item_num, widget=pg.PlotWidget(), x=None, y=None, line=None)
        data.x = list(range(0,item_num))
        data.y = [0]*item_num
        data.line = data.widget.plot(data.x, data.y)
        return data


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = GroundControlWindow()
    window.resize(800, 300)
    window.show()

    sys.exit(app.exec())