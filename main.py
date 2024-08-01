import time

from pygame import VIDEORESIZE, RESIZABLE, Surface, transform
from govno import *
from govno import ships_array
import ctypes
import copy
from threading import Thread, Lock
from queue import Queue


blue_ship = None
ctypes.windll.user32.SetProcessDPIAware()
WIDTH = 1280
HEIGHT = 720

pygame.init()
clock = pygame.time.Clock()
ships_array_lock = threading.Lock()

true_screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = Surface((WIDTH, HEIGHT))
current_size = WIDTH, HEIGHT
scaled_screen = transform.scale(screen, current_size)

pygame.display.set_caption('Космические казаки-рейнджеры 4')
part_selected = False

bg_load = pygame.image.load('models/backs/level_1.png').convert()
bg = pygame.transform.scale(bg_load, (WIDTH, HEIGHT))
menu_screen_load = pygame.image.load('models/backs/menu_screen.png')
menu_screen = pygame.transform.scale(menu_screen_load, (WIDTH, HEIGHT)).convert()
ship_yard_load = pygame.image.load('models/backs/ship_yard.png').convert()
ship_yard = pygame.transform.scale(ship_yard_load, (WIDTH, HEIGHT))
level_select_screen_load = pygame.image.load('models/backs/level_select_1.png').convert()
level_select_screen = pygame.transform.scale(level_select_screen_load, (WIDTH, HEIGHT))
level_info_load = pygame.image.load('models/backs/level_info.png').convert()
level_info = pygame.transform.scale(level_info_load, (400, HEIGHT))
level_info_tab_load = pygame.image.load('models/level_menu/level_info_tab.png').convert_alpha()
level_info_tab = pygame.transform.scale(level_info_tab_load, (350, 300))

cursor = pygame.image.load('models/cursors/menu_cursor.png').convert_alpha()
cursor = pygame.transform.scale(cursor, (30, 35))
target_cursor = pygame.image.load('models/cursors/targeter.png').convert_alpha()
target_cursor = pygame.transform.scale(target_cursor, (42, 42))
fire_cursor.convert_alpha()
pygame.mouse.set_visible(False)


limit_font_blit = pygame.USEREVENT + 3

level_nummer = 1
font = pygame.font.Font(None, 36)

def main_menu():
    global current_size
    game_name, buttons, buttons_in_list = create_main_menu_objects(WIDTH, HEIGHT)
    # Остальной код
    running = True
    drag_x, drag_y = 0, 0
    # Основной игровой цикл
    while running:
        def environment_processing_menu():
            screen.blit(menu_screen, (0, 0))
        t_menu_screen = Thread(target=environment_processing_menu())
        t_menu_screen.start()
        mouse = pygame.mouse.get_pos()
        game_name.write(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.MOUSEBUTTONUP and buttons[4].button_rect.collidepoint(mouse)):
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if buttons[0].button_rect.collidepoint(mouse) and event.button == 1:
                    #compare_ship(WIDTH, HEIGHT)
                    start_game()
                if buttons[1].button_rect.collidepoint(mouse) and event.button == 1:
                    fade()
                    level_select()
                if buttons[2].button_rect.collidepoint(mouse) and event.button == 1:
                    # fade()
                    ship_editor()
                if buttons[3].button_rect.collidepoint(mouse) and event.button == 1:
                    settings()
                if buttons[5].button_rect.collidepoint(mouse) and event.button == 1:
                    level_editor()

            if event.type == VIDEORESIZE:
                current_size = event.size

            for button in buttons:
                button.handle_event(event)
        buttons_in_list.set_pos(WIDTH, HEIGHT)

        buttons_in_list.draw(screen)
        for button in buttons:
            button.check_hover(mouse)

        screen.blit(cursor, (mouse[0]-3, mouse[1]-3))
        scaled_screen = transform.scale(screen, current_size)
        true_screen.blit(scaled_screen, (drag_x, drag_y))
        pygame.display.update()


