def ifblock(dir: str):
    """Проверяем, можно ли идти в нужное направление"""
    # Если в dir опечатка, то вызываем ошибку
    if not (dir in ("RIGHT", "LEFT", "UP", "DOWN")):
        raise ValueError(f"Несуществующее направление: {dir}")

    possible: bool = (dir == "RIGHT" and coords[0] == 20) or \
                     (dir == "LEFT" and coords[0] == 0) or \
                     (dir == "UP" and coords[1] == 0) or \
                     (dir == "DOWN" and coords[1] == 20)
    return possible


def __check_available_value(value: [str, int]):
    """Проверяем чтобы значение было [1; 1000] и возвращаем это
     значение чтобы лишний раз не доставать из переменной"""
    global vars

    if value is None:
        return None

    # Если value это число
    if isinstance(value, int):
        pass

    # Если value это число в виде строки
    elif value.isdigit():
        value = int(value)

    # Если value это переменная
    elif isinstance(value, str):
        try:
            value = vars[value]
        except KeyError:
            raise ValueError(f"Неизвестная переменная: {value}")

    # Если value это что-то другое, то вызываем ошибку
    else:
        raise ValueError(f"Недопустимое значение: {value}")

    # Проверяем под диапазон
    if not 1 <= value <= 1000:
        raise ValueError(f"Выход за границы допустимых значений [1; 1000]: {value}")

    return value


def __check_offscreen():
    """Проверяем, вышел ли агент за экран"""
    global coords
    if not (0 <= coords[0] <= 20 and 0 <= coords[1] <= 20):
        raise ValueError(f"Выход за пределы экрана! Координаты: {coords}")


def pass_func(*args):
    """Ничего не делаем"""
    return


def right(value: [str, int]):
    """Перемещаем вправо (принимает переменную или число)"""
    global coords
    distance = __check_available_value(value)
    coords[0] += distance
    __check_offscreen()


def left(value: [str, int]):
    """Перемещаем влево (принимает переменную или число)"""
    global coords
    distance = __check_available_value(value)
    coords[0] -= distance
    __check_offscreen()


def up(value: [str, int]):
    """Перемещаем вверх (принимает переменную или число)"""
    global coords
    distance = __check_available_value(value)
    coords[1] -= distance
    __check_offscreen()


def down(value: [str, int]):
    """Перемещаем вниз (принимает переменную или число)"""
    global coords
    distance = __check_available_value(value)
    coords[1] += distance
    __check_offscreen()


def set(variable_and_value: str):
    # Убираем все пробелы
    variable_and_value = variable_and_value.replace(" ", "")


# Сюда записываем все команды в формате: ["имя_команды": функция]
all_commands = {"IFBLOCK": ifblock,
                "UP": up,
                "DOWN": down,
                "LEFT": left,
                "RIGHT": right,
                "SET": set,

                "ENDREPEAT": pass_func,
                "ENDIF": pass_func,
                "ENDPROC": pass_func,
                }

# Инициализируем переменные для интерпретатора
coords = [0, 0]  # Начало координат: слева сверху

vars = {}  # Все переменные тут
procedures = {}  # Все процедуры тут

# Выполняем команды по 1 строчке
# Этот указатель будем гонять туда-сюда по всему коду
command_ind: int = 0
