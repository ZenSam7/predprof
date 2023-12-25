from tkinter import *
from tkinter import scrolledtext
import pygame

text_size = 21

cell_size = 30
edit_field_width = 30

# Окно
window = Tk()
window.title("GridMaster от команды ¯\\_(ツ)_/¯")

# Как сделать чтобы поле для агента было квадратным и зависило
# от размера шрифта и edit_field_width ???
window.geometry(f"{21*cell_size + edit_field_width}x{21*cell_size}")


# Поле для кода
edit_field = scrolledtext.ScrolledText(
    window,
    width=edit_field_width,
    font=("Calibri", text_size),
    fg="#222",
    bg="#eee",
)

edit_field.pack(side="left", fill="y", expand=False)


def begin_app():
    window.mainloop()
