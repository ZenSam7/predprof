from os import remove as remove_file


def code_for_user(raw_code: list[str]) -> list[str]:
    """Форматируем код для пользователя
    (добавляем/убираем отступы, все комады пишем заглавными буквами)"""
    code = []
    amount_indent = 0  # Количество отступов

    # Форматируем каждую строку
    for index, string in enumerate(raw_code):
        if string == "\n":
            code.append("\n")
            continue

        string = string.strip()  # Обрезаем все пробелы

        # Убираем все "\n"
        if string.endswith("\n"):
            string = string[:-1]

        # Разбиваем строку на название команды и значение для этой команды
        if string.upper().startswith("END"):
            command, value = string, " "
        else:
            command, value = string.split(maxsplit=1)

        # Убираем лишние пробелы после команды
        value = value.replace(" ", "")

        # Если value это направление, то оно тоже в верхнем регистре
        if value.upper() in ("LEFT", "RIGHT", "UP", "DOWN"):
            value = value.upper()

        # Делаем команду в верхнем регистре
        string = command.upper() + " " + value

        # Добавляем отступы
        string = " "*4 * amount_indent + string

        # Увеличиваем или уменьшаем количество отступов для следующих строк
        if string.split()[0] in ("IFBLOCK", "REPEAT", "PROCEDURE"):
            amount_indent += 1

            # Обрабатываем асимальное количество вложенных конструкций
            if amount_indent == 4:
                raise Exception(f"Достугнуто максимальное количство "
                                f"вложенных команд: 3 в строке {index+1 +1}")

        elif string.split()[0] in ("ENDIF", "ENDREPEAT", "ENDPROC"):
            amount_indent -= 1

            # Обрабатываем возможную ошибку
            if amount_indent < 0:
                raise Exception(f"Лишняя команда: {string} в строке {index +1}")

            string = string[4:]

        string += "\n"

        code.append(string)

    # Максимальное колиество пустых строк подряд - 2
    code = "".join(code)
    while "\n\n\n\n" in code:
        code = code.replace("\n\n\n\n", "\n\n\n")

    return code


def reformate_user_code(file_path: str = "user_code.txt"):
    """Заменяем файл со старым кодом, на файл с нормальным кодом"""
    # Исходный код от пользователя
    raw_code = open(file_path, "r").readlines()

    # Форматируем код (удаляем файл с старым кодом и заменяем на нормальный)
    code = code_for_user(raw_code)
    remove_file(file_path)

    with open(file_path, "w+") as user_file:
        for string in code:
            user_file.write(string)


def code_for_interpeter(raw_code: list[str]) -> list[str]:
    """Форматируем код для интерпретатора (убираем пустые строки и отступы)"""
    code_for_interpreter = []

    # Записываем все не пустые строки в code, убираем "\n" и отступы
    for command in code_for_user(raw_code):
        if command == "\n":
            continue
        if command.endswith("\n"):
            command = command[:-1]

        command = command.strip()  # Обрезаем отступы

        code_for_interpreter.append(command)

    return code_for_interpreter