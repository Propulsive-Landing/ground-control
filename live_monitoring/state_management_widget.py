from PySide6 import QtCore, QtWidgets
import pyqtgraph as pg
import pyqtgraph.exporters
from multiprocessing import Array, Value, Queue
import struct

from file_management_widget import file_management_widget
import gui_util
from threading_logs import telem_frame_handler, log_handler
from rf import RF

class state_management_widget(QtWidgets.QWidget):
    def __init__(self, output, file_management_panel : file_management_widget, thread_pool, graphs, transmitting_buttons = []) -> None:
        super().__init__()
        self.layout = QtWidgets.QFormLayout(self)

        self.output = output #function that handles output messages
        self.file_management_panel = file_management_panel
        self.thread_pool = thread_pool 
        self.graphs = graphs #list of graphs type: pg.PlotWidget

        self.transmitting_buttons = transmitting_buttons #A list of buttons that iteract with RF my be disabled (or enabled) from here

        for button in self.transmitting_buttons:
            button.setEnabled(False)

        #connect button
        self.connect_serial_button = QtWidgets.QPushButton("Connect Serial and Listen")
        self.layout.addRow(self.connect_serial_button)
        self.connect_serial_button.clicked.connect(self.connect_and_listen)

        #stop and save button
        self.stop_listening_and_save_button = QtWidgets.QPushButton("Stop Listening and Save")
        self.layout.addRow(self.stop_listening_and_save_button)
        self.stop_listening_and_save_button.clicked.connect(self.stop_and_save)
        self.stop_listening_and_save_button.setEnabled(False)

        #Reset and Save Graphs
        self.reset_and_save_graphs_button = QtWidgets.QPushButton("Reset and Save Graphs")
        self.layout.addRow(self.reset_and_save_graphs_button)
        self.reset_and_save_graphs_button.clicked.connect(self.reset_and_save_graphs)
        self.reset_and_save_graphs_button.setEnabled(False)


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

        if(not gui_util.serial_port_available(self.file_management_panel.port_input.text())):
            self.output("GUI: Invalid Serial Port")
            return
        
        self.initialize_rf(self.file_management_panel.port_input.text(), 9600)
            
        self._start_animation_timer()
            
        self.data_path, self.log_path = self.file_management_panel.create_files()
        self.rf._telem_struct_unpacking_values['telem_struct_string'] = self.file_management_panel.struct_string

        self.looping_for_data.value = 1
        self.rf.start_listen_loop(self.looping_for_data)

        self.thread_pool.start(log_handler(self.log_path, self.output, self._data['log_queue']))
        self.thread_pool.start(telem_frame_handler(self.data_path, self.output, self._data['frame_queue']))
        self.stop_listening_and_save_button.setEnabled(True)

        for button in self.transmitting_buttons:
            button.setEnabled(True)

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
        self.graphed_most_recent_value.value = 1

        self.looping_for_data = Value('i', 1) #Controls whether the listenig process is running.

        self.rf = RF(port, baud, self._data['current_frame'], self._data['frame_queue'], self._data['log_queue'], handled_most_recent=self.graphed_most_recent_value, telem_string=telem_frame_string)

        for graph in self.graphs:
            graph.setup_connection(self._data['current_frame'])
