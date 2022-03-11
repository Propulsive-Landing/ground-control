from PySide6 import QtCore, QtWidgets

class command_pannel(QtWidgets.QWidget):
    def __init__(self, command_function : function)  -> None:
        super().__init__()
        self.layout = QtWidgets.QFormLayout(self)
        self.command_function = command_function
