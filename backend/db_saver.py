import os
import sqlite3
from .reformat import code_for_interpeter, raise_error


def _do_request(request: str):
    """Выполняет запрос к бд"""
    conn, result = None, None
    try:
        conn = sqlite3.connect("saves.db")
        cur = conn.cursor()

        # Добавляем ";"
        if not request.endswith(";"):
            request += ";"

        # Выполняем запрос
        cur.execute(request)
        # Если что-то прочитали, что всё запишется в result
        result = cur.fetchall()
        conn.commit()
        cur.close()

    except sqlite3.Error as err:
        print("Ошибка в подключении:", err)

    # Всегда закрываем подключение
    finally:
        if conn:
            conn.close()
        return result


def db_save(name: str, code: str):
    """Сохраняем код как новое сохранение в бд"""
    try:
        db_load(name)
    except ValueError:
        _do_request(f"insert into saves (name, code) values ('{name}', '{code}');")

    # Если сохраненпие уже есть, то удалаем его и заменяем новым
    else:
        db_delete(name)
        _do_request(f"insert into saves (name, code) values ('{name}', '{code}');")


def db_load(name: str) -> str:
    """Загружаем и возвращаем код из сохранения"""
    code = _do_request(f"select code from saves where name = '{name}';")

    if not code:
        raise ValueError(f"Сохранения {name} не существует")

    return code[0][0]


def db_delete(name: str):
    """Удаляем сохранение из бд"""
    _do_request(f"delete from saves where name = '{name}';")


def create_new_table():
    """Создаём новую таблицу (зачем?)"""
    _do_request(
        "create table if not exists saves (name text not null, code longtext);"
    )


@raise_error
def export_to_txt(name: str):
    """Экспортируем сохранение из бд в дайл"""
    # Убираем формат
    name = name.split(".")[0] if "." in name else name

    # Если файл уже есть, то заменяем
    if (name + ".txt") in os.listdir("./txt_saves"):
        os.remove(f"txt_saves/{name}.txt")

    with open(f"txt_saves/{name}.txt", "w+", encoding="utf-16") as file:
        file.write(db_load(name))


@raise_error
def import_from_file(file_path: str):
    """Импортируем сохранение в бд из файла"""
    with open(file_path, "r", encoding="utf-16") as file:
        code = "".join(file.readlines())

    # Има сохранения == название файла
    name = file_path.split("\\" if "\\" in file_path else "/")[-1]
    name = name.split(".")[0]

    db_save(name, code)


def db_load_for_interpreter(name: str) -> list[str]:
    """Загружаем файл по имени чтобы потом использовать в интерпретаторе"""
    loaded = db_load(name).split("\n")
    # Добавляем перенос строки к каждой строке
    raw_code = [string + "\n" for string in loaded]

    # Обрабатываем код для интерпретатора
    code_to_use = code_for_interpeter(raw_code)

    return code_to_use
