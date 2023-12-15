from typing import Optional
import sqlite3


def do_request(request: str) -> Optional[str]:
    """Выполняет запрос к бд"""
    conn, result = None, None
    try:
        conn = sqlite3.connect("saves.db")
        cur = conn.cursor()

        # Выполняем запрос
        cur.execute(request)
        # Если что-то прочиталиЮ что всё запишется в result
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


def save(name: str, code: str):
    """Сохраняем код как новое сохранение в бд"""
    if load(name) == []:
        do_request(f"insert into saves (name, code) values ('{name}', '{code}');")
    else:
        raise ValueError(f"Сохранение с именем {name} уже существует")


def load(name: str) -> str:
    """Загружаем и возвращаем код из сохранения"""
    code = do_request(f"select code from saves where name = '{name}';")
    return code


def delete(name: str):
    """Удаляем сохранение из бд"""
    do_request(f"delete from saves where name = '{name}';")


def create_new_table():
    """Создаём новую таблицу (зачем?)"""
    do_request("create table if not exists saves (name text not null, code text);")