def level_editor():
    global current_size
    ships_array.clear()
    selected_wave = 0
    ships_array_editor = []
    running = True

    buttons, map, b_list_list, wave_list_list = create_level_editor_objects(WIDTH, HEIGHT)

    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill('Black')
        for w_list in wave_list_list:
            w_list.draw(screen)

        for button in buttons:
            button.draw(screen)
            button.check_hover(mouse)
        for wave_col in wave_list_list:
            for button in wave_col.buttons:
                button.check_hover(mouse)
        map.update(screen, ships_array_editor)
        #print((mouse[0] - 15 - 85)*35, (mouse[1] - 15 - 85)*35)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                if buttons[1].button_rect.collidepoint(mouse) and event.button == 1:
                    craft = level.spawn_object()
                    if craft is not None:
                        new_ship_index = len(ships_array_editor)+1
                        new_ship_button = ImageButton(WIDTH, HEIGHT, 0, 0, 50, 50, str(new_ship_index),
                                                      'models/buttons/unselected_button.png',
                                                      'models/buttons/selected_button.png', 'sounds/effects/big_button.mp3')
                        # Добавляем новый объект ImageButton в список кнопок
                        b_list_list[selected_wave].append(new_ship_button)
                        wave_list_list[selected_wave].reset_len()
                        level.add_ship_to_wave(craft, selected_wave)
                        ships_array_editor.append(craft)
                if buttons[2].button_rect.collidepoint(mouse) and event.button == 1:
                    print('Укажите номер объекта')
                    ship_to_remove = int(input())-1
                    b_list_list[ship_to_remove].pop()
                    level.remove_object(selected_wave, ship_to_remove)
                    ships_array_editor.pop(ship_to_remove)
                    for wave_col in wave_list_list:
                        wave_col.reset_len()

                if buttons[0].button_rect.collidepoint(mouse) and event.button == 1:
                    level.save_level()
                    running = False
                for index, wave_col in enumerate(wave_list_list):
                    for button in wave_col.buttons:
                        if button.button_rect.collidepoint(mouse) and event.button == 1:
                            selected_wave = index
                            print(f"Выбрана волна: {selected_wave}")

        screen.blit(cursor, (mouse[0]-3, mouse[1]-3))
        scaled_screen = transform.scale(screen, current_size)
        true_screen.blit(scaled_screen, (0, 0))
        pygame.display.update()


def level_select():
    global current_size, level_nummer
    level_buttons, prev_button, start_level_button, select_level_level_buttons = create_level_selector_objects(WIDTH, HEIGHT)
    running = True
    level_selected = False
    click_on_level = False
    while running:
        mouse = pygame.mouse.get_pos()

        def environment_processing_level():
            screen.blit(level_select_screen, (0, 0))

        t_level_screen = Thread(target=environment_processing_level)
        t_level_screen.start()
        if level_selected:
            screen.blit(level_info, (WIDTH-400, 0))
            start_level_button.draw(level_info, True)
            start_level_button.check_hover(mouse, -(WIDTH - 400))
            level_info.blit(level_info_tab, (30, 60))
            for button in select_level_level_buttons:
                button.draw(level_info)
                button.check_hover(mouse, -(WIDTH - 400))
       # print(start_level_button)

        prev_button.draw(screen)
        prev_button.check_hover(mouse)
        for button in level_buttons:
            button.draw(screen)
            button.check_hover(mouse)

        for event in pygame.event.get():
            if start_level_button.handle_event(event):
                start_game()
            if level_selected:
                for index in range(len(select_level_level_buttons)):
                    if select_level_level_buttons[index].handle_event(event):
                        level_nummer = (index+1)
                        click_on_level = True

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if level_buttons[0].button_rect.collidepoint(mouse) and event.button == 1:
                    level_selected = True
                elif prev_button.button_rect.collidepoint(mouse) and event.button == 1:
                    #fade()
                    running = False
                elif not click_on_level:
                    level_selected = False
                click_on_level = False
            for button in level_buttons:
                button.handle_event(event)
            prev_button.handle_event(event)
        screen.blit(cursor, (mouse[0] - 3, mouse[1] - 3))
        #print(current_size)

        scaled_screen = transform.scale(screen, current_size)
        true_screen.blit(scaled_screen, (0, 0))
        pygame.display.update()
        clock.tick(60)

