from db_saver import *
from interpreter import run
from reformat_code import reformate_user_code

# Исходный код от пользователя
raw_code = open("user_code.txt", "r").readlines()

reformate_user_code()

run(code)