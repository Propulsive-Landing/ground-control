from PySide6 import QtCore, QtWidgets
from pathlib import Path
from os import mkdir



class file_management_widget(QtWidgets.QWidget):
    def __init__(self, output) -> None:
        super().__init__()
        self.layout = QtWidgets.QFormLayout(self)

        select_struct_button = QtWidgets.QPushButton("Select Struct Definition Directory")
        self.manual_struct_string = QtWidgets.QLineEdit()
        self.manual_struct_string.setPlaceholderText("Struct String")

        self.layout.addRow(select_struct_button, self.manual_struct_string)

        select_output_directory_button = QtWidgets.QPushButton("Select Output Directory")
        self.show_output_directory = QtWidgets.QLineEdit()
        self.show_output_directory.setReadOnly(True)

        self.layout.addRow(select_output_directory_button, self.show_output_directory)
        
        self.port_input = QtWidgets.QLineEdit()
        self.port_input.setPlaceholderText("Enter Port")
        self.layout.addRow(self.port_input)

        self.output = output


        self.struct_string = None
        self.output_location = None
        self.header = None

        self.manual_struct_string.textEdited.connect(self._update_struct_string)
        select_struct_button.clicked.connect(self._get_struct)
        select_output_directory_button.clicked.connect(self._get_output_location)

    def _get_output_location(self):
        self.output_directory = Path(QtWidgets.QFileDialog.getExistingDirectory(self, "Choose Output Location"))

        if(not self.output_directory):
            return
        self.find_next_available_save_location_in_current_directory()

    def find_next_available_save_location_in_current_directory(self):
        temp_location = self.output_directory.joinpath('./run0')
        index = 1

        while(temp_location.exists()):
            temp_location = self.output_directory.joinpath('./run'+str(index))
            index += 1
        
        self.output_location = temp_location
        self.show_output_directory.setText(str(self.output_location))

    def _get_struct(self):
        struct_directory = Path(QtWidgets.QFileDialog.getExistingDirectory(self, "Choose Directory with Struct Defintion"))
        structure_file = struct_directory.joinpath('./structure.txt')
        struct_string_file = struct_directory.joinpath('./struct_string.txt')

        if(structure_file.is_file()):
            temp_header = ''
            with open(structure_file) as file:
                try:
                    file.readline()
                    for line in file.readlines():
                        line = line.strip()
                        if(line):
                            if(int(line.split(',')[1]) > 1):
                                for i in range(0, int(line.split(',')[1])):
                                    temp_header += line.split(',')[2] + '[' + str(i) + '], '
                            else:
                                temp_header += line.split(',')[2] + ', '
                except:
                    print("ERR")
            self.header = temp_header


        if(not struct_string_file.is_file()):
            self.output("No structure defintion in directory")
            return
        
        with open(struct_string_file) as file: 
            self.struct_string = file.readline().strip()
        
        self.manual_struct_string.setText(self.struct_string)

    def _update_struct_string(self):
        self.struct_string = self.manual_struct_string.text()

    def create_files(self):
        mkdir(self.output_location)
        mkdir(self.output_location.joinpath('./Graphs'))

        data_path = self.output_location.joinpath('./data.csv')
        log_path = self.output_location.joinpath('./output.log')

        with open(data_path, 'w') as file:
            if(self.header):
                file.write(self.header)
                file.write('\n')

        return data_path, log_path

    #Checks that data management values are valid
    def check_ready(self):
        if(not (self.struct_string and self.output_location)):
            self.output('Error: Struct String and Output Location must be set')
            return False
        if(not self.struct_string):
            self.output('Error: Must set Struct String')
            return False
        elif(not self.output_location):
            self.output('Error: Must set Output Location')
            return False

        return True

    

    