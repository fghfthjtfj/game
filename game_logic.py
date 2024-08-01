# game_logic.py
import copy
from decimal import Decimal, getcontext
import pygame
import time
from govno import *
import random
import math
from threading import Thread

bullet_array = []
ships_array = []
level = Level()

current_wave = 0



#enemy_texture_path = 'models/enemy/down.png'
#player_texture_path = 'models/player_animation/move_0.png'
#turret_texture_path = 'models/turrels/platform_1.png'


#level_nummer = 1
ship_nummer = 1

# Создаем экземпляр камеры
#camera = Camera(WIDTH, HEIGHT)
#loaded_parts = []


def level_nummer_set(a):
    global level_nummer
    level_nummer = a
    print(level_nummer)


# def load_ship_from_json(ship_nummer):
#     print('Выберите корабль')
#     print(ship_nummer)
#     ship_name = ship_nummer
#
#     # Путь к папке levels
#     ships_dir = 'saved_ships'
#     filename = os.path.join(ships_dir, f"{ship_name}.json")
#     try:
#         with open(filename, 'r') as json_file:
#             json_data = json_file.read()
#             loaded_parts = jsonpickle.decode(json_data)
#
#             # Восстанавливаем текстуры из строк байтов при загрузке
#             for part in loaded_parts:
#                 part.texture = load_surface(part.texture, (part.width, part.height))
#
#             # Сортируем массив loaded_parts
#             loaded_parts.sort(key=lambda part: (isinstance(part, Core), isinstance(part, Cannon)), reverse=True)
#
#             return loaded_parts
#     except:
#         loaded_parts = []
#         return loaded_parts


# def load_surface(data, size):
#     return pygame.image.fromstring(data, size, 'RGBA')




def change_speed(ship, WIDTH, HEIGHT):
    # Выбираем случайные скорости в диапазоне -10 до 10
    ship.speed_x = random.randint(-5, 5)
    ship.speed_y = random.randint(-5, 5)

    enemy_angle = math.atan2(ship.speed_x, ship.speed_y)
    enemy_angle_degrees = math.degrees(enemy_angle)

    # Проверяем, чтобы корабль не выходил за границы экрана
    if ship.center_x < 0:
        ship.center_x = abs(ship.speed_x)
    elif ship.center_x > WIDTH:
        ship.speed_x = -abs(ship.speed_x)

    if ship.center_y < 0:
        ship.speed_y = abs(ship.speed_y)
    elif ship.center_y > HEIGHT:
        ship.speed_y = -abs(ship.speed_y)

    ship.calculate_angle(ship.speed_x*1000, ship.speed_y*1000)


def move_ship(ship):
    ship.move_ship()

    # Проверяем, чтобы корабль не выходил за границы экрана
    if ship.center_x < 0:
        ship.center_x = 0
    elif ship.center_x > WIDTH:
        ship.center_x = WIDTH - ship.center_x/2

    if ship.center_y < 0:
        ship.center_y = 0
    elif ship.center_y > HEIGHT:
        ship.center_y = HEIGHT - ship.center_y/2


#@numba.jit(fastmath=True)
def calculate_lead(x, y, object, target, result_queue, x_bullet=0, y_bullet=0):
    v_bullet = 25  # базовая скорость пули
    v_object = math.sqrt((object.speed_x ** 2) + (object.speed_y ** 2))  # скорость источника выстрела
    v_bullet += v_object  # скорость пули с учетом скорости источника выстрела
    v_target = math.sqrt((target.speed_x ** 2) + (target.speed_y ** 2))  # скорость цели
    x_target = x
    y_target = y
    d = math.sqrt((target.blit_point_x - object.blit_point_x) ** 2 + (target.blit_point_y - object.blit_point_y) ** 2)

    a = (v_target - v_object) ** 2 - v_bullet ** 2
    b = 2 * ((x_target - x_bullet) * (v_target - v_object) + (y_target - y_bullet) * (v_target - v_object))
    c = (x_target - x_bullet) ** 2 + (y_target - y_bullet) ** 2 - d ** 2
    getcontext().prec = 25

    # Преобразуем коэффициенты в Decimal
    a = Decimal(a)
    b = Decimal(b)
    c = Decimal(c)
    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        discriminant = abs(discriminant)

    root = math.sqrt(discriminant)
    root = Decimal(root)

    if a != 0:
        t1 = (-b + root) / (2 * a)
        t2 = (-b - root) / (2 * a)
        t = max(t1, t2)
    else:
        t = b + c

    delta_v_x = Decimal(target.speed_x - object.speed_x)
    delta_v_y = Decimal(target.speed_y - object.speed_y)
    delta_x = delta_v_x * t
    delta_y = delta_v_y * t

    result_queue.put((float(delta_x + Decimal(x)), float(delta_y + Decimal(y))))


