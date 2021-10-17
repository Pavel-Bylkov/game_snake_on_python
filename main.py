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
SHIFT = 0  # ускорение
score = 0  # для подсчета очков
TIMER = 5 * 60  # 5 min

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


# создаем спрайт - еда
apples = [
    play.new_image(
        image='eat.png', x=96, y=15, angle=0, size=4, transparency=100)
    ]

# создаем спрайт - голова змейки
box = play.new_box(
        color='yellow', x=6, y=15, width=30, height=30,
        border_color="blue", border_width=2
    )

# Спрайты в списке - тело
body = []

# спрайт для отображения очков
display_score = play.new_text(
        words=("SCORE: %0.3d" % score), x=670, y=280, angle=0, font=None, font_size=40,
        color='black', transparency=100
    )
display_timer = play.new_text(
        words=("TIME: %0.2d:%0.2d" % ((TIMER // 60), (TIMER % 60))),
        x=-300, y=280, angle=0, font=None, font_size=40,
        color='black', transparency=100
    )


def body_append():
    body.append(
        play.new_box(
            color='light yellow', x=800, y=400, width=30, height=30,
            border_color="blue", border_width=2
        )
    )


def body_move(index, pos):
    current_pos_body = body[index].x, body[index].y
    body[index].x, body[index].y = pos
    return current_pos_body


def is_snake_body():
    """Проверяет произошло ли столкновение с хвостом возвращает номер тела или -1"""
    for index in range(len(body)):
        if body[index].x == box.x and body[index].y == box.y:
            return index
    return -1


def eating_body():
    global score

    index = is_snake_body()
    if index > -1:
        while len(body) > index:
            tmp = body.pop()
            play.all_sprites.remove(tmp)
            score -= 1
        display_score.words = "SCORE: %0.3d" % score


# Блок который работает один раз на старте и не повторяется
@play.when_program_starts
def do():
    """Стартовые настройки - рисуем сетку"""
    net(STEP)


# Блок который работает в цикле - т.е. постоянно повторяется
@play.repeat_forever
async def move_box():
    """Асинхронная функция - перемещает голову и хвост
        """
    current_pos = box.x, box.y
    box.move(STEP)
    eating_body()
    n = 0
    while len(body) > n:
        current_pos = body_move(n, current_pos)
        n += 1

    if SHIFT:
        await play.timer(seconds=0.01)
    else:
        await play.timer(seconds=SPEED)


@play.repeat_forever
async def time_control():
    global TIMER

    if TIMER > -1:
        minute = TIMER // 60
        seconds = TIMER % 60
        display_timer.words = "TIME: %0.2d:%0.2d" % (minute, seconds)
        TIMER -= 1
    else:
        print("GameOver")

    await play.timer(seconds=1)

# ToDo Улучшить производительность функции
def is_space_clear(x, y):
    """Проверяет по указанным координатам - занято метсто или свободно"""
    clear_space = True
    for obj in play.all_sprites:
        if obj.x == x and obj.y == y:
            clear_space = False
    return clear_space


@play.repeat_forever
async def new_apple():
    """Добавляет яблоки на экран"""
    x = play.random_number(lowest=-13, highest=26) * 30 + 5
    y = play.random_number(lowest=-17, highest=9) * 30 + 15
    while not is_space_clear(x, y):
        x = play.random_number(lowest=-12, highest=26) * 30 + 5
        y = play.random_number(lowest=-16, highest=9) * 30 + 15

    apples.append(
        play.new_image(
            image='eat.png', x=x, y=y, angle=0, size=4, transparency=100)
    )

    await play.timer(seconds=5)


@play.repeat_forever
async def eat_control():
    """Асинхронная функция - следит за касанием головы еды - и удаляет из списка
    яблок съеденное
    """
    global score

    for eat in apples:
        if eat.is_touching(box):
            score += 1
            display_score.words = "SCORE: %0.3d" % score  # обновляем значение на экране
            eat.hide()
            apples.remove(eat)
            play.all_sprites.remove(eat)
            body_append()

    await play.timer(seconds=SPEED/100)


@play.when_key_pressed('up', 'w', 'down', 's', 'right', 'd', 'left', 'a', 'enter')
async def control(key):
    global SHIFT

    if key == 'up' or key == 'w':
        box.angle = 90
    if key == 'down' or key == 's':
        box.angle = -90
    if key == 'right' or key == 'd':
        box.angle = 0
    if key == 'left' or key == 'a':
        box.angle = 180
    if key == 'enter':  # включаем ускорение
        SHIFT = 1
    else:
        SHIFT = 0

    await play.timer(seconds=0.001)

play.start_program()