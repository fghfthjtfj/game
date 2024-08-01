import copy
import json
import os
import pygame
import math
import threading
import jsonpickle

lock = threading.Lock()


class Blocks:
    def __init__(self, block_type, health):
        self.fraction = None
        self.health = health
        self.part_rect = None
        self.connected = False
        self.block_type = block_type

    def get_fraction(self):
        return self.fraction

    def decrease_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            return self.health

    def destroy(self, all_parts):
        if self in all_parts:
            all_parts.remove(self)
            # ship_assembly_parts = ShipAssembly.get_parts(ShipAssembly)

    def set_fraction(self, fraction):
        self.fraction = fraction


class Sprites(Blocks):
    texture = None
    def __init__(self, texture_path, block_type, health, size):
        super().__init__(block_type, health)
        self.x_cord, self.y_cord = None, None
        self.width, self.height = size
        self.texture_path = texture_path
        #self.load_texture()

    def load_texture(self):
        load_texture = pygame.image.load(self.texture_path).convert_alpha()
        self.texture = pygame.transform.scale(load_texture, (self.width, self.height))

    def draw(self, surface, assemble, camera):
        rotated_image = pygame.transform.rotate(self.texture, assemble.angle)
        rotated_rect = rotated_image.get_rect(center=(assemble.blit_point_x, assemble.blit_point_y))
        rotated_offset = pygame.math.Vector2(self.x_cord, self.y_cord).rotate(-assemble.angle)
        part_position = rotated_rect.center + rotated_offset

        self.part_rect = rotated_image.get_rect(center=part_position)
        self.part_rect[0] -= camera.x
        self.part_rect[1] -= camera.y
        if self.block_type != 'cannon':
            self.rects = [self.part_rect]
            #pygame.draw.rect(surface, (255, 0, 0), self.part_rect, width=1)

            surface.blit(rotated_image, self.part_rect)
            # if self.fraction == 'Blue':
            #     print(camera.x)
        # else:
        # self.outer_rect = self.part_rect.inflate(60, 520)

    def calculate_part_position(self, assemble):
        # rotated_image = pygame.transform.rotate(self.texture, assemble.angle)
        rotated_rect = self.texture.get_rect(center=(assemble.blit_point_x, assemble.blit_point_y))
        rotated_offset = pygame.math.Vector2(self.x_cord, self.y_cord + self.height / 4).rotate(-assemble.angle)
        part_position = rotated_rect.center + rotated_offset
        # if self.fraction == 'Blue' and isinstance(self, Reactor):
        #     print(part_position)
        return part_position

    def just_draw(self, surface, cords, cell_wide=0, cell_height=0):
        if cords == None:
            x = self.x_cord
            y = self.y_cord
        else:
            x, y = cords
        self.part_rect = self.texture.get_rect(center=(x + self.width / 2, y + self.height / 2))
        if isinstance(self, Cannon):
            self.outer_rect = self.part_rect.inflate(50, 30)
            # print(self.part_rect)
        if self.height > cell_wide:
            self.part_rect = self.texture.get_rect(center=(x + self.width / 2, y + self.height / 2))

        surface.blit(self.texture, self.part_rect)
        self.part_rect = self.part_rect.inflate(-self.width / 4, -self.height / 4)


class Hull(Sprites):
    def __init__(self):
        self.mass = 10
        self.health = 100

        #self.part_rect = texture.get_rect()
        super().__init__('models/blocks/hull.png', 'hull', self.health, (50, 50))


class Armor(Sprites):
    def __init__(self):
        self.mass = 30
        self.health = 9999

        super().__init__('models/blocks/armor.png', 'armor', self.health, (50, 50))


