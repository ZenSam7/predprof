from backend.interpreter import run_code
from backend.reformat import *
from frontend.draw_agent import Game
from frontend.ui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QTimer
from time import time
import asyncio


class my_window(QtWidgets.QMainWindow):
    def __init__(self, file="./txt_saves/code.txt"):
        """Инициализация окна"""
        super(my_window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Размеры игрового окна
        self.game_x = 610
        self.game_y = 30
        self.game_size = 21 * 34

        # Оттрисовываем изначально эти координаты
        self.route = [[0, 0]]

        # Записываем код в редактор кода
        with open(file, "r", encoding="utf-16") as f:
            self.ui.textEdit.setText(f.read())

        self.game = Game()
        self.update(self.game_x, self.game_y, self.game_size, self.game_size)

        # При нажатии на кнопку запускаем код
        self.ui.pushButton.clicked.connect(self.start_code)

        # Отрисовка таблицы
        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(1)

    def start_code(self):
        code = self.ui.textEdit.toPlainText().split('\n')
        print(code)

        # В route записываем последовательность координат по которым надо пройтись,
        # и потом рисуем агента в paintEvent по 1 клетке
        self.route, err = run_code(code_for_interpeter(code), [[0, 0]])
        self.ui.textEdit_2.setText('all is good')

        if err is not None:
            raise err

    def pygame_loop(self):
        self.update(self.game_x, self.game_y, self.game_size, self.game_size)

    def paintEvent(self, e):
        """Функция рисования (нельзя нормально рисовать Агента все этой функции)"""
        if self.game:
            # Оттрисовываем координаты Агента (по 1 клетке)
            if len(self.route) != 0:
                self.game.should_here = self.route[0]
                self.game.frame_cube_animate(self.route[0])

                # Когда дошли до необходимый координат, то удаляем их и движевся дальше
                if self.game.coords == self.route[0]:
                    self.route.pop(0)

            buf = self.game.wind.get_buffer()
            img = QImage(buf, self.game_size, self.game_size, QImage.Format_RGB32)
            p = QPainter(self)
            p.drawImage(self.game_x, self.game_y, img)

    def excepthook(self, exc_type, exc_value, exc_traceback):
        # Выполните здесь ваш код обработки исключений
        # Например, отобразите диалоговое окно с информацией об ошибке
        error_message = f"{exc_type.__name__}: {exc_value}"

        # ДЛЯ ДЕБАГА
        # error_message += f"{exc_traceback.__name__}"

        self.ui.textEdit_2.setText(error_message)


def begin_app():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = my_window()
    sys.excepthook = w.excepthook
    w.show()
    sys.exit(app.exec_())