lose_font = create_game_objects(WIDTH, HEIGHT)
def start_game():

    global blue_ship, current_size, ship_nummer, level_nummer
    level = Level()

    level.load_level_from_json(level_nummer, 2, ships_array)
    level.level_goals_apply()
#    ships_array.append(level.goals[0].player)

    threads = []

    queue_array = Queue()
    camera = Camera(ships_array[0])
    cursor_class = Cursor()
    drag_x, drag_y = 0, 0
    running = True
    # level_end_win = False
    # level_end_lose = False
    map = Map((5, 5), (3000, 3000))
    max_drag_x, max_drag_y = 0, 0
    for ship in ships_array:
        print(ship.parts)
        for part in ship.parts:
            part.load_texture()
        if ship.fraction == 'Blue':
            blue_ship = ship
            ship.update(WIDTH, HEIGHT)
        ship.draw(screen, camera)

    while running:


        def camera_processing():
            cursor_class.update()
            camera.update(blue_ship, WIDTH, HEIGHT, cursor_class)
        t_camera = Thread(target=camera_processing, args=())
        t_camera.start()
        x, y = pygame.mouse.get_pos()

        def environment_processing():
            screen.blit(bg, (0, 0))
        t_environment = Thread(target=environment_processing, args=())
        t_environment.start()

        def ship_processing(craft):
            global blue_ship
            if len(craft.parts) == 0:
                ships_array.remove(craft)
                # if craft.fraction == 'Red':
                #     level.goals[1].enemy_on_wave.remove(craft)
               # if craft.fraction == 'Green':
                    #pass
                    #allived_protectee.remove(craft)
            x, y = pygame.mouse.get_pos()

            craft.move()
            craft.draw(screen, camera)
            #start = time.time()

            check_part_health(craft)
            #end = time.time()
            #print(end * 100 - start * 100)
            if craft.fraction == 'Blue':
                craft.calculate_angle(x, y, camera)
                t_control = Thread(target=control(craft, screen, camera))
                t_control.start()
                for part in craft.cannons:
                    if isinstance(part, Cannon):
                        position = part.calculate_part_position(craft)
                        part.rotate_cannon(screen, position, x, y, craft, camera)
            elif craft.fraction == 'Red':
                if blue_ship is None:
                    rotate_enemy_cannon(screen, 0, 0, camera, craft)
                else:
                    if not ship.ai:
                        check_distance(craft, blue_ship)
                        rotate_enemy_cannon(screen, 0, 0, camera, craft)

                    else:

                        nearest_part, distance = find_nearest_part(blue_ship, craft)  # Используем blue_ship.parts
                        ai_process(craft, blue_ship, distance, screen)
                        # blue_ship.blit_point_x, blue_ship.blit_point_y
                        if nearest_part is not None:
                            x, y = nearest_part.calculate_part_position(blue_ship)
                        else:
                            x, y = 0, 0
                        calculate_lead(x, y, craft, blue_ship, queue_array)
                        t2 = Thread(target=calculate_lead, args=(x, y, craft, blue_ship, queue_array))
                        t2.start()
                        dx, dy = queue_array.get()
                        rotate_enemy_cannon(screen, dx, dy, camera, craft)

            elif craft.fraction == 'Green':
                rotate_enemy_cannon(screen, 0, 0, camera, craft)

        if not any(ship.fraction == 'Blue' for ship in ships_array):
            blue_ship = ships_array[-1]

        for ship in ships_array:
            #print(ship.fraction)
            t_ships = Thread(target=ship_processing, args=(ship,))
            t_ships.start()
            t_ships.join()
            #threads.append(t_ships)

        # for thread in threads:
        #     thread.join()
        def level_processing():
            nonlocal running
            level_end_win_l = False
            level_end_lose_l = False
            if level.goals[1].no_enemy:
                level_end_win_l = True
            if level.goals[1].check_completion(ships_array):
                print('нет врагов')
                new_enemies = level.goals[1].spawn_wave()
                if new_enemies is not None:
                    for enemy in new_enemies:
                        ships_array.append(enemy)
                else:
                    level.goals[1].no_enemy = True
            if level.goals[0].check_completion(ships_array):
                level_end_lose_l = True

            if level.goals[2].check_completion(ships_array):
                level_end_lose_l = True
            # проверка окончания уровня
            if level_end_win_l:
                # print('Победа')
                running = False
                ships_array.clear()
                bullet_array.clear()
            if level_end_lose_l:
                # print('Поражение')
                lose_font.write(screen)

        t_level = Thread(target=level_processing, args=())
        t_level.start()


        def bullets_processing(screen, camera):
            for bullet in bullet_array:
                bullet.bullet_draw(screen, camera)
                bullet_collision(bullet, camera)
                bullet.bullet_fly()
            bullet_delete(bullet_array)

        t_bullets = Thread(target=bullets_processing, args=(screen, camera))
        t_bullets.start()
        fps = clock.get_fps()
        fps_text = font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
        screen.blit(fps_text, (300, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade()
                    current_size = WIDTH, HEIGHT
                    drag_x, drag_y = 0, 0
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if event.button == 4:  # Колесо вверх
                    # Масштабирование вверх
                    scale_factor = 1.05
                elif event.button == 5 and current_size[0] > 1280:  # Колесо вниз
                    # Масштабирование вниз
                    scale_factor = 1 / 1.05
                else:
                    scale_factor = 1

                    # Получение координат курсора относительно поверхности (surface)
                rel_x = x - drag_x
                rel_y = y - drag_y

                # Масштабирование размера окна
                current_size = tuple(int(x * scale_factor) for x in current_size)

                # Пересчет смещения
                drag_x = x - rel_x * scale_factor
                drag_y = y - rel_y * scale_factor
                # print(drag_x, drag_y)
                if drag_x > 0:
                    drag_x = 0
                if drag_y > 0:
                    drag_y = 0
                # Определение максимальных значений смещения
                if current_size[0] > WIDTH:
                    max_drag_x = -(current_size[0] - WIDTH)
                if current_size[1] > HEIGHT:
                    max_drag_y = -(current_size[1] - HEIGHT)
                if drag_x < max_drag_x:
                    drag_x = max_drag_x
                if drag_y < max_drag_y:
                    drag_y = max_drag_y

            if current_size[0] < WIDTH:
                drag_x, drag_y = 0, 0
                current_size = WIDTH, HEIGHT

            if event.type == VIDEORESIZE:
                current_size = event.size

        mouse = pygame.mouse.get_pos()
        screen.blit(target_cursor, (mouse[0]-21, mouse[1]-21))
        scaled_screen = transform.scale(screen, current_size)
        #print(current_size)
        true_screen.blit(scaled_screen, (drag_x, drag_y))
        map.update(true_screen, ships_array)
        pygame.display.update()
        clock.tick(60)


def ship_editor():
    global part_selected, current_size

    def handle_mouse_click():
        global part_selected
        x, y = pygame.mouse.get_pos()
        x = (x - drag_x) * (scale)
        y = (y - drag_y) * (scale)
        part_on_page = part_cells.parts_on_page
        for part in part_on_page:
            if part.part_rect.collidepoint(blit_x, blit_y) and not part_selected:
                index = list_parts.index(part)
                selected_parts.append(list_parts2[index])
                part_selected = True
                break

        else:
            if part_selected:
                for selected_part in selected_parts:
                    selected_part.x_cord, selected_part.y_cord = grid.snap_to_grid(x, y, selected_part)
                    sent_back_to_list_parts = False

                    for part in part_on_page:
                        mouse2 = pygame.mouse.get_pos()
                        if part.part_rect.collidepoint(mouse2):
                            sent_back_to_list_parts = True
                            break
                    if not sent_back_to_list_parts:
                        allow_placement = check_placement(selected_part)
                        allow_placement2 = limits_check()
                        if allow_placement and allow_placement2:
                            if selected_parts[0].width < grid.cell_width:
                                selected_parts[0].x_cord += 0
                                placed_parts.append(copy.copy(selected_part))
                            else:
                                print(selected_part.x_cord, selected_part.y_cord)

                                placed_parts.append(copy.copy(selected_part))
                selected_parts.clear()
                part_selected = False

    def draw_selected_part(x, y, scale):
        x = (x - drag_x) * (scale)
        y = (y - drag_y) * (scale)
        for part in selected_parts:
            part.just_draw(screen, (x - part.width / 2, y - part.height / 2))
            #part.just_draw(screen, (x - part.width / 2, y - part.height / 2))

    def replace_part(x, y):
        global part_selected, replace_timer
        #placed_parts.reverse()
        x = (x - drag_x) * (scale)
        y = (y - drag_y) * (scale)
        for part in reversed(placed_parts):
            if isinstance(part, Cannon):
                if part.outer_rect.collidepoint(x, y):
                    if not selected_parts:
                        selected_parts.append(copy.copy(part))
                        placed_parts.remove(part)
                        part_selected = True
                        replace_timer = pygame.time.get_ticks()  # Обновляем таймер
                    else:
                        break
            else:
                if part.part_rect.collidepoint(x, y):
                    if not selected_parts:
                        selected_parts.append(copy.copy(part))
                        placed_parts.remove(part)
                        part_selected = True
                        replace_timer = pygame.time.get_ticks()  # Обновляем таймер
                    else:
                        break

    def check_placement(upper_part):
        print('Начало проверки')
        x, y = pygame.mouse.get_pos()
        x = (x - drag_x) * (scale)
        y = (y - drag_y) * (scale)
        for lower_part in placed_parts:
            if upper_part.part_rect.colliderect(lower_part.part_rect) and lower_part.part_rect.collidepoint(x, y):
                print('Наложение')

                if isinstance(lower_part, Hull) and isinstance(upper_part, Cannon):
                    for another_part in placed_parts:
                        if another_part != lower_part and isinstance(another_part,
                                                                     Cannon) and another_part.outer_rect.colliderect(
                                lower_part.part_rect):
                            print('Уже есть пушка на этом корпусе')
                            return False
                    print('Поставил пушку на корпус')
                    return True
                else:
                    print('Наложение частей')
                    return False
        if isinstance(upper_part, Cannon):
            print('Неверное размещение')
            return False
        print('Без наложений')
        return True

    def limits_check():
        global overlimit_font
        count = 1
        for part in placed_parts:
            if part.block_type == selected_parts[0].block_type:
                if hasattr(part, 'limit'):
                    count += 1
                    if count > part.limit:
                        overlimit_font = Writing(f"Лимит детали: {part.limit}",
                                                 x, y, 2, 20, 150)
                        overlimit_font_array.append(overlimit_font)

                        return False
                    else:
                        continue
                else:
                    continue
            else:
                print('продолжить')
                continue
        return True

    def save_ship():
        ship_name = input()

        ships_dir = 'saved_ships'
        # Проверяем, существует ли папка levels, если нет, создаем ее
        if not os.path.exists(ships_dir):
            os.makedirs(ships_dir)
        filename = os.path.join(ships_dir, f"{ship_name}.json")  # Создаем путь к файлу

        with open(filename, 'w') as json_file:

            # Создаем копии текстур перед сохранением
            saved_parts = []

            # Вычисляем средние значения x_cord и y_cord
            # avg_x = sum(part.x_cord for part in placed_parts) / len(placed_parts)
            # avg_y = sum(part.y_cord for part in placed_parts) / len(placed_parts)

            for part in placed_parts:
                if isinstance(part, Core):
                    part.connected = True


            json_data = jsonpickle.encode(placed_parts)
            json_file.write(json_data)

    def save_surface(surface):
        return pygame.image.tostring(surface, 'RGBA')

    def load_ship_to_editor(ship_nummer=2):
        placed_parts.clear()
        for part in load_ship_from_json(ship_nummer):
            placed_parts.append(part)
            part.load_texture()
    clock = pygame.time.Clock()

    list_parts, buttons_ind, energy_bar = create_main_editor_objects(WIDTH, HEIGHT)

    list_parts2 = []
    placed_parts = []  # Массив для хранения размещённых деталей
    selected_parts = []
    overlimit_font_array = []

    part_cells = CellsForPartList(WIDTH, HEIGHT, 50, 85, list_parts)
    grid = Grid(50, 50, 7, 7)

    for part in list_parts:
        part_list = copy.copy(part)
        list_parts2.append(part_list)

    drag_x, drag_y = 0, 0
    start_time = 0
    max_drag_x = 0
    max_drag_y = 0
    overlimit_font = None

    running = True
    mouse_pressed = False
    global ship_nummer
    load_ship_to_editor()
    while running:
        screen.blit(ship_yard, (0, 0))
        part_cells.draw(true_screen, WIDTH)
        grid.draw(screen, WIDTH, HEIGHT)
        scale = WIDTH/current_size[0]
        x, y = pygame.mouse.get_pos()
        blit_x, blit_y = x, y
        save_and_load_ship(save_ship, load_ship_to_editor)
        #print(x, y)

        for part in placed_parts:
            if not isinstance(part, Cannon):
                part.just_draw(screen, None, 100)

        for part in placed_parts:
            if isinstance(part, Cannon):
                part.just_draw(screen, None, 100)
        for font in overlimit_font_array:
            if font.blit_time > 0:
                font.write(screen)
            else:
                overlimit_font_array.remove(font)
        if part_selected:
            draw_selected_part(x, y, scale)
        energy = calculate_energy(placed_parts)
        energy_bar.set_pos(WIDTH, HEIGHT)
        energy_bar.scale_bar(true_screen, energy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #if event.type == limit_font_blit and overlimit_font is not None:
                #overlimit_font.write()

                    # Назад в меню
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True

                start_time = pygame.time.get_ticks()
                if event.button == 1:

                    # Назад в меню
                    if buttons_ind[0].button_rect.collidepoint(x, y):
                        fade()
                        current_size = WIDTH, HEIGHT
                        drag_x, drag_y = 0, 0
                        running = False
                    if buttons_ind[1].button_rect.collidepoint(x, y):
                        if energy[0] >= energy[1]:
                            save_ship()
                            running = False
                        else:
                            print('Недостаточно энергии')
                    if buttons_ind[2].button_rect.collidepoint(x, y):
                        ship_nummer -= 1
                        load_ship_to_editor(ship_nummer)
                    if buttons_ind[3].button_rect.collidepoint(x, y):
                        ship_nummer += 1
                        load_ship_to_editor(ship_nummer)
                if event.button == 4:  # Колесо вверх
                    # Масштабирование вверх
                    scale_factor = 1.05
                elif event.button == 5 and current_size[0] > 1280:  # Колесо вниз
                    # Масштабирование вниз
                    scale_factor = 1 / 1.05
                else:
                    scale_factor = 1

                    # Получение координат курсора относительно поверхности (surface)
                rel_x = x - drag_x
                rel_y = y - drag_y

                # Масштабирование размера окна
                current_size = tuple(int(x * scale_factor) for x in current_size)

                # Пересчет смещения
                drag_x = x - rel_x * scale_factor
                drag_y = y - rel_y * scale_factor
                #print(drag_x, drag_y)
                if drag_x > 0:
                    drag_x = 0
                if drag_y > 0:
                    drag_y = 0
                # Определение максимальных значений смещения
                if current_size[0] > WIDTH:
                    max_drag_x = -(current_size[0] - WIDTH)
                if current_size[1] > HEIGHT:
                    max_drag_y = -(current_size[1] - HEIGHT)
                if drag_x < max_drag_x:
                    drag_x = max_drag_x
                if drag_y < max_drag_y:
                    drag_y = max_drag_y
                # Обновление смещения
                #drag_x = min(drag_x, max_drag_x)
                #drag_y = min(drag_y, max_drag_y)
                if current_size[0] < WIDTH:
                    drag_x, drag_y = 0, 0
                    max_drag_x, max_drag_y = 0, 0
                    current_size = WIDTH, HEIGHT

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pressed = False
                start_time = 0
                cords = event.pos
                handle_mouse_click()
                if part_cells.next_page.button_rect.collidepoint(x, y):
                    part_cells.page_set(1)
                if part_cells.prev_page.button_rect.collidepoint(x, y):
                    part_cells.page_set(-1)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False
            if event.type == VIDEORESIZE:
                current_size = event.size
        if mouse_pressed:
            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time > 1000:
                replace_part(x, y)
        for button in buttons_ind:
            button.set_pos(WIDTH, HEIGHT)
            button.draw(true_screen)
            button.check_hover((x, y))
        true_screen.blit(cursor, (blit_x-3, blit_y-3))

        pygame.display.update()
        scaled_screen = transform.scale(screen, current_size)
        drag_x, drag_y = ship_editor_control(drag_x, drag_y, current_size, max_drag_x, max_drag_y)
        true_screen.blit(scaled_screen, (drag_x, drag_y))

        clock.tick(60)


def settings():
    global current_size

    buttons, video_button_list, button_prev = create_settings_objects(WIDTH, HEIGHT)

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        screen.blit(menu_screen, (0, 0))

        for button in buttons:
            button.check_hover(mouse)
        button_prev.draw(screen)
        button_prev.check_hover(mouse)

        for event in pygame.event.get():
            # Назад в меню
            if event.type == pygame.MOUSEBUTTONUP and button_prev.button_rect.collidepoint(mouse):
                fade()
                running = False
            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and buttons[0].button_rect.collidepoint(mouse):
                change_resolution(1280, 720)

            if event.type == pygame.MOUSEBUTTONDOWN and buttons[1].button_rect.collidepoint(mouse):
                change_resolution(1600, 900)

            if event.type == pygame.MOUSEBUTTONDOWN and buttons[2].button_rect.collidepoint(mouse):
                change_resolution(1920, 1080, pygame.FULLSCREEN)

            for button in buttons:
                button.handle_event(event)
            if event.type == VIDEORESIZE:
                current_size = event.size
        video_button_list.set_pos(WIDTH, HEIGHT)
        video_button_list.draw(screen)
        screen.blit(cursor, mouse)
        scaled_screen = transform.scale(screen, current_size)
        true_screen.blit(scaled_screen, (0, 0))
        pygame.display.update()


def fade():
    running = True
    fade_alpha = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fade_surface = pygame.Surface(current_size)
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        true_screen.blit(fade_surface, (0, 0))
        fade_alpha += 0.8
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False
        pygame.display.update()


def change_resolution(w, h, fullscreen=0):
    global WIDTH, HEIGHT, true_screen, scaled_screen, bg, menu_screen, ship_yard, level_select_screen, level_info,\
        current_size, screen
    WIDTH, HEIGHT = w, h
    current_size = w, h
    screen = Surface((WIDTH, HEIGHT))

    true_screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE | fullscreen)
    bg = pygame.transform.scale(bg_load, (WIDTH, HEIGHT))
    menu_screen = pygame.transform.scale(menu_screen_load, (WIDTH, HEIGHT))
    ship_yard = pygame.transform.scale(ship_yard_load, (WIDTH, HEIGHT))
    level_select_screen = pygame.transform.scale(level_select_screen_load, (WIDTH, HEIGHT))
    level_info = pygame.transform.scale(level_info_load, (400, HEIGHT))


if __name__ == '__main__':
    main_menu()
