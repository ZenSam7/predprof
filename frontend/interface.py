import os
from backend.interpreter import run_code
from backend.reformat import *
from backend.db_saver import *
from frontend.draw_agent import Game
from frontend.ui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog
)
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

        # Остановлен ли интерфейс
        self.stopped = False

        # Оттрисовываем изначально эти координаты
        self.route = [[0, 0]]

        # Записываем код в редактор кода
        with open(file, "r", encoding="utf-16") as f:
            self.ui.textEdit.setText(f.read())

        self.game = Game()
        self.update(self.game_x, self.game_y, self.game_size, self.game_size)

        # Если у нас в file_path путь, возвращаем путь
        # Если у нас в file_path имя на сохранение в бд, возвращаем сохранение
        def getter_fite_path(): return db_load(self.file_path) if "/" in self.file_path else self.file_path
        # Заголовок текущего файла
        self.file_path = property(getter_fite_path)
        self.file_path = ""

        # При нажатии на кнопку запускаем или форматируем код
        self.ui.button_start.clicked.connect(self.start_code)
        self.ui.button_start_with_reset.clicked.connect(self.start_code_with_reset)
        self.ui.button_stop.clicked.connect(self.stop_code)
        self.ui.button_reformat.clicked.connect(self.format_code)

        # Подключаем команды к кнопкам
        self.ui.actionOpen_txt.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave_as_txt.triggered.connect(self.save_as_txt)
        self.ui.actionExport_as_txt.triggered.connect(self.export_as_txt)
        self.ui.actionImport_file.triggered.connect(self.import_file)
        self.ui.actionImport_db.triggered.connect(self.import_db)
        self.ui.export_menu.triggered.connect(self.export_from_submenu)
        self.export_from_submenu()

        # Отрисовка таблицы
        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(1)

    def export_from_submenu(self):
        """Назначаем каждому сохранению всё замыкание для загрузки в окно"""
        for db_save_name in db_titles_saves():
            def close_name_for_export(name: str):
                def export_from_db():
                    nonlocal name
                    self.ui.textEdit.setText(db_load(name))

                    # Чтобы у нас каждый раз изменялось количество кнопок
                    self.export_from_submenu()

                return export_from_db

            # Добавляем Кнопку
            if not ("save_for_sub_menu_" + db_save_name in self.ui.__dict__):
                # Добавляем сохранение в меню Экспорт
                self.ui.__dict__["save_for_sub_menu_" + db_save_name] = QtWidgets.QAction(self.ui.MainWindow)
                self.ui.__dict__["save_for_sub_menu_" + db_save_name].setText(db_save_name)
                self.ui.export_menu.addAction(self.ui.__dict__["save_for_sub_menu_" + db_save_name])

            self.ui.__dict__["save_for_sub_menu_" + db_save_name].triggered.connect(
                close_name_for_export(db_save_name)
            )

    def export_as_txt(self):
        # ))))))
        self.save_as_txt()

    def import_db(self):
        """Импортируем из окна редактирования"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "Введите название для сохранения в бд ()")

        # Нам нужно только имя для сохранения в бд
        save_name = file_path.split("/")[-1].split(".")[0]

        # Сохраняем в бд
        db_save(save_name, self.ui.textEdit.toPlainText())

        # Добавляем сохранение в меню Экспорт
        self.export_from_submenu()

    def import_file(self):
        self.open_file()
        import_from_file(self.file_path)

        # Добавляем сохранение в меню Экспорт
        self.export_from_submenu()

    def format_code(self):
        """Форматируем код в редакторе кода"""
        raw_code = self.ui.textEdit.toPlainText().split("\n")
        norm_code = code_for_user(raw_code)
        self.ui.textEdit.setText("".join(norm_code))

    def open_file(self):
        """Открываем сохранение через диалоговое окно"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "")
        if file_path:
            with open(file_path, "r", encoding="utf-16") as file:
                self.ui.textEdit.setText(file.read())
                self.file_path = file_path

    def stop_code(self):
        """Останавливаем код"""
        self.game.should_here = self.game.coords
        self.route = []
        self.stopped = True

    def save(self):
        """Сохраняем сохранение"""
        # Если мы открыли или уже ранее сохраняли файлы, то не парим пользователя
        if self.file_path:
            os.remove(self.file_path)
            with open(self.file_path, "w+", encoding="utf-16") as file:
                file.write(self.ui.textEdit.toPlainText())
        else:
            self.save_as_txt()

    def save_as_txt(self):
        """Сохраняем сохранение через диалоговое окно"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Текстовые файлы (*.txt)")
        if file_path:
            with open(file_path, "w+", encoding="utf-16") as file:
                file.write(self.ui.textEdit.toPlainText())
                self.file_path = file_path

    def start_code_with_reset(self):
        """Та же кнопка запуска кода, но сбрасываем все переменные и процедуры"""
        import backend.interpreter as i
        i.vars.clear()
        i.procedures.clear()
        i.route = [[0, 0]]
        self.route = [[0, 0]]
        i.coords = [0, 0]
        self.game.coords = [0, 0]
        self.game.should_here = [0, 0]
        self.game.move_cube((0, 0))
        self.stopped = False
        self.start_code()

    def start_code(self):
        code = self.ui.textEdit.toPlainText().split('\n')
        print(code)

        # В route записываем последовательность координат по которым надо пройтись,
        # и потом рисуем агента в paintEvent по 1 клетке
        self.route, err = run_code(code_for_interpeter(code))
        self.ui.textEdit_2.setText("Всё хорошо")

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
        # Если мы остановили Исполнителя и запускаем его при помощи "Старт",
        # то не выводим ошибки "Процедура .. уже объявлена"
        if self.stopped:
            self.stopped = False
            return

        # Выполните здесь ваш код обработки исключений
        # Например, отобразите диалоговое окно с информацией об ошибке
        error_message = f"{exc_type.__name__}: {exc_value}"

        # ДЛЯ ДЕБАГА
        error_message += f"{exc_traceback.__name__}"

        self.ui.textEdit_2.setText(error_message)


def begin_app():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = my_window()
    sys.excepthook = w.excepthook
    w.show()
    sys.exit(app.exec_())
