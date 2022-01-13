import struct
from PySide6 import QtCore, QtWidgets
from pathlib import Path


class file_management_widget(QtWidgets.QWidget):
    def __init__(self, output) -> None:
        super().__init__()
        self.layout = QtWidgets.QFormLayout(self)

        select_struct_button = QtWidgets.QPushButton("Select Struct Definition Directory")
        self.manual_struct_string = QtWidgets.QLineEdit()
        self.manual_struct_string.setPlaceholderText("Struct String")

        self.layout.addRow(select_struct_button, self.manual_struct_string)

        select_output_directory_button = QtWidgets.QPushButton("Select Output Directory")
        show_output_directory = QtWidgets.QLineEdit()
        show_output_directory.setEnabled(False)

        self.layout.addRow(select_output_directory_button, show_output_directory)
        
        self.output = output


        self.struct_string = None
        self.output_location = None
        self.header = None

        self.ready = False

        self.manual_struct_string.textEdited.connect(self.update_struct_string)
        select_struct_button.clicked.connect(self.get_struct)

    def get_struct(self):
        struct_directory = Path(QtWidgets.QFileDialog.getExistingDirectory(self, "Choose Directory with Struct Defintion"))
        structure_file = struct_directory.joinpath('./structure.txt')
        struct_string_file = struct_directory.joinpath('./struct_string.txt')

        if(not structure_file.is_file()):
            pass
        if(not struct_string_file.is_file()):
            self.output("No structure defintion in directory")
            return
        
        with open(struct_string_file) as file: 
            self.struct_string = file.readline().strip()
        
        self.manual_struct_string.setText(self.struct_string)

    def update_struct_string(self):
        self.struct_string = self.manual_struct_string.text()

    def check_ready(self):
        if(not (self.struct_string and self.output_location)):
            self.output('Error: Struct String and Output Location must be set')
            return False
        if(not (self.struct_string)):
            self.output('Error: Must set Struct String')
            return False
        elif(not self.output_location):
            self.output('Error: Must set Output Location')
            return False

        

    