class Cannon(Sprites):
    def __init__(self, texture_path, reloading, health):
        # self.mass = mass
        # self.health = 200
        # self.e_consume = 5
        self.reloading = reloading
        self.last_shot_time = 0
        self.reloaded = True
        block_type = 'cannon'
        super().__init__(texture_path, block_type, health, (50, 100))

    def rotate_cannon(self, surface, part_position, target_x, target_y, ship, camera):
        if self.fraction != 'Red':
            target_x += camera.x + ship.speed_x
            target_y += camera.y + ship.speed_y
            cor_speed_x = 0
            cor_speed_y = 0
        else:
            cor_speed_x = ship.speed_x
            cor_speed_y = ship.speed_y
        self.angle = -math.degrees(math.atan2(target_y - part_position[1] + cor_speed_y,
                                              target_x - part_position[0] + cor_speed_x)) - 90

        rotated_image = pygame.transform.rotate(self.texture, self.angle)
        rotated_image2 = pygame.transform.rotate(self.texture, 0)
        rotated_image3 = pygame.transform.rotate(self.texture, 90)

        self.part_rect = rotated_image.get_rect(center=part_position)

        self.part_rect[0] -= camera.x
        self.part_rect[1] -= camera.y

        surface.blit(rotated_image, self.part_rect)
        part_rect2 = rotated_image2.get_rect(center=part_position)
        part_rect3 = rotated_image3.get_rect(center=part_position)
        # self.part_rect = pygame.transform.rotate(self.part_rect, ship.angle)
        part_rect2[0] -= camera.x
        part_rect2[1] -= camera.y
        part_rect3[0] -= camera.x
        part_rect3[1] -= camera.y
        self.part_rect2 = part_rect2.inflate(-5, -15)
        self.part_rect3 = part_rect3.inflate(-15, -5)
        self.rects = [self.part_rect2, self.part_rect3]
        #pygame.draw.rect(surface, (0, 0, 255), self.part_rect2, width=2)
        #pygame.draw.rect(surface, (0, 0, 255), self.part_rect3, width=2)
        #pygame.draw.rect(surface, (0, 0, 255), self.part_rect, width=2)
        #self.outer_rect = pygame.draw.circle(surface, (255,0,0), (self.part_rect[0]+self.width/2, self.part_rect[1]+self.height/2), self.width, width=1)

    def check_reloading(self):
        current_time = pygame.time.get_ticks()
        time_since_last_shot = current_time - self.last_shot_time
        if time_since_last_shot >= self.reloading:
            self.reloaded = True
            self.last_shot_time = current_time


# class Laser_Cannon(Cannon):
#     damage = 0
#
#     def __init__(self, texture_path):
#         self.mass = 30
#         self.health = 200
#         self.e_consume = 5
#         self.reloading = 400
#         load_texture = pygame.image.load(texture_path).convert_alpha()
#         super().__init__((0, 0), load_texture, self.reloading, self.health)
#
#     def fire(self, assemble, screen):
#         base_vector = 750
#         # Создание вектора направления пушки
#         direction_vector = pygame.math.Vector2(0, -1).rotate(-self.angle)
#         start_point = self.rects[0].center[0], self.rects[0].center[1]
#         #self.end_point = pygame.math.Vector2(self.rects[0].center) + direction_vector * base_vector
#         end_point = pygame.math.Vector2(self.rects[0].center) + direction_vector * base_vector
#
#         # Отрисовка линии
#         #laser_line = pygame.draw.line(screen, self.fraction, start_point, self.end_point, 7)
#         # Произведение атрибута self.angle и base_vector
#
#
#         #laser_line = pygame.draw.line(screen, self.fraction, start_point, self.end_point, 7)
#         laser = Laser(start_point, end_point, self.fraction, self.damage)
#
#         return laser

    # def bullet_draw(self):
    #     pass
    #
    # def bullet_fly(self):
    #     pass
class Laser_Cannon(Cannon):
    damage = 1000
    reloading = 100

    def __init__(self):
        self.mass = 30
        self.health = 200
        self.e_consume = 5
        super().__init__('models/turrels/laser_cannon.png', self.reloading, self.health)

    def fire(self, assemble, screen):
        self.check_reloading()
        if self.reloaded:
            speed = 15
            position = self.calculate_part_position(assemble)
            x_cord, y_cord = position

            angle_radians = math.radians(self.angle)
            bullet_speed_x = -math.sin(angle_radians)
            bullet_speed_y = -math.cos(angle_radians)

            # Нормализуем вектор скорости пули и умножаем на speed
            magnitude = math.sqrt(bullet_speed_x ** 2 + bullet_speed_y ** 2)
            if magnitude != 0:
                bullet_speed_x = bullet_speed_x / magnitude
                bullet_speed_y = bullet_speed_y / magnitude
                bullet_speed_x *= speed
                bullet_speed_y *= speed
            else:
                bullet_speed_x, bullet_speed_y = 0, 0

            # Создаем пулю, передавая скорость
            bullet = Laser((x_cord - assemble.speed_x, y_cord - assemble.speed_y),
                            (bullet_speed_x + assemble.speed_x, bullet_speed_y + assemble.speed_y),
                            self.fraction, self.damage, self.angle)

            self.reloaded = False
            return bullet


