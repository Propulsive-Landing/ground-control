import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg

#https://www.pythonguis.com/tutorials/plotting-pyqtgraph/

class MyWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("CLICK ME!")
        self.text = QtWidgets.QLabel("HELLO", alignment=QtCore.Qt.AlignCenter)

        self.graph = pg.PlotWidget()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.graph)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
        self.graph.plot(hour, temperature)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())