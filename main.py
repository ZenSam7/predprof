from backend.db_saver import *
from backend.reformat import *
from backend.interpreter import run_code

file = "user_code"  # Имя рабочего файла из txt_saves

# Делаем красиво
reformat_user_file_code(f"./txt_saves/{file}.txt", f"./txt_saves/code.txt")

# Импортируем в бд
import_from_file(f"./txt_saves/{file}.txt")
import_from_file(f"./txt_saves/code.txt")

# Запускаем
run_code(db_load_for_interpreter(file))