class Gun_Cannon(Cannon):
    damage = 25

    def __init__(self):
        self.mass = 30
        self.health = 200
        self.e_consume = 5
        self.reloading = 400
        super().__init__('models/turrels/cannon_1.png', self.reloading, self.health)

    def fire(self, assemble, screen):
        self.check_reloading()
        if self.reloaded:
            speed = 25
            position = self.calculate_part_position(assemble)
            x_cord, y_cord = position

            angle_radians = math.radians(self.angle)
            bullet_speed_x = -math.sin(angle_radians)
            bullet_speed_y = -math.cos(angle_radians)

            # Нормализуем вектор скорости пули и умножаем на speed
            magnitude = math.sqrt(bullet_speed_x ** 2 + bullet_speed_y ** 2)
            if magnitude != 0:
                bullet_speed_x = bullet_speed_x / magnitude
                bullet_speed_y = bullet_speed_y / magnitude
                bullet_speed_x *= speed
                bullet_speed_y *= speed
            else:
                bullet_speed_x, bullet_speed_y = 0, 0

            # Создаем пулю, передавая скорость
            bullet = Bullet((x_cord - assemble.speed_x, y_cord - assemble.speed_y),
                            (bullet_speed_x + assemble.speed_x, bullet_speed_y + assemble.speed_y),
                            self.fraction, self.damage, self.angle)

            self.reloaded = False
            return bullet


class Cabin(Sprites):
    def __init__(self, texture_path, block_type, mass):
        self.mass = mass
        self.health = 400
        texture = pygame.image.load(texture_path).convert_alpha()
        #self.part_rect = texture.get_rect()
        super().__init__(texture, block_type, self.health)


class Reactor(Sprites):
    def __init__(self):
        self.mass = 40
        self.health = 150
        self.e_produce = 15
        super().__init__('models/reactors/reactor_1.png', 'reactor', self.health, (50, 50))


class Engine(Sprites):
    def __init__(self):
        self.mass = 20
        self.health = 150
        self.e_consume = 5
        self.thrust = 65
        super().__init__('models/trusters/thruster.png', 'engine', self.health, (50, 50))


class Core(Sprites):
    def __init__(self):
        self.mass = 25
        self.health = 400
        self.limit = 1
        self.connected = True
        super().__init__('models/cores/core_1.png', 'core', self.health, (50, 50))


