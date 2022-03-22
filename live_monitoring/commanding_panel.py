from PySide6 import QtCore, QtWidgets

class commanding_signals(QtCore.QObject):
    command_signal = QtCore.Signal(str)

class commanding_pannel(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        
        self.command_signal = commanding_signals().command_signal
        self.layout = QtWidgets.QGridLayout(self)

        self.setup_gui()
        self.connect_functionality()


    def setup_gui(self):
        self.command = QtWidgets.QLineEdit()
        self.command.setPlaceholderText("Enter Command")
        self.layout.addWidget(self.command, 0, 0)

        self.send_command_button = QtWidgets.QPushButton("Send Command")
        self.layout.addWidget(self.send_command_button, 1, 0)

        self.abort_button= QtWidgets.QPushButton("ABORT")
        self.abort_button.setStyleSheet("background: red; color: white; font-size: 13px;")
        self.layout.addWidget(self.abort_button, 2, 0)

        self.countdown_button = QtWidgets.QPushButton("GO FOR COUNTDOWN")
        self.countdown_button.setStyleSheet("background: lime; font-size: 13px;")
        self.layout.addWidget(self.countdown_button, 3, 0)

    def connect_functionality(self):
        self.command.returnPressed.connect(self.send_command_and_clear_text)
        self.send_command_button.clicked.connect(self.send_command_and_clear_text)
        self.countdown_button.clicked.connect(lambda: self.send_command("COMMAND: set_mode 1"))
        self.abort_button.clicked.connect(lambda : self.send_command("COMMAND: ABORT"))


    def send_command(self, command : str):
        self.command_signal.emit(command)

    def send_command_and_clear_text(self):
        self.send_command(self.command.text())
        self.command.setText("")