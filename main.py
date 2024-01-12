from backend.db_saver import *
from backend.reformat import *
from frontend.interface import *
# Для меня: Когда надо конвертировать этот проект в программу,
# то ВЕЗДЕ в пути к папке сохранений надо написать ./_internal/txt_saves


file = "user_code"  # Имя рабочего файла из txt_saves

# Делаем красиво
reformat_user_file_code(f"./_internal/txt_saves/{file}.txt", "./_internal/txt_saves/code.txt")

begin_app()

run_code(
    code_for_interpeter(open("./_internal/txt_saves/user_code.txt", "r", encoding="utf-16").readlines()),
    Game()
)