# Класс для представления сборки корабля
class ShipAssembly:
    def __init__(self, parts, speed_x, speed_y, fraction, spawn_cords=(0, 0)):
        self.spawn_x, self.spawn_y = spawn_cords

        self.blit_point_x = self.spawn_x
        self.blit_point_y = self.spawn_y
        self.parts = parts
        self.speed_x = speed_x  # Скорость движения сборки
        self.speed_y = speed_y  # Скорость движения сборки
        self.fraction = fraction
        self.mass = 0
        self.thrust = 0
        self.center_x, self.center_y = 0, 0
        self.angle = 0
        self.ai = False
        self.cannons = []
        self.joins()
        # self.calculate_center()
        for part in self.parts:
            part.set_fraction(self.fraction)

    def calculate_center(self):
        print(len(self.parts))
        total_x, total_y = 0, 0
        for part in self.parts:
            total_x += part.x_cord
            total_y += part.y_cord
        try:
            self.center_x += total_x / len(self.parts) + self.blit_point_x
            self.center_y += total_y / len(self.parts) + self.blit_point_y
            # if self.fraction == 'Blue':
            #     self.blit_point_x = self.spawn_x
            #     self.blit_point_y = self.spawn_y
                # print(self.center_x, self.center_y)
        except:
            bebra = 1
            print(444)

    def draw(self, surface, camera):
        for part in self.parts:
            part.draw(surface, self, camera)
        #print(self.center_x, self.center_y)
        #pygame.draw.circle(surface, self.fraction, (self.center_x, self.center_y), 10)

    def update(self, width, height):
        self.blit_point_x = width / 2
        self.blit_point_y = height / 2
        self.calculate_center()

    def move(self):
        # print(self.center_x)
        # Движение по прямоугольной траектории
        if (self.blit_point_x > 3000 and self.speed_x > 0) or (self.blit_point_x < -3000 and self.speed_x < 0):
            self.speed_x = 0
        if (self.blit_point_y > 3000 and self.speed_y > 0) or (self.blit_point_y < -3000 and self.speed_y < 0):
            self.speed_y = 0
        self.blit_point_x += self.speed_x
        self.blit_point_y += self.speed_y

        # self.calculate_center()

    def check_collide(self):
        pass

    def calculate_angle(self, x, y, camera):
        self.angle = -math.degrees(math.atan2(y - self.center_y, x - self.center_x)) - 90

    # def get_center(self):
    #     return self.center_x, self.center_y

    def calculate_boost(self, coff_x=0, coff_y=0):
        self.mass = 0
        self.thrust = 0

        for part in self.parts:
            self.mass += part.mass
            if isinstance(part, Engine):
                self.thrust += part.thrust
        try:
            self.speed_x += coff_x * self.thrust / self.mass
            self.speed_y += coff_y * self.thrust / self.mass
        except:
            print('Корабль уничтожен')

    def joins(self):
        # print(self.parts)
        # print(len(self.parts))
        connected_parts = []
        self.cannons = []
        for part in self.parts:
            if isinstance(part, Cannon):
                self.cannons.append(part)
                part.connected = False
            if not isinstance(part, Core):
                part.connected = False
            else:
                connected_parts = [part]
        while True:
            num_connected_parts = len(connected_parts)

            for connected_part in connected_parts.copy():  # Используем копию, чтобы избежать изменения размера списка в цикле
                if connected_part.connected:
                    if isinstance(connected_part, Cannon):
                        continue
                    for part in self.parts:
                        scaled_rect = part.part_rect.inflate(5, 5)
                        if scaled_rect.colliderect(connected_part.part_rect) and part not in connected_parts:
                            part.connected = True
                            connected_parts.append(part)


            # Если после прохода по списку количество элементов не изменилось, выходим из цикла
            if len(connected_parts) == num_connected_parts:
                break


    def destroy_not_connected(self):
        print(self.center_x)
        # Создаем новый список, содержащий только несоединенные детали
        print(self.parts)
        parts_to_keep = []
        self.cannons = []
        for part in self.parts:
            if part.connected:
                parts_to_keep.append(part)
                if isinstance(part, Cannon):
                    self.cannons.append(part)


        # Заменяем список self.parts на новый список
        self.parts = parts_to_keep
        print(self.parts)
        # for part in self.parts:
        #     if not part.connected:
        #         self.parts.remove(part)


class Camera:
    def __init__(self, target):
        self.x = target.center_x
        self.y = target.center_y
        self.target_speed_x = target.speed_x
        self.target_speed_y = target.speed_y

    def update(self, target, width, height, cursor):
        # print(cursor.x, cursor.y)
        x = target.blit_point_x - width / 2 + cursor.coff * (cursor.x - width / 2) + target.speed_x
        y = target.blit_point_y - height / 2 + cursor.coff * (cursor.y - height / 2) + target.speed_y
        self.cursor_x = cursor.coff * (cursor.x - width / 2)
        self.cursor_y = cursor.coff * (cursor.y - height / 2)
        self.x = x
        self.y = y


