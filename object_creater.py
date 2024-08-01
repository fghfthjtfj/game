from govno import *

def create_game_objects(WIDTH, HEIGHT):
    lose_font = Writing('Поражение', WIDTH / 2, HEIGHT / 2, 2, 60)
    return lose_font

def create_main_menu_objects(WIDTH, HEIGHT):
    button_1 = ImageButton(WIDTH, HEIGHT, 50, 0, 300, 75, 'Начать игру', 'models/buttons/unselected_button.png',
                           'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    button_2 = ImageButton(WIDTH, HEIGHT, 50, 50, 300, 75, 'Выбор уровня', 'models/buttons/unselected_button.png',
                           'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    button_3 = ImageButton(WIDTH, HEIGHT, 50, 67, 300, 75, 'Ангар', 'models/buttons/unselected_button.png',
                           'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    button_4 = ImageButton(WIDTH, HEIGHT, 50, 84, 300, 75, 'Настройки', 'models/buttons/unselected_button.png',
                           'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    button_5 = ImageButton(WIDTH, HEIGHT, 50, 0, 300, 75, 'Выход', 'models/buttons/unselected_button.png',
                           'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    button_6 = ImageButton(WIDTH, HEIGHT, 50, 0, 300, 75, 'Редактор', 'models/buttons/unselected_button.png',
    'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')

    game_name = Writing('Космические казаки-рейнджеры 4', 800, 100, 1, 40)

    buttons = [button_1, button_2, button_3, button_4, button_5, button_6]
    buttons_in_list = ImageButtonList(WIDTH, HEIGHT, 15, 5, 'models/buttons/frame.png', buttons)

    return game_name, buttons, buttons_in_list


def create_main_editor_objects(WIDTH, HEIGHT):
    button_prev = ImageButton(WIDTH, HEIGHT, 2, 1, 33, 77, None, 'models/buttons/prev_page.png',
                              'models/buttons/prev_page_selected.png')
    button_save = ImageButton(WIDTH, HEIGHT, 94, 2, 60, 60, None, 'models/buttons/save.png')

    energy_bar = Energy_bar('models/garage/not_used_energy.png', 'models/garage/used_energy.png',
                            'models/garage/over_used_energy.png')
    prev_ship = ImageButton(WIDTH, HEIGHT, 4, 45, 60, 120, None, 'models/buttons/prev_page.png',
                              'models/buttons/prev_page_selected.png')
    next_ship = ImageButton(WIDTH, HEIGHT, 96, 45, 60, 120, None, 'models/buttons/next_page.png',
                              'models/buttons/next_page_selected.png')
    gun_turret = Gun_Cannon()
    laser_turret = Laser_Cannon()
    engine = Engine()
    hull = Hull()
    armor = Armor()
    reactor = Reactor()
    core = Core()

    list_parts = [gun_turret, laser_turret, engine, hull, armor, reactor, core]
    for part in list_parts:
        part.load_texture()
    buttons_ind = [button_prev, button_save, prev_ship, next_ship]

    return list_parts, buttons_ind, energy_bar


def create_settings_objects(WIDTH, HEIGHT):
    video_button_1 = ImageButton(WIDTH, HEIGHT, 50, 50, 300, 75, '1280 x 720', 'models/buttons/unselected_button.png',
                                 'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    video_button_2 = ImageButton(WIDTH, HEIGHT, 50, 67, 300, 75, '1600 x 900', 'models/buttons/unselected_button.png',
                                 'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    video_button_3 = ImageButton(WIDTH, HEIGHT, 50, 84, 300, 75, '1920 x 1080', 'models/buttons/unselected_button.png',
                                 'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    button_prev = ImageButton(WIDTH, HEIGHT, 2, 1, 33, 77, None, 'models/buttons/prev_page.png',
                              'models/buttons/prev_page_selected.png')
    video_buttons = [video_button_1, video_button_2, video_button_3]
    video_button_list = ImageButtonList(WIDTH, HEIGHT, 50, 50, 'models/buttons/frame.png', video_buttons)

    return video_buttons, video_button_list, button_prev


def create_level_selector_objects(WIDTH, HEIGHT):
    button_prev = ImageButton(WIDTH, HEIGHT, 2, 1, 33, 77, None, 'models/buttons/prev_page.png',
                              'models/buttons/prev_page_selected.png')
    level_1 = ImageButton(WIDTH, HEIGHT, 15, 60, 60, 60, None, 'models/level_menu/level_button.png',
                          'models/level_menu/level_button.png')
    start_level = ImageButton(400, HEIGHT, 12, 78, 315, 75, "Начать", 'models/buttons/unselected_button.png',
                              'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    select_level_level_1 = ImageButton(400, HEIGHT, 12, 65, 80, 75, "1", 'models/buttons/unselected_button.png',
                              'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    select_level_level_2 = ImageButton(400, HEIGHT, 41.5, 65, 80, 75, "2", 'models/buttons/unselected_button.png',
                              'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    select_level_level_3 = ImageButton(400, HEIGHT, 71, 65, 80, 75, "3", 'models/buttons/unselected_button.png',
                              'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')

    level_buttons = [level_1]
    select_level_level_buttons = [select_level_level_1, select_level_level_2, select_level_level_3]
    return level_buttons, button_prev, start_level, select_level_level_buttons

def create_level_editor_objects(WIDTH, HEIGHT):
    exit = ImageButton(WIDTH, HEIGHT, 50, 33, 300, 75, 'Завершить', 'models/buttons/unselected_button.png',
                       'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    add_goal = ImageButton(WIDTH, HEIGHT, 50, 50, 300, 75, 'Добавить цель', 'models/buttons/unselected_button.png',
                       'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    add_unit = ImageButton(WIDTH, HEIGHT, 50, 67, 300, 75, 'Добавить объект', 'models/buttons/unselected_button.png',
                           'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    remove_unit = ImageButton(WIDTH, HEIGHT, 50, 84, 300, 75, 'Удалить объект', 'models/buttons/unselected_button.png',
                           'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    buttons = [exit, add_unit, remove_unit, add_goal]
    wave_name_1 = ImageButton(WIDTH, HEIGHT, 0, 0, 50, 50, 'W1', 'models/buttons/unselected_button.png',
                           'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    wave_name_2 = ImageButton(WIDTH, HEIGHT, 0, 0, 50, 50, 'W2', 'models/buttons/unselected_button.png',
                           'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    wave_name_3 = ImageButton(WIDTH, HEIGHT, 0, 0, 50, 50, 'W3', 'models/buttons/unselected_button.png',
                           'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
    b_list_1 = [wave_name_1]
    b_list_2 = [wave_name_2]
    b_list_3 = [wave_name_3]
    b_list_list = [b_list_1, b_list_2, b_list_3]

    wave_1_list = ImageButtonList(WIDTH, HEIGHT, 4, 35, 'models/buttons/frame.png', b_list_1, 100)
    wave_2_list = ImageButtonList(WIDTH, HEIGHT, 14, 35, 'models/buttons/frame.png', b_list_2, 100)
    wave_3_list = ImageButtonList(WIDTH, HEIGHT, 24, 35, 'models/buttons/frame.png', b_list_3, 100)
    wave_list_list = [wave_1_list, wave_2_list, wave_3_list]

    map = Map((5, 5), (3000, 3000))


    return buttons, map, b_list_list, wave_list_list