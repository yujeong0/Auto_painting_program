import sys
from make_model import make_model
from classification import classification
from real_drawing_board import drawing_board
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # 화면크기스케일링

class auto_painting:
    def __init__(self):
        self.painting()

    def painting(self):
        app = QApplication(sys.argv)
        board = drawing_board()
        board.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    w = auto_painting()
