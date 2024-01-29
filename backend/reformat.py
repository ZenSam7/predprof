from os import remove
from codecs import BOM


def raise_error(func):
    """Декоратор для функций, работающие с файлом"""

    def try_run_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            raise FileNotFoundError("Файла не существует")
        except Exception as err:
            raise Exception(f"Проблемы с файлом")

    return try_run_func


def code_for_user(raw_code: list[str]) -> list[str]:
    """Форматируем код для пользователя
    (добавляем/убираем отступы, все комады пишем заглавными буквами)"""
    code = []
    amount_indent = 0  # Количество отступов

    # Форматируем каждую строку
    for index, string in enumerate(raw_code):
        string = string.strip()  # Обрезаем все пробелы

        # Убираем все "\n"
        string = string.replace("\n", "")

        if string == "":
            code.append("\n")
            continue

        # Определяем комментарии
        if string.startswith("#"):
            # Удаляем лишние пробелы
            while "  " in string:
                string = string.replace("  ", " ")

            # Комментарий должен начинаться с Большой Буквы (а остальные маленькие)
            string = "# " + string[1:].strip().capitalize()

        # Если это не комментарий
        else:
            # Разбиваем строку на название команды и значение для этой команды
            if string.upper() in ("ENDIF", "ENDREPEAT", "ENDPROC"):
                command, value = string, ""
            else:
                try:
                    command, value = string.split(maxsplit=1)
                except Exception as err:
                    raise NameError(f"Неизвестная команда: {string}")

            # Убираем лишние пробелы после команды
            value = value.replace(" ", "")

            # Если value это направление, то оно тоже в верхнем регистре
            if value.upper() in ("LEFT", "RIGHT", "UP", "DOWN"):
                value = value.upper()

            # Делаем команду в верхнем регистре
            string = command.upper() + " " + value

        # Добавляем отступы
        string = " " * 4 * amount_indent + string

        # Увеличиваем или уменьшаем количество отступов для следующих строк
        if string.split()[0] in ("IFBLOCK", "REPEAT", "PROCEDURE"):
            amount_indent += 1

            # Обрабатываем асимальное количество вложенных конструкций
            if amount_indent == 4:
                raise RecursionError(
                    f"Достугнуто максимальное количство "
                    f"вложенных команд: 3 в строке {index + 1 + 1}"
                )

        elif string.split()[0] in ("ENDIF", "ENDREPEAT", "ENDPROC"):
            amount_indent -= 1

            # Обрабатываем возможную ошибку
            if amount_indent < 0:
                raise Exception(f"Лишняя команда: {string} в строке {index + 1}")

            string = string[4:]

        string += "\n"

        code.append(string)

    # Максимальное колиество пустых строк подряд - 2
    code = "".join(code)
    while "\n\n\n\n" in code:
        code = code.replace("\n\n\n\n", "\n\n\n")

    # Убираем лишние пустые строки в конце файла
    while code.endswith("\n"):
        code = code[:-1]

    # Разделяем по строкам
    code = [string + "\n" for string in code.split("\n")]

    # Если для последней строки есть отступ, то мы что-то написани не так
    if amount_indent != 0:
        raise Exception("Ошибка в коде! Проверьте наличие всех ENDREPEAT, ENDIF и EDPROC")

    return code


@raise_error
def reformat_user_file_code(file_path: str, new_file_path: str = None):
    """Создаём или заменяем на файл с красивым кодом"""
    # Это надо чтобы можно было писать комментарии на русском
    open(file_path, "r+b").write(BOM)

    # Исходный код от пользователя
    raw_code = open(file_path, "rt", encoding="utf-16").readlines()

    # Форматируем код
    code = code_for_user(raw_code)

    # Если мы хотим ЗАМЕНИТЬ файл с кодом на нормальный, то удаляем его
    if new_file_path is None:
        remove(file_path)
        new_file_path = file_path

    with open(new_file_path, "w+", encoding="utf-16") as user_file:
        for string in code:
            user_file.write(string)


def code_for_interpeter(raw_code: list[str]) -> list[str]:
    """Форматируем код для интерпретатора (убираем пустые строки и отступы)"""
    code_for_interpreter = []

    # Записываем все не пустые строки в code, убираем: "\n", отступы и комментарии
    for string in raw_code:
        if "\n" in string:
            string = string.replace("\n", "")

        if string == "":
            continue

        string = string.strip()  # Обрезаем отступы

        if string.startswith("#"):
            continue

        code_for_interpreter.append(string)

    return code_for_interpreter