class Bullet:
    def __init__(self, bullet_cords, bullet_speed, fraction, damage, angle):
        # super().__init__(bullet_cords, bullet_speed, None)
        self.x_cord, self.y_cord = bullet_cords
        self.damage = damage
        self.fraction = fraction
        self.creation_time = pygame.time.get_ticks()  # Время создания пули в миллисекундах
        self.speed_x, self.speed_y = bullet_speed
        self.life_time = 1500

    def bullet_fly(self):
        self.x_cord += self.speed_x
        self.y_cord += self.speed_y

    def bullet_draw(self, surface, camera):
        self.missile = pygame.draw.circle(surface, self.fraction, (self.x_cord - camera.x, self.y_cord - camera.y), 4)


class Laser:
    def __init__(self, bullet_cords, bullet_speed, fraction, damage, angle):
        # super().__init__(bullet_cords, bullet_speed, None)
        self.x_cord, self.y_cord = bullet_cords
        self.damage = damage
        self.fraction = fraction
        self.creation_time = pygame.time.get_ticks()  # Время создания пули в миллисекундах
        self.speed_x, self.speed_y = bullet_speed
        self.life_time = 1500
        texture = pygame.image.load('models/bullets/laser_part_blue.png')

        self.angle = angle
        # self.texture = pygame.transform.rotozoom(texture, self.angle - 90, 1)

    def bullet_fly(self):
        self.x_cord += self.speed_x
        self.y_cord += self.speed_y

    def bullet_draw(self, surface, camera):
        # self.missile = surface.blit(self.texture, (self.x_cord - camera.x, self.y_cord - camera.y))
        self.missile = pygame.draw.circle(surface, self.fraction, (self.x_cord - camera.x, self.y_cord - camera.y), 9)


class DefendTargets:
    def __init__(self):
        self.exists = False
        self.target_not_defended = False

    def target_destroyed(self):
        return self.target_not_defended

    def check_completion(self, ships_array):
        self.target_not_defended = not any(ship.fraction == 'Green' for ship in ships_array)
        if self.target_not_defended:
            return True

    def add_protectee(self, ship, ships_array):
        self.exists = True
        if ship not in ships_array:
            ships_array.append(ship)
        print(ships_array, 'add_protectee')

class AllEnemyDestroyed:
    def __init__(self):
        self.exists = False
        self.no_enemy = False
        self.current_wave = 0
        self.enemy_on_wave = []
        self.target_enemies = {}

    def check_completion(self, ships_array):
        no_enemy_on_wave = not any(ship.fraction == 'Red' for ship in ships_array)
        if no_enemy_on_wave:
            return True

    def add_enemy(self, ship, wave_key):
        self.exists = True
        if wave_key not in self.target_enemies:
            self.target_enemies[wave_key] = []
        self.target_enemies[wave_key].append(ship)

    def spawn_wave(self):
        # print(self.target_enemies.get("0"))
        self.enemy_on_wave = self.target_enemies.get(str(self.current_wave))
        self.current_wave += 1
        return self.enemy_on_wave

class PlayerDestroyed:
    def __init__(self):
        self.no_player = False
        self.exists = True

    def target_destroyed(self):
        return self.no_player

    def check_completion(self, ships_array):
        self.no_player = not any(ship.fraction == 'Blue' for ship in ships_array)
        if self.no_player:
            return True
    def add_player(self, ship, ships_array):
        if ship not in ships_array:
            ships_array.append(ship)
        # print(ships_array, 'add_player')


