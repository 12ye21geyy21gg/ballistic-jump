import pygame, game_objects


class Graphical_Engine:
    def __init__(self, vw, vh, screen):
        self.view_width = vw
        self.view_height = vh
        self.screen = screen
        self.color = pygame.Color('black')
        self.temp_objects = list()
        self.mode = 2  # 1 main menu, 2 game,3 store
        self.isAiming = False
        self.margin = 40
        self.text_margin = 2
        self.wind_scale = 40
        self.map = None
        self.x = 0
        self.y = 0
        self.information_font = pygame.font.Font('data/FreeSans.ttf', 15)

    def prepare(self, player, background, camera, map):
        self.background = background
        self.player = player
        self.camera = camera
        self.map = map

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
            pass
        elif self.mode == 2:
            self.draw_background()
            if len(self.temp_objects) > 0:
                for i in self.temp_objects:
                    self.draw_object(i)
            self.draw_object(self.player)
            if self.isAiming:
                pygame.draw.line(self.screen, pygame.Color('blue'), self.get_rel_coords_center(self.player),
                                 (self.x, self.y),
                                 2)
                pygame.draw.circle(self.screen, pygame.Color('blue'), self.get_rel_coords_center(self.player),
                                   int(self.player.precision), 1)
                pass
            # print(self.map.wind_accel)
            self.draw_misc()

        elif self.mode == 3:
            pass

    def draw_misc(self):

        draw_list = list()
        mxw = self.wind_scale
        mxh = self.margin // 2
        temp = self.information_font.render(f'wind force :{round(abs(self.map.wind_accel), 1)}', True,
                                            pygame.Color('blue'))
        temp_r = temp.get_rect()
        mxw = max(mxw, temp_r.width)
        mxh = max(mxh, temp_r.height)
        draw_list.append((temp, temp_r))
        temp = self.information_font.render(f'distance traveled :{round(self.map.player.distance / 100, 1)}', True,
                                            pygame.Color('blue'))
        temp_r = temp.get_rect()
        mxw = max(mxw, temp_r.width)
        mxh = max(mxh, temp_r.height)
        draw_list.append((temp, temp_r))

        pygame.draw.rect(self.screen, pygame.Color('#fccb76'), ((self.margin // 2, self.margin // 2), (
        mxw + self.margin + len(draw_list) * self.text_margin, mxh + self.margin + len(draw_list) * self.text_margin)),
                         0)
        pygame.draw.rect(self.screen, pygame.Color('#875704'),
                         ((self.margin // 2, self.margin // 2), (mxw + self.margin + len(draw_list) * self.text_margin,
                                                                 mxh + self.margin + len(
                                                                     draw_list) * self.text_margin)), 3)

        pygame.draw.line(self.screen, pygame.Color('blue'),
                         (self.margin, self.margin),
                         (self.margin + self.wind_scale, self.margin), 5)
        pygame.draw.line(self.screen, pygame.Color('purple'),
                         (self.margin + self.wind_scale // 2, 3 * self.margin // 4), (
                             self.margin + self.wind_scale // 2 + int(
                                 self.wind_scale // 2 * self.map.wind_accel / (self.map.max_wind / 2)),
                             3 * self.margin // 4),
                         5)
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
