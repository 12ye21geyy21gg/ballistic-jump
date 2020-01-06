import pygame, game_objects


class Graphical_Engine:
    def __init__(self, vw, vh, screen, camera, player, background):
        self.view_width = vw
        self.view_height = vh
        self.screen = screen
        self.color = pygame.Color('black')
        self.temp_objects = list()
        self.mode = 2  # 1 main menu, 2 game,3 store
        self.isAiming = False
        self.x = 0
        self.y = 0

    def prepare(self, player, background, camera):
        self.background = background
        self.player = player
        self.camera = camera


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
                pygame.draw.line(self.screen, pygame.Color('blue'), self.get_rel_coords(self.player), (self.x, self.y),
                                 2)
                pass

        elif self.mode == 3:
            pass

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
        return obj.x - self.camera.x, self.view_height - (obj.height + obj.y - self.camera.y)
