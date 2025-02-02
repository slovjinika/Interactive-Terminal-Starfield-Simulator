import time
import random
import os
import sys
import math

# Настройки
WIDTH = 80
HEIGHT = 25
STAR_DENSITY = 0.03
MAX_STAR_SPEED = 0.2
STAR_CHARS = ['·', '*', '+']
ACCELERATION_RATE = 0.2  #скорость изменения
MIN_SPEED_LIMIT = 0.01
MAX_SPEED_LIMIT = 1000


# Функция для очистки экрана
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_star_field():
    stars = []
    for _ in range(int(WIDTH * HEIGHT * STAR_DENSITY)):
        stars.append({
            "x": random.randint(0, WIDTH - 1),
            "y": random.randint(0, HEIGHT - 1),
            "char": random.choice(STAR_CHARS),
            "speed": random.random() * MAX_STAR_SPEED,
            "angle": random.uniform(0, 2 * math.pi)
        })
    return stars


# Инициализация звезд
stars = create_star_field()

# Функция для неблокирующего ввода
def get_key():
    if os.name == 'nt':
        import msvcrt
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8')
        else:
            return None
    else:
        import termios, fcntl
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
        try:
            try:
                c = sys.stdin.read(1)
            except IOError:
                c = None
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        return c

# Основной цикл игры
try:
    while True:
        clear_screen()

        # Создаем пустой экран
        screen = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

        # Обновляем положение звезд и отрисовываем их
        for star in stars:
            # Обновляем позицию
            star['x'] += star['speed'] * math.cos(star['angle'])
            star['y'] += star['speed'] * math.sin(star['angle'])

            # Проверяем границы и переносим звезду на противоположную сторону
            if star['x'] < 0:
                star['x'] = WIDTH - 1
            if star['x'] >= WIDTH:
                star['x'] = 0
            if star['y'] < 0:
                star['y'] = HEIGHT - 1
            if star['y'] >= HEIGHT:
                star['y'] = 0

            # Отрисовываем звезду, если она в пределах экрана
            x = int(star['x'])
            y = int(star['y'])
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                screen[y][x] = star['char']

        # Выводим экран
        for row in screen:
            print(''.join(row))

        # Обработка ввода
        key = get_key()
        if key == 'w':
           MAX_STAR_SPEED += ACCELERATION_RATE
           MAX_STAR_SPEED = min(MAX_STAR_SPEED, MAX_SPEED_LIMIT)
        elif key == 's':
            MAX_STAR_SPEED -= ACCELERATION_RATE
            MAX_STAR_SPEED = max(MAX_STAR_SPEED, MIN_SPEED_LIMIT)


        sleep_time = 1 / (MAX_STAR_SPEED * 2)
        time.sleep(sleep_time)  # Задержка для плавного движения
except KeyboardInterrupt:
    print("Выход из симуляции...")
    sys.exit(0)
