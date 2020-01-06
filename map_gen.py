import random, game_objects


class Map:
    def __init__(self, vw, vh, group):
        self.platforms = list()  # [x,y,width,height]
        self.bonuses = list()  # [x,y,type]
        self.group = group
        self.player = game_objects.Player(10, 50, group)
        self.wind_accel = 0
        self.gravity_accel = -2.5
        self.view_width = vw
        self.view_height = vh
        self.margin = 100
        self.background = game_objects.Background(group)

    def get_nearest_objects(self, px):  # px -> 0
        plats = list()
        bonus = list()
        for i in self.platforms:
            if i.x >= -self.margin + px and i.x <= self.margin + px + self.view_width:
                plats.append(i)
        for i in self.platforms:
            if i.x >= -self.margin + px and i.x <= self.margin + px + self.view_width:
                bonus.append(i)
        return plats, bonus

    def clean(self, px):
        for i in self.platforms:
            if i.x <= -self.margin + px:
                self.platforms.remove(i)
        for i in self.bonuses:
            if i.x <= -self.margin + px:
                self.bonuses.remove(i)

    def change_wind(self):
        self.wind_accel = random.random() * 2 - 2

    def set_view(self, vw, vh):
        self.view_width = vw
        self.view_height = vh

    def set_sprites(self):
        for i in self.platforms:
            pass
        for i in self.bonuses:
            pass
        pass



class Map_Gen:
    def __init__(self, group):
        self.hor_step = 300
        self.ver_step = 100
        self.p_width = 100
        self.p_height = 50
        self.prev_x = 0
        self.bonus_chance = 0.1
        self.group = group

    def generate(self, platforms, bonuses, N):
        for i in range(N):
            dx = self.prev_x
            self.prev_x += random.randint(0, self.hor_step) + 100
            dx = self.prev_x - dx
            if random.random() < self.bonus_chance:
                bonuses.append(game_objects.Bonus(self.prev_x - random.randint(0, dx - 75) + self.p_width,
                                                  random.randint(0, self.ver_step) + 30, 1,
                                                  self.group))  # max_type unknown
            t = game_objects.Platform(self.prev_x, random.randint(0, self.ver_step) + 30,
                                      random.randint(10, self.p_width), random.randint(10, self.p_height), self.group)
            platforms.append(t)
