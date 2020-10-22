import os
import math

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtWidgets import QGridLayout
from PyQt5.Qt import QColor, QPalette, QPixmap

BACKGROUND_COLOR = (255, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0)

class PlayfieldWidget(QWidget):
    def __init__(self, size, symbol_directory_path):
        QWidget.__init__(self)
        self.size = size
        self.layout = QGridLayout()

        self.symbol_dict = {}
        for filename in os.listdir(symbol_directory_path):
            name = os.path.splitext(filename)[0]
            self.symbol_dict[name] = QPixmap(symbol_directory_path + '/' + filename)

        for y in range(self.size):
            for x in range(self.size):
                self.layout.addWidget(PlayFieldSquareWidget(self), x, y)

        self.setLayout(self.layout)

    def set_symbols_at(self, x, y, symbol_list):
        self.layout.itemAtPosition(self.size - y - 1, x).widget().set_symbols(symbol_list)

    def highlight_square(self, x, y):
        for a in range(self.size):
            for b in range(self.size):
                palette = self.palette()
                palette.setColor(QPalette.Window, QColor(*BACKGROUND_COLOR))
                self.layout.itemAtPosition(a, b).widget().setPalette(palette)
        y = self.size - y - 1
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(*HIGHLIGHT_COLOR))
        self.layout.itemAtPosition(y, x).widget().setPalette(palette)

    def set_background_symbol_at(self, x, y, symbol_name):
        for a in range(self.size):
            for b in range(self.size):
                palette = self.palette()
                palette.setColor(QPalette.Window, QColor(*BACKGROUND_COLOR))
                self.layout.itemAtPosition(a, b).widget().clear()
                self.layout.itemAtPosition(a, b).widget().setPalette(palette)
        y = self.size - y - 1
        pixmap = self.symbol_dict[symbol_name]
        self.layout.itemAtPosition(y, x).widget().setPixmap(pixmap)




class PlayFieldSquareWidget(QLabel):

    def __init__(self, playfield: PlayfieldWidget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playfield = playfield
        self.setAutoFillBackground(True)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255,0,0))
        self.setPalette(palette)

    def set_symbols(self, symbol_names):
        grid_size = math.ceil(math.sqrt(len(symbol_names)))
        position = 0
        #clear all previous elements from the layout
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        #set new layout elements
        for symbol_name in symbol_names:
            label = QLabel()
            label.setScaledContents(True)
            pixmap = self.playfield.symbol_dict[symbol_name]
            label.setPixmap(pixmap)
            #label.setText("TEST")
            self.layout.addWidget(label, position % grid_size, position // grid_size)
            position += 1

