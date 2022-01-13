import sys
from PySide6 import QtCore, QtWidgets
import pyqtgraph as pg
import struct
from multiprocessing import Value, Array, Queue

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

        self.rf = RF(self._data['current_frame'], self._data['frame_queue'], self._data['log_queue'])

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

        if(not self.rf.connect_serial(self.port_input.text(), 9600)):
            self.output("Invalid Serial Port")
            return

        self.data_path, self.log_path = self.file_management_panel.create_files()
        self.rf._telem_struct_unpacking_values['telem_struct_string'] = self.file_management_panel.struct_string

        self.looping_for_data.value = 1
        self.rf.start_listen_loop()

        self._thread_pool.start(log_handler(self.log_path, self.console, self._data['log_queue']))
        self._thread_pool.start(telem_frame_handler(self.data_path, self.console, self._data['frame_queue']))
        self.stop_listening_and_save_button.setEnabled(True)
    
    def stop_and_save(self):
        self._data['log_queue'].put('STOP')
        self._data['frame_queue'].put('STOP')
        self.looping_for_data.value = 0

    def setup_graphs(self):
        pass
    
    def _update_plot_data(self):
        pass

    def _start_animation_timer(self):
        self.animation_timer = QtCore.QTimer()
        self.animation_timer.setInterval(100)
        self.animation_timer.timeout.connect(self._update_plot_data)
        self.animation_timer.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = GroundControlWindow()
    window.resize(800, 300)
    window.show()

    sys.exit(app.exec())