from govno import *

class Cursor:
    def __init__(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.coff = 0.5

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()


class Map:
    def __init__(self, cords, map_size):
        self.x, self.y = cords
        self.map_size_x, self.map_size_y = map_size
        load_texture = pygame.image.load('models/minimap/minimap.png').convert_alpha()
        self.texture = pygame.transform.scale(load_texture, (200, 200))
        self.width, self.height = self.texture.get_size()

        # Размеры рамки миникарты (в данном случае сделаем 10 пикселей с каждой стороны)
        self.frame_size = 15

    def update(self, surface, objects):
        # Рассчитываем масштаб
        scale_x = (self.width - 2 * self.frame_size) / (2 * self.map_size_x)
        scale_y = (self.height - 2 * self.frame_size) / (2 * self.map_size_y)

        # Выводим текстуру миникарты
        surface.blit(self.texture, (self.x, self.y))

        # Выводим точки объектов
        for object in objects:
            # Корректируем координаты объекта, учитывая рамку миникарты
            adjusted_x = object.blit_point_x + self.map_size_x - self.frame_size
            adjusted_y = object.blit_point_y + self.map_size_y - self.frame_size

            # Масштабируем координаты точки
            scaled_x = int(adjusted_x * scale_x) + self.x + self.frame_size
            scaled_y = int(adjusted_y * scale_y) + self.y + self.frame_size

            # Рисуем точку
            pygame.draw.circle(surface, object.fraction, (scaled_x, scaled_y), 5)


class Energy_bar():
    def __init__(self, texture_path_1, texture_path_2, texture_path_3):
        self.load_texture_1 = pygame.image.load(texture_path_1)
        self.load_texture_2 = pygame.image.load(texture_path_2)
        self.load_texture_3 = pygame.image.load(texture_path_3)

    def scale_bar(self, screen, energy):
        not_used_energy = pygame.transform.scale(self.load_texture_1, (250, 40))
        screen.blit(not_used_energy, (self.x, self.y))
        try:
            filled = energy[1]/energy[0] * 200
        except:
            filled = 0
        if energy[0] >= energy[1]:
            used_energy = pygame.transform.scale(self.load_texture_2, (filled, 36))
            screen.blit(used_energy, (self.x+1, self.y+2))
        elif energy[0] > 0:
            used_energy = pygame.transform.scale(self.load_texture_2, (249, 36))
            screen.blit(used_energy, (self.x+1, self.y+2))
            if filled - 249 <= 250:
                over_used_energy = pygame.transform.scale(self.load_texture_3, (filled-249, 36))
            else:
                over_used_energy = pygame.transform.scale(self.load_texture_3, (250, 36))

            screen.blit(over_used_energy, (self.x+1, self.y+2))
        else:
            over_used_energy = pygame.transform.scale(self.load_texture_3, (249, 36))
            screen.blit(over_used_energy, (self.x+1, self.y+2))

    def set_pos(self, current_width, current_height, y=None):
        self.x = current_width * 0.5 - 250/2
        self.y = current_height * 0.1

class Grid:
    def __init__(self, cell_width, cell_height, rows, cols):
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.rows = rows
        self.cols = cols
        cell_load_texture = pygame.image.load('models/garage/build_cell.png')
        self.texture = pygame.transform.scale(cell_load_texture, (cell_width, cell_height))

    def draw(self, surface, screen_width, screen_height):
        # Начальные координаты для центрирования сетки в центре экрана
        start_x = (screen_width - self.cols * self.cell_width) // 2
        start_y = (screen_height - self.rows * self.cell_height) // 2

        for x in range(start_x, start_x + self.cell_width * self.cols, self.cell_width):
            for y in range(start_y, start_y + self.cell_height * self.rows, self.cell_height):
                grid_x, grid_y = self.snap_to_grid(x, y)
                surface.blit(self.texture, (grid_x, grid_y))

    def snap_to_grid(self, x, y, part=None):
        # Выравниваем координаты по сетке
        x = (x // self.cell_width) * self.cell_width
        y = (y // self.cell_height) * self.cell_height
        try:
            x += (self.cell_height - part.width) // 2
            y += (self.cell_height - part.height) // 2
        except:
            pass
        return x, y

class CellsForPartList:
    def __init__(self, current_width, current_height, percent_x, percent_y, parts):
        self.percent_x = percent_x / 100
        self.percent_y = percent_y / 100
        self.x = self.percent_x * current_width
        self.y = self.percent_y * current_height
        self.parts = parts
        self.texture = pygame.transform.scale(pygame.image.load('models/garage/part_cell.png'), (150, 120))
        self.prev_page = ImageButton(current_width, current_height, 15, 85, 35, 120, None, 'models/buttons/prev_page.png',
                                     'models/buttons/prev_page_selected.png')
        self.next_page = ImageButton(current_width, current_height, 82, 85, 35, 120, None, 'models/buttons/next_page.png',
                                     'models/buttons/next_page_selected.png')
        self.part_rect = self.texture.get_rect()
        self.width = self.texture.get_size()[0]
        self.parts_on_page = []
        self.page = 0
        if len(self.parts) % 5 == 0:
            b = 0
        else:
            b = 1
        self.max_pages = len(self.parts)//5+b
        self.page_set()

    def page_set(self, a=0):
        check_page = self.page + a
        if 0 <= check_page < self.max_pages:
            self.page += a
        self.parts_on_page.clear()
        start_index = self.page * 5  # Начальный индекс для отображения деталей
        end_index = min(start_index + 5, len(self.parts))  # Конечный индекс

        for part in self.parts[start_index:end_index]:
            self.parts_on_page.append(part)

    def draw(self, screen, width):
        total_width = len(self.parts_on_page) * (self.texture.get_width() + 10) - 10  # Общая ширина линии
        start_x = (screen.get_width() - total_width) / 2  # Начальная X-координата для центрирования

        space_x = start_x  # Интервал между квадратами по горизонтали
        for part in self.parts_on_page:
            drag = 0
            drag += 10
            current_rect = self.texture.get_rect(topleft=(space_x, self.y))
            screen.blit(self.texture, current_rect)

            # Отображаем изображение из массива parts
            part.width = part.texture.get_size()[0]
            part.height = part.texture.get_size()[1]
            part.texture = pygame.transform.scale(part.texture, (80, 100))
            part.just_draw(screen, (current_rect[0] + self.width / 2 - part.width / 2, current_rect[1] + 7))

            space_x += self.texture.get_width() + 10  # 10 - интервал между квадратами

        # Установка позиции кнопок prev_page и next_page
        self.prev_page.x = start_x - 55  # Позиция prev_page в начале списка всех деталей
        self.next_page.x = start_x + total_width + 20  # Позиция next_page в конце списка всех деталей

        mouse = pygame.mouse.get_pos()
        self.prev_page.draw(screen)
        self.next_page.draw(screen)
        self.prev_page.check_hover(mouse)
        self.next_page.check_hover(mouse)

    def change_page(self):


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if self.prev_page.button_rect.collidepoint(mouse) and event.button == 1:
                    pass
                if self.next_page.button_rect.collidepoint(mouse) and event.button == 1:
                    pass

            self.prev_page.handle_event(event)
            self.next_page.handle_event(event)

class Writing:
    def __init__(self, text, x, y, font, size, blit_time=None):
        self.text = text
        self.x_cord = x
        self.y_cord = y
        self.blit_time = blit_time
        if font == 1:
            self.font = pygame.font.Font('fonts/SAIBA-45-Regular-(v1.1).otf', size)
        elif font == 2:
            self.font = pygame.font.Font('fonts/cuyabra-Regular.otf', size)

        self.rendered_text = self.font.render(self.text, False, (195, 195, 195))
        self.text_rect = self.rendered_text.get_rect(center=(self.x_cord, self.y_cord))

    def write(self, screen):
        screen.blit(self.rendered_text, (self.text_rect[0], self.text_rect[1]))
        if self.blit_time is not None:
            self.blit_time -= 1


class ImageButtonList:
    def __init__(self, current_width, current_height, percent_x, percent_y, image_path, buttons, width=350):
        self.percent_x = percent_x/100
        self.percent_y = percent_y/100
        self.width = width
        self.height = 0
        self.buttons = buttons
        self.x = self.percent_x * current_width
        self.y = self.percent_y * current_height

        for button in self.buttons:
            #self.width += button.width
            self.height += button.height + 25
        self.texture = pygame.image.load(image_path)
        self.list_rect = self.texture.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        space_y = 0
        self.list_rect = self.texture.get_rect(topleft=(self.x, self.y))

        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        screen.blit(self.texture, (self.x, self.y))
        for button in self.buttons:
            button.draw_in_list(screen, self.list_rect, space_y)
            space_y += (button.height + 10)

    def set_pos(self, current_width, current_height, y=None):
        self.x = current_width * self.percent_x - self.width/2
        self.y = current_height * self.percent_y

    def reset_len(self):
        self.height = 0
        for button in self.buttons:
            #self.width += button.width
            self.height += button.height + 25

class ImageButton:
    def __init__(self, current_width, current_height, percent_x, percent_y, width, height, text, image_path, hover_image=None, sound_path=None):
        self.percent_x = percent_x/100
        self.percent_y = percent_y/100
        self.x = self.percent_x * current_width
        self.y = self.percent_y * current_height
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        if hover_image:
            self.hover_image = pygame.image.load(hover_image)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.button_rect = self.image.get_rect(topleft=(self.x, self.y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False

    def draw(self, screen, named=False):
        self.button_rect = self.image.get_rect(topleft=(self.x, self.y))

        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.button_rect)
        if named:
            pass
        if self.text is not None:
            font = pygame.font.Font('fonts/SAIBA-45-Regular-(v1.1).otf', 30)
            rendered_text = font.render(self.text, False, (195, 195, 195))
            text_rect = rendered_text.get_rect(center=self.button_rect.center)

            screen.blit(rendered_text, text_rect)

    def draw_in_list(self, screen, list_rect, space_y):
        self.button_rect = self.image.get_rect(topleft=(list_rect[0]+25, list_rect[1] + space_y + 27))
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.button_rect)

        if self.text is not None:
            font = pygame.font.Font('fonts/SAIBA-45-Regular-(v1.1).otf', 30)
            rendered_text = font.render(self.text, False, (195, 195, 195))
            text_rect = rendered_text.get_rect(center=self.button_rect.center)
            screen.blit(rendered_text, text_rect)

    def check_hover(self, mouse_pos, offset_x=0, offset_y=0):
        #print(offset_x)
        self.is_hovered = self.button_rect.collidepoint(mouse_pos[0]+offset_x, mouse_pos[1]+offset_y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
                return True
    def set_pos(self, current_width, current_height, y=None):
        self.x = current_width * self.percent_x - self.width/2
        self.y = current_height * self.percent_y
        self.button_rect = self.image.get_rect(topleft=(self.x, self.y))







