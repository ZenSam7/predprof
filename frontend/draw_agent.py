import pygame
from time import sleep

cell_size = 40

pygame.init()

wind = pygame.display.set_mode((21 * cell_size, 21 * cell_size))
pygame.display.set_caption("Predprof")


def draw(coords: list[int, int], string: str):
    pygame.event.get()

    # Фон
    wind.fill((40, 50, 60))

    # Сетка
    for x in range(0, 22):
        for y in range(0, 22):
            pygame.draw.rect(
                wind,
                (90, 100, 110),
                (x * cell_size, y * cell_size, cell_size + 1, cell_size + 1),
                1,
            )

    # Агент
    pygame.draw.rect(
        wind,
        (120, 130, 140),
        (
            coords[0] * cell_size,
            coords[1] * cell_size,
            cell_size,
            cell_size,
        ),
    )

    # Выводим команду
    font = pygame.font.Font(None, 40)  # Какой шрифт и размер надписи
    text_SCORE = font.render(string, True, (220, 220, 220))
    wind.blit(text_SCORE, (0, 0))

    # Ждёмс
    sleep(0.5)

    pygame.display.update()
