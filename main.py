from db_saver import *

with open("./usr_code.txt", "r") as usr_code:
    code = []
    # Записываем все не пустые строки в code и убираем "\n"
    for command in usr_code.readlines():
        if command == "\n":
            continue
        command = command.lower()  # Делаем нижний регистр
        command = command[:-1] if "\n" in command else command

        code.append(command)

print(code)

raw_code = "".join(open("./usr_code.txt", "r").readlines())
