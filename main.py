from backend.db_saver import *
from backend.reformat import *
from backend.interpreter import run_code

from frontend.interface import begin_app

file = "user_code"  # Имя рабочего файла из txt_saves

export_to_txt(file)

reformat_user_file_code(
    f"./txt_saves/{file}.txt", f"./txt_saves/code.txt"
)  # Делаем красиво
import_from_file(f"./txt_saves/{file}.txt")  # Импортируем в бд

run_code(db_load_for_interpreter(file))  # Запускаем
