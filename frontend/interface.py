from PyQt5 import QtWidgets
import sys
from frontend.draw_agent import Game
from PyQt5.QtGui import QImage, QPainter
from backend.interpreter import run_code
from frontend.ui import Ui_MainWindow
from backend.reformat import *


class my_window(QtWidgets.QMainWindow):
    def __init__(self, file):
        """инициализация окна"""
        super(my_window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.game_x = 610
        self.game_y = 30
        self.game_size = 21 * 34

        with open(file, "r", encoding="utf-16") as f:
            self.ui.textEdit.setText(f.read())

        self.game = Game()
        self.update(self.game_x, self.game_y, self.game_size, self.game_size)

        self.ui.pushButton.clicked.connect(self.start)

    def start(self):
        """старт кода, не работает"""
        code = self.ui.textEdit.toPlainText().split("\n")

        self.ui.textEdit.setText("\n".join(code_for_user(code)))
        try:
            run_code(code_for_interpeter(code), self.game)
        except Exception as e:
            print(e)
            self.ui.textEdit_2.setText(e)

    def paintEvent(self, e):
        """функция рисования"""
        if self.game:
            buf = self.game.wind.get_buffer()
            img = QImage(buf, self.game_size, self.game_size, QImage.Format_RGB32)
            p = QPainter(self)
            p.drawImage(self.game_x, self.game_y, img)


def begin_app():
    """Запуск окна"""
    app = QtWidgets.QApplication([])
    application = my_window("./txt_saves/code.txt")
    application.setFixedSize(1360, 780)
    application.show()
