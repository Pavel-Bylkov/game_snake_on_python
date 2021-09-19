# https://github.com/replit/play  - описание библиотеки Play

# pip3 install replit-play - сразу устанавливает и библиотеку play и pygame

import play
import pygame

play.set_backdrop((55, 155, 55))
WIN_X, WIN_Y = 1200, 810  # ширина и высота окна
pygame.display.set_mode((WIN_X, WIN_Y))

lines = []  # переменная список для линий сетки
STEP = 30  # шаг сетки в пикселях
SPEED = 0.5  # пауза меньше = скорость выше, пауза больше = скорость меньше


def net(step):
    """ Рисуем сетку для игры c шагом step"""
    for y in range(300, -500, -step):
        lines.append(
            play.new_line(
                color='black', x=-400, y=y,
                length=WIN_X, angle=0, thickness=1, x1=None, y1=None)
        )
    for x in range(-400, 800, step):
        lines.append(
            play.new_line(
                color='black', x=x, y=300,
                length=WIN_X, angle=-90, thickness=1, x1=None, y1=None)
        )


eat = play.new_image(
        image='eat.png', x=96, y=15, angle=0, size=4, transparency=100
    )


box = play.new_box(
        color='yellow',
        x=6, y=15, width=30, height=30,
        border_color="blue", border_width=2
    )


# Блок который работает один раз на старте и не повторяется
@play.when_program_starts
def do():
    net(STEP)


# Блок который работает в цикле - т.е. постоянно повторяется
@play.repeat_forever
async def move_box():

    box.move(STEP)

    await play.timer(seconds=SPEED)


@play.repeat_forever
async def eat_control():

    if eat.is_touching(box):
        eat.hide()
        old_x = eat.x
        old_y = eat.y
        x = play.random_number(lowest=-12, highest=26) * 30 + 5
        y = play.random_number(lowest=-16, highest=9) * 30 + 15
        while old_y == y and old_x == x:
            x = play.random_number(lowest=-12, highest=26) * 30 + 5
            y = play.random_number(lowest=-16, highest=9) * 30 + 15
        eat.go_to(x=x, y=y)
        eat.show()

    await play.timer(seconds=SPEED/2)


# Блок который работает в цикле - т.е. постоянно повторяется
@play.when_key_pressed('up', 'w', 'down', 's', 'right', 'd', 'left', 'a')
async def control(key):
    if key == 'up' or key == 'w':
        box.angle = 90
    if key == 'down' or key == 's':
        box.angle = -90
    if key == 'right' or key == 'd':
        box.angle = 0
    if key == 'left' or key == 'a':
        box.angle = 180
    await play.timer(seconds=0.001)

play.start_program()