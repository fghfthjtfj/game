import pygame
from govno import *  # Подключите ваши модули и классы

from threading import Thread
angle = 0
last_shot_time = pygame.time.get_ticks()
fire_cursor = pygame.image.load('models/cursors/fire.png')
fire_cursor = pygame.transform.scale(fire_cursor, (42, 42))


def control(ship, screen, camera):
    global direction, angle, last_shot_time, current_wave

    current_time = pygame.time.get_ticks()
    time_since_last_shot = current_time - last_shot_time

    key = pygame.key.get_pressed()

    if key[pygame.K_a]:
        ship.calculate_boost(-1)
        angle = 90
    elif key[pygame.K_d]:
        ship.calculate_boost(1)
        angle = 270

    if key[pygame.K_w]:
        ship.calculate_boost(0, -1)
        angle = 0
    elif key[pygame.K_s]:
        ship.calculate_boost(0, 1)
        angle = 180

    if key[pygame.K_UP] and key[pygame.K_RIGHT]:
        angle = 315
    elif key[pygame.K_DOWN] and key[pygame.K_RIGHT]:
        angle = 225
    elif key[pygame.K_DOWN] and key[pygame.K_LEFT]:
        angle = 135
    elif key[pygame.K_UP] and key[pygame.K_LEFT]:
        angle = 45
    elif key[pygame.K_k]:
        print('Название уровня')
        save_level()
    if key[pygame.K_u]:
        current_wave += 1
        print(current_wave)

    if key[pygame.K_SPACE]:
        x, y = pygame.mouse.get_pos()

        screen.blit(fire_cursor, (x - 21, y - 21))
        for cannon in ship.cannons:
            bullet = cannon.fire(ship, screen)
            if bullet is not None:
                bullet_array.append(bullet)
    #direction = angle / 45

    #return direction


#max_drag_x, max_drag_y = 0, 0


def calculate_speed(ship, coff_x=0, coff_y=0):
    try:
        ship.speed_x += coff_x * ship.thrust/ship.mass
        ship.speed_y += coff_y * ship.thrust/ship.mass
    except:
        print('Корабль уничтожен')


def ship_editor_control(drag_x, drag_y, current_size, max_drag_x, max_drag_y):
    key = pygame.key.get_pressed()

    if key[pygame.K_a]:
        drag_x += 3
    elif key[pygame.K_d]:
        drag_x -= 3

    if key[pygame.K_w]:
        drag_y += 3
    elif key[pygame.K_s]:
        drag_y -= 3
    if drag_x > 0:
        drag_x = 0
    if drag_y > 0:
        drag_y = 0
    if drag_x < max_drag_x:
        drag_x = max_drag_x
    if drag_y < max_drag_y:
        drag_y = max_drag_y

    return drag_x, drag_y


def save_and_load_ship(save_ship, load_ship_to_editor):
    key = pygame.key.get_pressed()

    if key[pygame.K_j]:
        print('Сохранение корабля')
        save_ship()
    elif key[pygame.K_h]:
        print('Загрузка корабля')
        load_ship_to_editor()