def rotate_enemy_cannon(screen, dx, dy, camera, ship):
    for turret in ship.cannons:
        position = turret.calculate_part_position(ship)
        turret.rotate_cannon(screen, position, dx, dy, ship, camera)


def normalize_vector(vector):
    magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
    if magnitude != 0:
        return vector[0] / magnitude, vector[1] / magnitude
    else:
        return 0, 0


def fire(turret, assemble):
    turret.check_reloading()
    if turret.reloaded:
        speed = 25
        position = turret.calculate_part_position(assemble)
        print(position, 'pos')
        print(turret.rects[0])
        x_cord, y_cord = position

        angle_radians = math.radians(turret.angle)
        bullet_speed_x = -math.sin(angle_radians)
        bullet_speed_y = -math.cos(angle_radians)

        # Нормализуем вектор скорости пули и умножаем на speed
        bullet_speed_x, bullet_speed_y = normalize_vector((bullet_speed_x, bullet_speed_y))
        bullet_speed_x *= speed
        bullet_speed_y *= speed

        # Создаем пулю, передавая скорость
        bullet = Bullet((x_cord - assemble.speed_x, y_cord - assemble.speed_y),
                        (bullet_speed_x + assemble.speed_x, bullet_speed_y+assemble.speed_y),
                        turret.fraction, 10, copy.copy(assemble))

        bullet_array.append(bullet)

        turret.reloaded = False


def check_part_health(ship):
    for part in ship.parts:
        if part.health <= 0:
            print('блок уничтожен')
            print(len(ship.parts))
            part.destroy(ship.parts)
            connections_check(ship)
            ship.calculate_boost()


def connections_check(ship):
    ship.joins()
    ship.destroy_not_connected()


def bullet_collision(bullet, camera):
    # Проверяем столкновение пули с кораблями противоположных фракций
    for ship in ships_array:
        for part in ship.parts:
            for rect in part.rects:
                part.part_rect = rect
                # Проверяем столкновение текущего rect и переходим к следующему rect
                if part.part_rect is not None and (
                        part.part_rect.colliderect(bullet.missile)
                ) and part.fraction != bullet.fraction:
                    # Уменьшаем здоровье блока при попадании
                    #print('попадание')
                    part.decrease_health(bullet.damage)

                    bullet_array.remove(bullet)
                    #check_part_health(part, ship)
                    return  # Прерываем функцию после первого попадания


def bullet_delete(bullet_array):
    bullets_to_remove = []
    current_time = pygame.time.get_ticks()

    for i, bullet in enumerate(bullet_array):
        if current_time - bullet.creation_time > bullet.life_time:
            bullets_to_remove.append(i)

    for index in reversed(bullets_to_remove):
        bullet_array.pop(index)


def find_nearest_part(blue_ship, ship):
    min_distance = float('inf')
    nearest_part = None
    for cannon in ship.cannons:
        for target in blue_ship.parts:
            dx = target.calculate_part_position(blue_ship)[0] - cannon.calculate_part_position(ship)[0]
            dy = target.calculate_part_position(blue_ship)[1] - cannon.calculate_part_position(ship)[1]
            distance_between_parts = math.sqrt(dx**2 + dy**2)
            distance = distance_between_parts

            if distance < min_distance:
                min_distance = distance
                nearest_part = target  # Заменяем nearest_part на ближайший target

    else:
        distance = min_distance
    return nearest_part, distance

#
# def distance_between_parts(part1, part2, blue_ship, ship):
#     dx = part2.calculate_part_position(blue_ship)[0] - part1.calculate_part_position(ship)[0]
#     dy = part2.calculate_part_position(blue_ship)[1] - part1.calculate_part_position(ship)[1]
#     return math.sqrt(dx**2 + dy**2)


def part_position_get(part, assemble):
    part_cords = part.calculate_part_position(assemble)
    x = part_cords[0]
    y = part_cords[1]
    return x, y


def calculate_energy(parts):
    total_e_consume = 0
    total_e_produce = 0
    for part in parts:
        if hasattr(part, 'e_consume'):
            total_e_consume += part.e_consume
        if hasattr(part, 'e_produce'):
            total_e_produce += part.e_produce
    return total_e_produce, total_e_consume



