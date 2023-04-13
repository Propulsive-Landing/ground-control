from PySide6 import QtCore, QtWidgets

class commanding_signals(QtCore.QObject):
    command_signal = QtCore.Signal(str)

class commanding_panel(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        
        self.commands = commanding_signals() # Reference MUST be kept to prevent object deletion.
        self.command_signal = self.commands.command_signal

        self.layout = QtWidgets.QGridLayout(self)

        self.setup_gui()
        self.connect_functionality()


    def setup_gui(self):
        self.command = QtWidgets.QLineEdit()
        self.command.setPlaceholderText("Enter Command")
        self.layout.addWidget(self.command, 0, 0, 1, 2)

        self.send_command_button = QtWidgets.QPushButton("Send Command")
        self.layout.addWidget(self.send_command_button, 1, 0, 1, 2)

        self.abort_button= QtWidgets.QPushButton("ABORT")
        self.abort_button.setStyleSheet("background: red; color: white; font-size: 13px;")
        self.layout.addWidget(self.abort_button, 2, 0, 1, 2)

        self.countdown_button = QtWidgets.QPushButton("Go to countdown")
        self.countdown_button.setStyleSheet("background: green; font-size: 13px;")
        self.layout.addWidget(self.countdown_button, 3, 1)

        self.standby_button = QtWidgets.QPushButton("Nav start")
        self.standby_button.setStyleSheet("background: green; font-size: 13px;")
        self.layout.addWidget(self.standby_button, 3, 0)

        # self.update_acc_bias_button = QtWidgets.QPushButton("Update Acc Bias")
        # self.update_acc_bias_button.setStyleSheet("font-size: 13px")
        # self.layout.addWidget(self.update_acc_bias_button, 4, 0)

        # self.update_gyro_bias_button = QtWidgets.QPushButton("Update Gyro Bias")
        # self.update_gyro_bias_button.setStyleSheet("font-size: 13px")
        # self.layout.addWidget(self.update_gyro_bias_button, 4, 1)

        # self.bias_reset_button = QtWidgets.QPushButton("Bias Reset")
        # self.bias_reset_button.setStyleSheet("font-size: 13px")
        # self.layout.addWidget(self.bias_reset_button, 5, 0)

        self.nav_reset_button = QtWidgets.QPushButton("Nav Reset")
        self.nav_reset_button.setStyleSheet("font-size: 13px")
        self.layout.addWidget(self.nav_reset_button, 5, 1)

        self.drop_open = QtWidgets.QPushButton("Open Dropmech")
        self.drop_open.setStyleSheet("font-size: 13px")
        self.layout.addWidget(self.drop_open, 6, 0)

        self.drop_close = QtWidgets.QPushButton("Close Dropmech")
        self.drop_close.setStyleSheet("font-size: 13px")
        self.layout.addWidget(self.drop_close, 6, 1)

    def connect_functionality(self):
        self.command.returnPressed.connect(self.send_command_and_clear_text)
        self.send_command_button.clicked.connect(self.send_command_and_clear_text)
        self.countdown_button.clicked.connect(lambda: self.send_command("COMMAND: countdown"))
        self.standby_button.clicked.connect(lambda: self.send_command("COMMAND: nav_start"))
        self.abort_button.clicked.connect(lambda : self.send_command("COMMAND: ABORT"))
        # self.update_acc_bias_button.clicked.connect(lambda : self.send_command("COMMAND: acc_bias"))
        # self.update_gyro_bias_button.clicked.connect(lambda : self.send_command("COMMAND: gyro_bias"))
        # self.bias_reset_button.clicked.connect(lambda : self.send_command("COMMAND: bias_reset"))
        self.nav_reset_button.clicked.connect(lambda : self.send_command("COMMAND: nav_reset"))
        self.drop_open.clicked.connect(lambda : self.open_dropmech())
        self.drop_close.clicked.connect(lambda : self.send_command("DROPMECH: close"))


    def open_dropmech(self):
        try:
            if(self.current[1] >= 4):
                self.send_command("DROPMECH: open")
            else:
                print("not correct mode")
        except:
            self.send_command("")

    def send_command(self, command : str):
        self.command_signal.emit(command)

    def send_command_and_clear_text(self):
        self.send_command(self.command.text())
        self.command.setText("")