import pygame
import random


clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1132, 744))
pygame.display.set_caption('Game')

ship_speed_x = 0
ship_speed_y = 0
ship_x = 500
ship_y = 650
direction = 0

bullet_speed_x = 0
bullet_speed_y = 0

ally_bullet_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ally_bullet_timer, 500)
ally_bullet_array = []


enemy_x = 500
enemy_y = 200
enemy_speed_x = 0
enemy_speed_y = 0
enemy_movement_timer = 0

enemy_bullet_speed_x = 0
enemy_bullet_speed_y = 7
enemy_bullet_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_bullet_timer, 1000)
bullet_array = []

bg = pygame.image.load('models/backgound_space1.jpeg')
enemy = pygame.image.load('models/enemy/down.png')

player = [pygame.image.load(f'models/player_animation/move_{direction}.png') for direction in range(8)]


running = True
allive = True
while running:
    screen.blit(bg, (0, 0))
    screen.blit(enemy, (enemy_x, enemy_y))
    enemy_box = enemy.get_rect(topleft=(enemy_x, enemy_y))

    screen.blit(player[direction], (ship_x, ship_y))
    player_box = player[direction].get_rect(topleft=(ship_x, ship_y))

    if allive:
        if enemy_movement_timer > 0:
            enemy_movement_timer -= 1
        else:
            enemy_speed_x = random.randint(-10, 10)
            enemy_speed_y = random.randint(-10, 10)
            enemy_movement_timer = random.randint(10, 40)
        if 0 < enemy_x < 1064:
            enemy_x += enemy_speed_x
        else:
            enemy_speed_x = -enemy_speed_x
            enemy_x += enemy_speed_x

        if 0 < enemy_y < 688:
            enemy_y += enemy_speed_y
        else:
            enemy_speed_y = -enemy_speed_y
            enemy_y += enemy_speed_y

        bullets_to_remove = []

        for i, bullet in enumerate(bullet_array):
            bullet['x'] += enemy_bullet_speed_x
            bullet['y'] += enemy_bullet_speed_y
            pygame.draw.circle(screen, 'Red', (bullet['x'], bullet['y']), 7)

            if player_box.colliderect(bullet['x'], bullet['y'], 14, 14):
                print("Подбитие!")
                allive = False

            if bullet['x'] < -10 or bullet['y'] > 760:
                bullets_to_remove.append(i)

        # Удаление пуль после завершения цикла
        for index in reversed(bullets_to_remove):
            bullet_array.pop(index)

        ship_x += ship_speed_x
        ship_y += ship_speed_y
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            ship_speed_x -= 1
            direction = 6
        elif key[pygame.K_RIGHT]:
            ship_speed_x += 1
            direction = 2

        if key[pygame.K_UP]:
            ship_speed_y -= 1
            direction = 0
        elif key[pygame.K_DOWN]:
            ship_speed_y += 1
            direction = 4

        if key[pygame.K_UP] and key[pygame.K_RIGHT]:
            direction = 1
        elif key[pygame.K_DOWN] and key[pygame.K_RIGHT]:
            direction = 3
        elif key[pygame.K_DOWN] and key[pygame.K_LEFT]:
            direction = 5
        elif key[pygame.K_UP] and key[pygame.K_LEFT]:
            direction = 7

        elif key[pygame.K_c]:
            ship_x = 580
            ship_y = 350

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == enemy_bullet_timer:
                bullet_array.append({'x': enemy_x + 30, 'y': enemy_y + 85})
            # Определение скорости пули на основе направления корабля
            direction_to_bullet_speed = {
                0: (0, -7),  # Вверх
                1: (7, -7),  # Вправо и вверх
                2: (7, 0),  # Вправо
                3: (7, 7),  # Вправо и вниз
                4: (0, 7),  # Вниз
                5: (-7, 7),  # Влево и вниз
                6: (-7, 0),  # Влево
                7: (-7, -7)  # Влево и вверх
            }

            if event.type == ally_bullet_timer and key[pygame.K_SPACE]:
                # Определение скорости пули на основе направления корабля
                bullet_speed_x, bullet_speed_y = direction_to_bullet_speed.get(direction, (0, 0))

                # Добавление пули
                ally_bullet_array.append({'x': ship_x, 'y': ship_y, 'speed_x': bullet_speed_x, 'speed_y': bullet_speed_y})

        # Создайте временный список для хранения индексов пуль, которые нужно удалить
        bullets_to_remove = []

        # Обработка пуль союзника
        for i, ally_bullet in enumerate(ally_bullet_array):
            ally_bullet['x'] += ally_bullet['speed_x']
            ally_bullet['y'] += ally_bullet['speed_y']
            pygame.draw.circle(screen, 'Blue', (ally_bullet['x'] + 32, ally_bullet['y'] + 34), 7)

            if enemy_box.colliderect(ally_bullet['x'], ally_bullet['y'], 14, 14):
                print("Попадание!")

            if ally_bullet['x'] < -10 or ally_bullet['y'] > 760:
                # Добавьте индекс пули в список для последующего удаления
                bullets_to_remove.append(i)

        # Удаление пуль после завершения цикла
        for index in reversed(bullets_to_remove):
            ally_bullet_array.pop(index)

    else:
        screen.fill((89, 89, 89))
    pygame.display.update()
    clock.tick(25)