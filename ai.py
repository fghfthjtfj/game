import pygame.event

from govno import *

pygame.init()

max_speed = 10
max_range = 800
# Таймер стрельбы
enemy_fire_event = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_fire_event, 200)
def ai_process(ship, blue_ship, distance, screen):
    #print(distance)

    if distance < 1000 or distance == "inf":
        ship.ai = False

    if ship.ai:
        if 120 < blue_ship.blit_point_x - ship.blit_point_x < max_range and 0 < blue_ship.blit_point_y - ship.blit_point_y < max_range:
            coff_x, coff_y = 1, -1
        elif -120 > blue_ship.blit_point_x - ship.blit_point_x > -max_range and 120 < blue_ship.blit_point_y - ship.blit_point_y < max_range:
            coff_x, coff_y = 1, 1
        elif 0 > blue_ship.blit_point_x - ship.blit_point_x > -max_range and 0 > blue_ship.blit_point_y - ship.blit_point_y > -max_range:
            coff_x, coff_y = -1, 1
        elif 0 < blue_ship.blit_point_x - ship.blit_point_x < max_range and 0 > blue_ship.blit_point_y - ship.blit_point_y > -max_range:
            coff_x, coff_y = -1, -1
        else:
            diff_x = blue_ship.blit_point_x - ship.blit_point_x
            diff_y = blue_ship.blit_point_y - ship.blit_point_y
            coff_magnitude2 = math.sqrt(diff_x ** 2 + diff_y ** 2)
            if coff_magnitude2 != 0:
                coff_x = diff_x / coff_magnitude2
                coff_y = diff_y / coff_magnitude2
            else:
                coff_x, coff_y = 0, 0
        if ship.speed_x > max_speed:
            coff_x = -1
        if ship.speed_x < -max_speed:
            coff_x = 1
        if ship.speed_y > max_speed:
            coff_y = -1
        if ship.speed_y < -max_speed:
            coff_y = 1
        # Находим корень из суммы квадратов коэффициентов
        coff_magnitude = math.sqrt(coff_x**2 + coff_y**2)

        # Нормализуем коэффициенты
        try:
            coff_x /= coff_magnitude
            coff_y /= coff_magnitude
        except:
            coff_x, coff_y = 0, 0
        ship.angle = -math.degrees(math.atan2(ship.speed_x, -ship.speed_y))

        # print(coff_x**2 + coff_y**2)
        ship.calculate_boost(coff_x, coff_y)
        for cannon in ship.cannons:
            bullet = cannon.fire(ship, screen)
            if bullet is not None:
                bullet_array.append(bullet)

def check_distance(ship, player):
    x_d = ship.blit_point_x - player.blit_point_x
    y_d = ship.blit_point_y - player.blit_point_y
    dist = math.sqrt(x_d**2+y_d**2)
    if dist <= 1000:
        ship.ai = False
    return dist
