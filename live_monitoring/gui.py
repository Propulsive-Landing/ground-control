from cmath import pi
import multiprocessing
import random
import sys
from PySide6 import QtCore, QtWidgets
import pyqtgraph as pg
import pyqtgraph.exporters
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

        #Reset and Save Graphs
        self.reset_and_save_graphs_button = QtWidgets.QPushButton("Reset and Save Graphs")
        self.layout.addWidget(self.reset_and_save_graphs_button, 5, 0)
        self.reset_and_save_graphs_button.clicked.connect(self.reset_and_save_graphs)
        self.reset_and_save_graphs_button.setEnabled(False)
        
        #Send button
        self.button = QtWidgets.QPushButton("SEND")
        self.layout.addWidget(self.button, 1, 2)
        self.button.clicked.connect(self.send_test)

        #Text view
        self.console = QtWidgets.QTextBrowser()
        self.layout.addWidget(self.console, 1, 1, 5, 1) 

    def send_test(self):
        self.rf.input_transmitter.send("HELLO")


    def reset_and_save_graphs(self):
        for i, graph in enumerate(self.graphs):
            exporter = pg.exporters.SVGExporter(graph.getPlotItem())
            path = str(self.file_management_panel.output_location.joinpath('./Graphs/'+str(i)+'.svg'))
            exporter.export(path)
            graph.getPlotItem().clear()

        self.file_management_panel.find_next_available_save_location_in_current_directory()

        self.connect_serial_button.setEnabled(True)
        self.reset_and_save_graphs_button.setEnabled(False)




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
        self.graphed_most_recent_value = Value('B')
        self.graphed_most_recent_value.value = 0

        self.looping_for_data = Value('i', 1) #Controls whether the listenig process is running.

        self.rf = RF(port, baud, self._data['current_frame'], self._data['frame_queue'], self._data['log_queue'], handled_most_recent=self.graphed_most_recent_value, telem_string=telem_frame_string)

        for graph in self.graphs:
            graph.setup_connection(self._data['current_frame'])

    def stop_and_save(self):
        self._data['log_queue'].put('STOP')
        self._data['frame_queue'].put('STOP')
        self.looping_for_data.value = 0

        self.stop_listening_and_save_button.setEnabled(False)
        self.connect_serial_button.setEnabled(False)
       
        for graph in self.graphs:
            graph.show_history()

        self.animation_timer.stop()
        
        self.reset_and_save_graphs_button.setEnabled(True)

    def setup_graphs(self):
        self.graphs = []

        self.graphs.append(custom_graph_widget((5, 6, 7), names=('euler_x', 'euler_y', 'euler_z')))
        self.graphs.append(custom_graph_widget((2, 3, 4), names=('velocity_x', 'velocity_y', 'velocity_z')))
        self.graphs.append(custom_graph_widget((11, 12), names=('current_u[x]', 'current_u[y]')))


        self.layout.addWidget(self.graphs[0], 0, 2)
        self.layout.addWidget(self.graphs[1], 0, 0)
        self.layout.addWidget(self.graphs[2], 0, 1)

        
    
    def _update_plot_data(self):
        if(self.graphed_most_recent_value.value == 0):
            for graph in self.graphs:
                graph.update_lines()
            self.graphed_most_recent_value.value = 1



    def _start_animation_timer(self):
        self.animation_timer = QtCore.QTimer()
        self.animation_timer.setInterval(10)
        self.animation_timer.timeout.connect(self._update_plot_data)
        self.animation_timer.start()
        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = GroundControlWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())