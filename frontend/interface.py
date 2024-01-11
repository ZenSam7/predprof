from PyQt5 import QtWidgets
from frontend.draw_agent import Game
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QTimer
from backend.interpreter import run_code
from frontend.ui import Ui_MainWindow
from backend.reformat import *


class My_Window(QtWidgets.QMainWindow):
    def __init__(self, start_file_path: str = ""):
        """Инициализация окна"""
        super(My_Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.game_x = 610
        self.game_y = 30
        self.game_size = 21 * 34

        with open(start_file_path, "r", encoding="utf-16") as f:
            self.ui.textEdit.setText(f.read())

        self.game = Game()
        self.update(self.game_x, self.game_y, self.game_size, self.game_size)
        self.ui.pushButton.clicked.connect(self.start)

        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(40)

    def start(self):
        """старт кода, не работает"""
        code = self.ui.textEdit.toPlainText().split("\n")

        # self.ui.reformat_text(my_window, code_for_user(code))
        run_code(code_for_interpeter(code), self.game)

    def pygame_loop(self):
        self.update(610, 30, 714, 714)

    def paintEvent(self, e):
        """Функция рисования"""
        if self.game:
            buf = self.game.wind.get_buffer()
            img = QImage(buf, self.game_size, self.game_size, QImage.Format_RGB32)
            p = QPainter(self)
            p.drawImage(self.game_x, self.game_y, img)

    def excepthook(self, exc_type, exc_value, exc_traceback):
        # Выполните здесь ваш код обработки исключений
        # Например, отобразите диалоговое окно с информацией об ошибке
        error_message = f"{exc_type.__name__}: {exc_value}"
        self.ui.textEdit_2.setText(error_message)


if __name__ == "__main__":
    import sys


    app = QtWidgets.QApplication(sys.argv)
    w = my_window()
    sys.excepthook = w.excepthook
    w.show()
    sys.exit(app.exec_())

