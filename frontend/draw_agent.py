import pygame
from time import sleep

class Game():
    def __init__(self):
        self.cell_size = 34
        pygame.display.init()
        self.wind = pygame.display.set_mode((21 * self.cell_size, 21 * self.cell_size), pygame.HIDDEN)

        self.move_cube([0, 0], 'hello')

        pygame.display.update()

    def move_cube(self, coords, command):
        print(coords, command)
        self.wind.fill((40, 50, 60))

        for x in range(0, 22):
            for y in range(0, 22):
                pygame.draw.rect(self.wind,
                                 (90, 100, 110),
                                 (x * self.cell_size, y * self.cell_size, self.cell_size + 1, self.cell_size + 1),
                                 1)

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
        print(2)

        pygame.display.update()
# class Game():
#     def __init__(self):
#         self.cell_size = 34
#         self.speed_move_cube = 3000  # Условные единицы
#         self.old_coords = (0.1, 0)
#         pygame.display.init()
#         self.wind = pygame.display.set_mode((21 * self.cell_size, 21 * self.cell_size), pygame.HIDDEN)
#
#         self.move_cube((0, 0))
#
#     def move_cube(self, coords: list[int, int], print_comand: str = None):
#         """Двигаем Исполнителя постепенно"""
#         self.wind.fill((40, 50, 60))
#
#         # Сетка
#         for x in range(0, 22):
#             for y in range(0, 22):
#                 pygame.draw.rect(self.wind,
#                                  (90, 100, 110),
#                                  (x * self.cell_size, y * self.cell_size, self.cell_size + 1, self.cell_size + 1),
#                                  1)
#
#         # Вспомогательные переменные
#         delay_between_frame = self.cell_size / self.speed_move_cube
#         pixel_size = 1 / self.cell_size
#         x, y = self.old_coords
#
#         # Двигаем плавно
#         while round(x, 1) != coords[0] or round(y, 1) != coords[1]:
#             if x < coords[0]:
#                 x += pixel_size
#             elif x > coords[0]:
#                 x -= pixel_size
#             if y < coords[1]:
#                 y += pixel_size
#             elif y > coords[1]:
#                 y -= pixel_size
#
#             # Исполнитель
#             pygame.draw.rect(
#                 self.wind,
#                 (120, 130, 140),
#                 (
#                     coords[0] * self.cell_size,
#                     coords[1] * self.cell_size,
#                     self.cell_size,
#                     self.cell_size,
#                 ),
#             )
#             pygame.display.update()
#
#             # Ждёмс
#             pygame.time.delay(int(delay_between_frame*1000))
#
#         self.old_coords = coords