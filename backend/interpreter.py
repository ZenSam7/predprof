def ifblock(dir: str):
    """Проверяем, можно ли идти в нужное направление"""
    # Если в dir опечатка, то вызываем ошибку
    if not (dir in ("LEFT", "RIGHT", "UP", "DOWN")):
        raise ValueError(f"Несуществующее направление: {dir}")

    possible: bool = (dir == "RIGHT" and coords[0] == 20) or \
                     (dir == "LEFT" and coords[0] == 0) or \
                     (dir == "UP" and coords[1] == 0) or \
                     (dir == "DOWN" and coords[1] == 20)
    return possible


def __check_available_value(value: [str | int]):
    """Проверяем чтобы значение было [1; 1000] и возвращаем это
     значение чтобы лишний раз не доставать из переменной"""
    global vars

    if value is None:
        return None

    # Если value это число
    elif isinstance(value, int):
        pass

    # Если value это число в виде строки
    elif value.isdigit():
        value = int(value)

    # Если value это переменная
    elif isinstance(value, str):
        try:
            value = vars[value]
        except KeyError:
            raise NameError(f"Неизвестная переменная: {value}")

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


def pass_func(*args, **kwargs):
    """Ничего не делаем"""
    return


def right(value: [str | int]):
    """Перемещаем вправо (принимает переменную или число)"""
    global coords
    distance = __check_available_value(value)
    coords[0] += distance

    # Если вышли за предела, то упираемся в стенку
    try:
        __check_offscreen()
    except ValueError as err:
        coords[0] = 20
        raise err


def left(value: [str | int]):
    """Перемещаем влево (принимает переменную или число)"""
    global coords
    distance = __check_available_value(value)
    coords[0] -= distance

    # Если вышли за предела, то упираемся в стенку
    try:
        __check_offscreen()
    except ValueError as err:
        coords[0] = 0
        raise err


def up(value: [str | int]):
    """Перемещаем вверх (принимает переменную или число)"""
    global coords
    distance = __check_available_value(value)
    coords[1] -= distance

    # Если вышли за предела, то упираемся в стенку
    try:
        __check_offscreen()
    except ValueError as err:
        coords[1] = 0
        raise err


def down(value: [str | int]):
    """Перемещаем вниз (принимает переменную или число)"""
    global coords
    distance = __check_available_value(value)
    coords[1] += distance

    # Если вышли за предела, то упираемся в стенку
    try:
        __check_offscreen()
    except ValueError as err:
        coords[1] = 20
        raise err


def set(variable_and_value: str):
    """Устанавливаем для переменной нужное значение"""
    global vars

    name_var, value = variable_and_value.split("=")

    if name_var[0].isdigit():
        raise NameError(f"Недопустимое имя переменной: {name_var}")

    value = __check_available_value(value)

    vars[name_var] = value


def call(name_proc: str):
    """Выполняем процедуру"""
    try:
        procedure_code = procedures[name_proc]
    except KeyError:
        raise ValueError(f"Неизвестное название процедуры: {name_proc}")

    # Код процедуры выполняем отдельно
    run_code(procedure_code, game)


# Сюда записываем все команды в формате: ["имя_команды": функция]
all_commands = {"IFBLOCK": ifblock,
                "UP": up,
                "DOWN": down,
                "LEFT": left,
                "RIGHT": right,
                "SET": set,
                "CALL": call,

                "ENDREPEAT": pass_func,
                "ENDIF": pass_func,
                "ENDPROC": pass_func,
                }

# Инициализируем переменные для интерпретатора
coords = [0, 0]  # Начало координат: слева сверху

vars: dict[str, int] = {}  # Все переменные тут
procedures: dict[str, list[str]] = {}  # Все процедуры тут

route: list[[int, int]] = [[0, 0]]  # Список всех прошлых координат


def iter_command(code: list[str], command_ind: int, game) -> int:
    """Интепретируем (выполняем) команду и возвращаем индекс
     команды на котором остановились"""
    global procedures, route, coords
    string = code[command_ind]

    # Разбиваем команду на название команды и значение этой команды
    if string.startswith("END"):
        command, value = string, None
    else:
        command, value = string.split(maxsplit=1)

    # Если у нас команда, которая принимает целый блок кода, то с ними поступаем иначе
    if command == "IFBLOCK":
        """Если у нас IFBLOCK вернул False, то пропускаем команды до ENDIF
           Если он вернул True, то просто продолжаем выполнять команды"""

        if not all_commands[command](value):
            skip = command_ind
            while code[skip] != "ENDIF":
                skip += 1
            return skip

    elif command == "REPEAT":
        """Рекурсивно выполняем блок кода от command_ind до endrepeat_index"""
        # Вычисляем промежуток строк который должны повторить
        startrepeat_index = command_ind + 1
        endrepeat_index = command_ind
        while code[endrepeat_index] != "ENDREPEAT":
            endrepeat_index += 1

        # Проверяем правильность value (может быть как числом так и переменной)
        value = __check_available_value(value)

        for N in range(value):
            index = startrepeat_index
            while index < endrepeat_index:
                index = iter_command(code, index, game)
                index += 1

        return endrepeat_index

    elif command == "PROCEDURE":
        """В procedures записываем название процедуры и его код"""
        procedure_code = []

        while code[command_ind] != "ENDPROC":
            command_ind += 1
            procedure_code.append(code[command_ind])

        # Записываем код для соответствующей процедуры
        # (если она не была объявлена раньше, и имя процедуры корректно)
        if value in procedures:
            raise NameError(f"Процедура {value} уже объявлена")
        elif value[0].isdigit():
            raise NameError(f"Некорректное имя процедуры: {value}")
        else:
            procedures[value] = procedure_code

        return command_ind

    elif command in ("LEFT", "RIGHT", "UP", "DOWN"):
        # Проверяем правильность value для команд right/left/up/down
        value = __check_available_value(value)

    # Добавляем координаты в маршрут
    if coords.copy() != route[-1]:
        route.append(coords.copy())

    # Просто выполняем команду без всяких заморочек
    all_commands[command](value)

    # Двигаем Исполнителя (сначала ходим, потом отрисовываем)
    game.move_cube(coords, string)
    
    return command_ind


def run_code(code: list[str], Game):
    """Выполняем предоставленный код
    (передаем экземпляр доски чтобы рисовать квадратики)"""
    # Выполняем команды по 1 строчке
    # Этот указатель будем гонять туда-сюда по всему коду
    command_ind: int = 0

    # Это надо чтобы работала фнкция call (в ней нельзя передать game)
    global game
    game = Game

    while command_ind < len(code):
        # Выполняем команду и Двигаемся дальше
        command_ind = iter_command(code, command_ind, game)
        command_ind += 1
