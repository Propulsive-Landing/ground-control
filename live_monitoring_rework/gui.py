import multiprocessing
import random
import sys
from PySide6 import QtCore, QtWidgets
import pyqtgraph as pg
import struct
from multiprocessing import Value, Array, Queue

import gui_util
from threading_logs import telem_frame_handler, log_handler
from rf import RF
from file_management_widget import file_management_widget
from custom_graph_widget import custom_graph_widget


#https://www.pythonguis.com/tutorials/plotting-pyqtgraph/



class GroundControlWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("AIAA PL Ground Control")
        self.layout = QtWidgets.QGridLayout(self)
        self._thread_pool = QtCore.QThreadPool.globalInstance()
        self.init_widgets()
        self.setup_graphs()

    def output(self, text):
        self.console.append(text)

    def closeEvent(self, event):
        self.stop_and_save()

    def init_widgets(self):
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



    def connect_and_listen(self):
        if(not self.file_management_panel.check_ready()):
            return

        if(not gui_util.serial_port_available(self.port_input.text())):
            self.output("Invalid Serial Port")
            return
        
        self.initialize_rf(self.port_input.text(), 9600)
            
        self._start_animation_timer()
            
        self.data_path, self.log_path = self.file_management_panel.create_files()
        self.rf._telem_struct_unpacking_values['telem_struct_string'] = self.file_management_panel.struct_string

        self.looping_for_data.value = 1
        self.rf.start_listen_loop(self.looping_for_data)

        self._thread_pool.start(log_handler(self.log_path, self.console, self._data['log_queue']))
        self._thread_pool.start(telem_frame_handler(self.data_path, self.console, self._data['frame_queue']))
        self.stop_listening_and_save_button.setEnabled(True)
    
    #does not connect the port, just passses the info to the RF class so it can be used later
    def initialize_rf(self, port : str, baud : int):
        telem_frame_string = self.file_management_panel.struct_string
        telem_attribute_num = len(struct.unpack(telem_frame_string,bytearray(struct.calcsize(telem_frame_string)*[0])))

        self._data = {
            'current_frame': Array('d', telem_attribute_num), #Most recent data frame received
            'log_queue' : Queue(), #queue of all logs
            'frame_queue': Queue() #queue of all data frames received
        }
        self.looping_for_data = Value('i', 1) #Controls whether the listenig process is running.

        self.rf = RF(port, baud, self._data['current_frame'], self._data['frame_queue'], self._data['log_queue'])

        self.eulers.setup_connection(self._data['current_frame'])
        self.velocities.setup_connection(self._data['current_frame'])

    def stop_and_save(self):
        self._data['log_queue'].put('STOP')
        self._data['frame_queue'].put('STOP')
        self.looping_for_data.value = 0

        self.stop_listening_and_save_button.setEnabled(False)
        self.eulers.show_history()
        self.velocities.show_history()

        self.animation_timer.stop()

    def setup_graphs(self):
        self.eulers = custom_graph_widget((5, 6, 7))
        self.velocities = custom_graph_widget((2, 3, 4))

        self.layout.addWidget(self.eulers, 0, 0)
        self.layout.addWidget(self.velocities, 0, 1)
        
    
    def _update_plot_data(self):
        self.eulers.update_lines()
        self.velocities.update_lines()

    def _start_animation_timer(self):
        self.animation_timer = QtCore.QTimer()
        self.animation_timer.setInterval(100)
        self.animation_timer.timeout.connect(self._update_plot_data)
        self.animation_timer.start()
        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = GroundControlWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())