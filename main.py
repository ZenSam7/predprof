from db_saver import *
from reformat_code import *
from interpreter import run

# Исходный код от пользователя
raw_code = open("user_code.txt", "r").readlines()

reformate_user_code()
code = code_for_interpeter(raw_code)

print(code)
run(code)
