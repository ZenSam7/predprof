from backend.db_saver import *
from backend.reformat import *
from frontend.interface import *

file = "code"  # Имя рабочего файла из txt_saves

reformat_user_file_code(f"./txt_saves/{file}.txt")  # Делаем красиво
import_from_file(f"./txt_saves/{file}.txt")  # Импортируем в бд

begin_app()
