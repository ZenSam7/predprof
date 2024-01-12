from backend.db_saver import *
from backend.reformat import *
from frontend.interface import my_window
from PyQt5 import QtWidgets
import sys

# НЕ РАБОТАЕТ!!!!!

file = "code"  # Имя рабочего файла из txt_saves

reformat_user_file_code(f"./txt_saves/{file}.txt")  # Делаем красиво
import_from_file(f"./txt_saves/{file}.txt")  # Импортируем в бд

app = QtWidgets.QApplication([])
application = my_window()
application.setFixedSize(1360, 780)
application.show()

sys.exit(app.exec())

# НЕ РАБОТАЕТ!!!!!


