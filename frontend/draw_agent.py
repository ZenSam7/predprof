import pygame
from time import sleep


class Game():
    def __init__(self):
        self.cell_size = 34

        # pygame.HIDDEN т.к. выводим поле в окне через буфер дисплея (если убрать, будет новое окно)
        pygame.display.init()
        self.wind = pygame.display.set_mode((21 * self.cell_size, 21 * self.cell_size), pygame.HIDDEN)

        # Когда двигаем агента по 1 клетке, в итоге должны мереместить его сюда
        self.should_here = [0, 0]
        self.coords = [0, 0]

        # Сколько секунд ждём между движением по клетке
        self.agent_speed = 0.05

        self.move_cube((0, 0))

    def frame_cube_animate(self, coords: list[int, int]):
        """Двигаем агента на 1 клетку до координат should_here"""
        x, y = self.coords

        if self.should_here[0] > x:
            x += 1
        elif self.should_here[0] < x:
            x -= 1

        if self.should_here[1] > y:
            y += 1
        elif self.should_here[1] < y:
            y -= 1

        self.move_cube([x, y])
        self.coords = [x, y]

        sleep(self.agent_speed)

    def move_cube(self, coords: list[int, int], command: str = None):
        """Двигаем Исполнителя"""
        # Очистка экрана
        self.wind.fill((40, 50, 60))

        # Сетка
        for x in range(0, 22):
            for y in range(0, 22):
                pygame.draw.rect(self.wind,
                                 (90, 100, 110),
                                 (x * self.cell_size, y * self.cell_size, self.cell_size + 1, self.cell_size + 1),
                                 1)

        # Исполнитель
        pygame.draw.rect(
            self.wind,
            (120, 130, 140),
            (
                coords[0] * self.cell_size,
                coords[1] * self.cell_size,
                self.cell_size,
                self.cell_size,
            ),
        )

        self.coords = coords

        # Выводим команду
        # pygame.font.init()
        # font = pygame.font.Font(None, 40)  # Какой шрифт и размер надписи
        # text_SCORE = font.render(command, True, (220, 220, 220))
        # self.wind.blit(text_SCORE, (0, 0))

        pygame.display.update()
