import pygame, game_objects, main_menu, math


class Graphical_Engine:
    def __init__(self, vw, vh, screen):
        self.view_width = vw
        self.view_height = vh
        self.screen = screen
        self.color = pygame.Color('black')
        self.menu = main_menu.Main_Menu(vw, vh, screen)
        self.temp_objects = list()
        self.mode = 2  # 1 store, 2 game
        self.paused = True
        self.isAiming = False
        self.margin = 40
        self.text_margin = 2
        self.wind_scale = 40
        self.map = None
        self.x = -1
        self.y = -1
        self.information_font = pygame.font.Font('data/FreeSans.ttf', 15)
        self.information_font.set_bold(True)
        self.information_color = pygame.Color('#875704')
        self.num_cols = 2
        self.num_rows = 4
        self.button_width = (self.view_width - 2 * self.margin - self.margin // 2 * (
                    self.num_cols - 1)) // self.num_cols
        self.button_height = (self.view_height - 2 * self.margin - self.margin // 2 * (
                    self.num_rows - 1)) // self.num_rows
        self.store_font = pygame.font.Font('data/FreeSans.ttf', 20)
        self.store_font.set_bold(True)

    def prepare(self, camera, map):

        self.camera = camera
        self.map = map
        self.player = self.map.player
        self.background = self.map.background

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def set_color_by_obj(self, obj):
        if type(obj) is game_objects.Player:
            self.color = pygame.Color('green')
        elif type(obj) is game_objects.Platform:
            self.color = pygame.Color('red')
        elif type(obj) is game_objects.Bonus:
            self.color = pygame.Color('yellow')
        else:
            self.color = pygame.Color('white')

    def set_objects(self, objects):
        self.temp_objects.clear()
        self.temp_objects = objects

    def draw(self):
        self.clear_screen()
        if self.mode == 1:
            self.draw_store()
        elif self.mode == 2:
            self.draw_background()
            if len(self.temp_objects) > 0:
                for i in self.temp_objects:
                    self.draw_object(i)
            self.draw_object(self.player)
            if self.isAiming and self.x != -1 and self.y != -1:
                pygame.draw.line(self.screen, pygame.Color('blue'), self.get_rel_coords_center(self.player),
                                 (self.x, self.y),
                                 2)
                pygame.draw.circle(self.screen, pygame.Color('blue'), self.get_rel_coords_center(self.player),
                                   int(self.player.precision), 1)
                x = self.x - self.get_rel_coords_center(self.player)[0]
                y = self.y - self.get_rel_coords_center(self.player)[1]
                length = math.sqrt(x ** 2 + y ** 2)

                if length >= self.map.player.precision:
                    v0 = self.map.player.v0
                else:
                    v0 = self.map.player.v0 * length / self.map.player.precision
                v0 *= self.player.boost
                x = self.get_rel_coords_center(self.player)[0] + x // 2
                y = self.get_rel_coords_center(self.player)[1] + y // 2
                temp = self.information_font.render(f'{round(abs(v0), 2)}', True,
                                                    pygame.Color('#0cdff2'))
                temp_r = temp.get_rect()
                temp_r.x = x
                temp_r.y = y
                self.screen.blit(temp, temp_r)
                pass
            # print(self.map.wind_accel)
            self.draw_misc()
        if self.paused:
            self.draw_pause()

    def draw_store(self):
        for i in range(self.num_rows * self.num_cols):
            pygame.draw.rect(self.screen, pygame.Color('#fccb76'), ((self.margin + (i // self.num_rows) * (
                        self.button_width + self.margin // 2), self.margin + (i % self.num_rows) * (
                                                                                 self.button_height + self.margin // 2)),
                                                                    (self.button_width, self.button_height)), 0)
            pygame.draw.rect(self.screen, pygame.Color('#875704'), ((self.margin + (i // self.num_rows) * (
                        self.button_width + self.margin // 2), self.margin + (i % self.num_rows) * (
                                                                                 self.button_height + self.margin // 2)),
                                                                    (self.button_width, self.button_height)), 5)

            if i == 0:
                pass
            elif i == self.num_rows * self.num_cols - 1:
                temp = self.store_font.render(f'your money:{self.map.player.money}', True,
                                              self.information_color)
                temp_r = temp.get_rect()
                temp_r.y = self.margin + (i % self.num_rows) * (
                            self.button_height + self.margin // 2) + self.button_height // 2 - temp_r.height // 2
                temp_r.x = self.margin + self.margin + (i // self.num_rows) * (
                            self.button_width + self.margin // 2) + self.button_width // 2 - temp_r.width // 2
                self.screen.blit(temp, temp_r)

    def draw_pause(self):
        self.menu.draw_button(1)
        self.menu.draw_button(2)
        self.menu.draw_button(3)
        self.menu.draw_button(4)

    def draw_misc(self):
        draw_list = list()
        mxw = self.wind_scale
        mxh = self.margin // 2
        temp = self.information_font.render(f'wind force:{round(abs(self.map.wind_accel), 1)}', True,
                                            self.information_color)
        temp_r = temp.get_rect()
        mxw = max(mxw, temp_r.width)
        mxh += temp_r.height + self.text_margin
        draw_list.append((temp, temp_r))
        temp = self.information_font.render(f'height:{int(self.player.y)}', True,
                                            self.information_color)
        temp_r = temp.get_rect()
        mxw = max(mxw, temp_r.width)
        mxh += temp_r.height + self.text_margin
        draw_list.append((temp, temp_r))
        temp = self.information_font.render(f'distance traveled:{round(self.map.player.distance / 100, 1)}', True,
                                            self.information_color)
        temp_r = temp.get_rect()
        mxw = max(mxw, temp_r.width)
        mxh += temp_r.height + self.text_margin
        draw_list.append((temp, temp_r))
        temp = self.information_font.render(f'money:{self.map.player.money}', True,
                                            self.information_color)
        temp_r = temp.get_rect()
        mxw = max(mxw, temp_r.width)
        mxh += temp_r.height + self.text_margin
        draw_list.append((temp, temp_r))
        temp = self.information_font.render(f'1 bonuses:{self.map.player.num_I}', True,
                                            self.information_color)
        temp_r = temp.get_rect()
        mxw = max(mxw, temp_r.width)
        mxh += temp_r.height + self.text_margin
        draw_list.append((temp, temp_r))
        temp = self.information_font.render(f'2 bonuses:{self.map.player.num_II}', True,
                                            self.information_color)
        temp_r = temp.get_rect()
        mxw = max(mxw, temp_r.width)
        mxh += temp_r.height + self.text_margin
        draw_list.append((temp, temp_r))

        pygame.draw.rect(self.screen, pygame.Color('#fccb76'), ((self.margin // 2, self.margin // 2), (
            mxw + self.margin + len(draw_list) * self.text_margin,
            mxh + self.text_margin)), 0)
        pygame.draw.rect(self.screen, pygame.Color('#875704'),
                         ((self.margin // 2, self.margin // 2),
                          (mxw + self.margin + len(draw_list) * self.text_margin,
                           mxh + self.text_margin)), 3)

        pygame.draw.line(self.screen, pygame.Color('purple'),
                         (self.margin, self.margin),
                         (self.margin + self.wind_scale, self.margin), 5)
        pygame.draw.line(self.screen, pygame.Color('red'),
                         (self.margin + self.wind_scale // 2, 3 * self.margin // 4), (
                             self.margin + self.wind_scale // 2 + int(
                                 self.wind_scale // 2 * self.map.wind_accel / (self.map.max_wind / 2)),
                             3 * self.margin // 4),
                         7)
        prev_y = self.margin
        for i in draw_list:
            t = i[1]
            t.x = self.margin
            t.y = prev_y + self.text_margin
            prev_y += t.height + self.text_margin
            self.screen.blit(i[0], t)


    def draw_background(self):
        pass

    def draw_object(self, obj):
        if obj.image is None:
            self.set_color_by_obj(obj)
            pygame.draw.rect(self.screen, self.color, (self.get_rel_coords(obj), (obj.width, obj.height)), 0)
        else:
            obj.connect_coords(self.view_height)
            pass

    def get_rel_coords(self, obj):
        return int(obj.x - self.camera.x), int(self.view_height - (obj.height + obj.y - self.camera.y))

    def get_rel_coords_center(self, obj):
        return int(obj.x + obj.width // 2 - self.camera.x), int(
            self.view_height - (obj.y - self.camera.y) - obj.height // 2)

    def get_button(self, x, y):
        for i in range(self.num_cols * self.num_rows):
            if x >= (self.margin + (i // self.num_rows) * (self.button_width + self.margin // 2)):
                if x <= (self.margin + (i // self.num_rows) * (
                        self.button_width + self.margin // 2)) + self.button_width:
                    if y >= self.margin + (i % self.num_rows) * (self.button_height + self.margin // 2):
                        if y <= self.margin + (i % self.num_rows) * (
                                self.button_height + self.margin // 2) + self.button_height:
                            return i
