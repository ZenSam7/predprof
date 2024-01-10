import pygame

class Game():
    def __init__(self):
        self.cell_size = 34
        pygame.display.init()
        self.wind = pygame.display.set_mode((21 * self.cell_size, 21 * self.cell_size), pygame.HIDDEN)

        self.wind.fill((40, 50, 60))

        # Сетка
        for x in range(0, 22):
            for y in range(0, 22):
                pygame.draw.rect(self.wind,
                                 (90, 100, 110),
                                 (x * self.cell_size, y * self.cell_size, self.cell_size + 1, self.cell_size + 1),
                                 1)

        pygame.display.update()

    def move_cube(self, coords, command):
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

        # Выводим команду
        # font = pygame.font.Font(None, 40)  # Какой шрифт и размер надписи
        # text_SCORE = font.render(command, True, (220, 220, 220))
        # self.wind.blit(text_SCORE, (0, 0))

        pygame.display.update()