class Level:
    def __init__(self):
        self.goals = [PlayerDestroyed(), AllEnemyDestroyed(), DefendTargets()]
        self.current_goals = []
        self.objects = []
        self.conditions = []
        self.waves = {}

    def spawn_object(self):
        try:
            print('Номер объекта')
            object_nummer = input()
            print('Фракция')
            fraction = input()
            print('Координаты объекта')
            print('x')
            x = int(input())
            print('y')
            y = int(input())
            parts2 = load_ship_from_json(object_nummer)
            print(parts2)
            avg_x = sum(part.x_cord for part in parts2) / len(parts2)
            avg_y = sum(part.y_cord for part in parts2) / len(parts2)
            for part in parts2:
                part.x_cord -= avg_x
                part.y_cord -= avg_y
            # x, y = pygame.mouse.get_pos()
            ship_assembly2 = ShipAssembly(parts2, 0, 0, fraction, (x, y))  # Например, для центра экрана

            # self.objects.append(ship_assembly2)
            return ship_assembly2
        except:
            return None

    def remove_object(self, wave_number, index):
        self.waves[wave_number].pop(index)

    def add_ship_to_wave(self, ship, wave_number):
        if wave_number not in self.waves:
            self.waves[wave_number] = []  # Создаем список кораблей для новой волны
        self.waves[wave_number].append(ship)  # Добавляем корабль к указанной волне
        print(self.waves)

    def save_level(self):
        level_name = input()
        levels_dir = 'levels'

        if not os.path.exists(levels_dir):
            os.makedirs(levels_dir)
        filename = os.path.join(levels_dir, f"{level_name}.json")

        level_data = {
            "goals": self.goals,
            "waves": self.waves
        }

        with open(filename, 'w') as json_file:


            json_data = jsonpickle.encode(level_data)
            json_file.write(json_data)

    def load_level_from_json(self, level_name, ship_nummer, ships_array):
        levels_dir = 'levels'
        print(level_name)
        filename = os.path.join(levels_dir, f"{level_name}.json")

        with open(filename, 'r') as json_file:
            json_data = json_file.read()
            level_data = jsonpickle.decode(json_data)
            for wave_key, loaded_waves in level_data.get("waves", {}).items():
                #print(f"Wave: {wave_key}")
                #print(loaded_waves)
                for ship in loaded_waves:
                    if ship.fraction == 'Green':
                        self.goals[2].add_protectee(ship, ships_array)

                    if ship.fraction == 'Red':
                        print('enemy')
                        self.goals[1].add_enemy(ship, wave_key)
                        ships_array.append(ship)
                    if ship.fraction == 'Blue':
                        # self.goals[0].add_player(ship)
                        pass
            parts2 = load_ship_from_json(ship_nummer)
            avg_x = sum(part.x_cord for part in parts2) / len(parts2)
            avg_y = sum(part.y_cord for part in parts2) / len(parts2)
            for part in parts2:
                part.x_cord -= avg_x
                part.y_cord -= avg_y
            player_ship = ShipAssembly(parts2, 0, 0, 'Blue')
            # self.objects.append(ship)
            self.goals[0].add_player(player_ship, ships_array)

            # print(ships_array)

    # def check_conditions(self, ships_array, current_wave, wave_end=False):
    #     for goal in self.current_goals:
    #         if isinstance(goal, PlayerDestroyed):
    #             pass
    #         if isinstance(goal, DefendTargets):
    #             goal.check_completion()
    #     if len(ships_array) == 1:
    #         current_wave += 1
    #         wave_end = True
    #     else:
    #         wave_end = False
    #     return wave_end, current_wave

    def add_conditions(self, wave_nummer):
        target_type = int(input())
        if target_type == 1:
            pass

    def level_execute(self, current_wave):
        # protectee_targets = self.level_data.get('goals', {}).get('targets', [])
        pass

    def level_goals_apply(self):
        for goal in self.goals:
            if isinstance(goal, PlayerDestroyed):
                if goal.exists:
                    self.current_goals.append(goal)
            if isinstance(goal, DefendTargets):
                if goal.exists:
                    self.current_goals.append(goal)
            if isinstance(goal, AllEnemyDestroyed):
                if goal.exists:
                    self.current_goals.append(goal)


def load_ship_from_json(ship_nummer):
    print(123)
    # print('Выберите корабль')
    # print(ship_nummer)
    ship_name = ship_nummer

    # Путь к папке levels
    ships_dir = 'saved_ships'
    filename = os.path.join(ships_dir, f"{ship_name}.json")
    try:
        with open(filename, 'r') as json_file:
            json_data = json_file.read()
            loaded_parts = jsonpickle.decode(json_data)

            # Восстанавливаем текстуры из строк байтов при загрузке


            # Сортируем массив loaded_parts
            loaded_parts.sort(key=lambda part: (isinstance(part, Core), isinstance(part, Cannon)), reverse=True)

            return loaded_parts
    except:
        loaded_parts = []
        return loaded_parts


def load_surface(data, size):
    return pygame.image.fromstring(data, size, 'RGBA')
