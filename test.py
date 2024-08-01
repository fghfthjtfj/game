import time

from pygame import VIDEORESIZE, RESIZABLE, Surface, transform
from govno import *
from govno import ships_array
import ctypes
import copy
from threading import Thread, Lock
from queue import Queue

class TestClass:
    texture = None

    def __init__(self):
        self.speed = 10
        self.load_texture()

    def load_texture(self):
        load_texture = pygame.image.load('models/blocks/hull.png')
        self.texture = pygame.transform.scale(load_texture, (50, 50))


a = TestClass()


def save_ship():
    ship_name = 'ttt'

    ships_dir = 'saved_ships'
    # Проверяем, существует ли папка levels, если нет, создаем ее
    if not os.path.exists(ships_dir):
        os.makedirs(ships_dir)
    filename = os.path.join(ships_dir, f"{ship_name}.json")  # Создаем путь к файлу

    with open(filename, 'w') as json_file:

        # Создаем копии текстур перед сохранением


        json_data = jsonpickle.encode(a)
        json_file.write(json_data)
def load_ship():
    ships_dir = 'saved_ships'
    filename = os.path.join(ships_dir, "ttt.json")
    with open(filename, 'r') as json_file:
        json_data = json_file.read()
    loaded_ship = jsonpickle.decode(json_data)
    return loaded_ship

save_ship()
b = load_ship()
print(b.texture)