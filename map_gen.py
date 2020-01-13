import random, game_objects


class Map:
    def __init__(self, vw, vh, group):
        self.platforms = list()  # [x,y,width,height]
        self.bonuses = list()  # [x,y,type]
        self.group = group
        self.player = game_objects.Player(10, 50, group)
        self.platforms.append(game_objects.Platform(10, 20, 20, 30, self.group))
        self.wind_accel = 0
        self.max_wind = 3
        self.gravity_accel = -10
        self.view_width = vw
        self.view_height = vh
        self.margin = self.view_width
        self.background = game_objects.Background(group)

    def get_nearest_objects(self, px):  # px -> 0
        plats = list()
        bonus = list()
        for i in self.platforms:
            if i.x >= -self.margin + px and i.x <= self.margin + px + self.view_width:
                plats.append(i)
        for i in self.bonuses:
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
        self.wind_accel = random.random() * self.max_wind - self.max_wind / 2

    def set_view(self, vw, vh):
        self.view_width = vw
        self.view_height = vh

    def set_sprites(self):
        for i in self.platforms:
            pass
        for i in self.bonuses:
            pass
        pass

    def reset(self):
        self.player.vx = 0
        self.player.vy = 0
        self.player.isFlying = False
        self.player.x = 10
        self.player.y = 50
        self.player.distance = 0
        self.player.update_bonuses()
        self.platforms.append(game_objects.Platform(10, 20, 20, 30, self.group))



class Map_Gen:
    def __init__(self, group):
        self.hor_step = 300
        self.ver_step = 100
        self.margin_width = 50
        self.platform_width = 100
        self.platform_height = 50
        self.max_bonuses = 2
        self.prev_x = 0
        self.dx = 0
        self.bonus_chance = 0.1
        self.boost = 5
        self.group = group

    def generate(self, platforms, bonuses, N):
        for i in range(N):
            dx = random.randint(0, self.hor_step) + self.margin_width
            self.dx += dx
            self.prev_x += dx
            t = game_objects.Platform(self.prev_x, random.randint(0, self.ver_step) + 30,
                                      random.randint(10, self.platform_width), random.randint(10, self.platform_height),
                                      self.group)
            platforms.append(t)
        for i in range(N):
            if random.random() < self.bonus_chance:

                isGood = False
                while not isGood:
                    isGood = True
                    t = game_objects.Bonus(random.randint(self.prev_x - self.dx, self.prev_x),
                                           random.randint(0, self.ver_step * 2) + 30 + self.ver_step,
                                           random.randint(1, self.max_bonuses),
                                           self.group)  # max type?
                    for i in platforms:
                        if i.rel_pos(t) == 5:
                            isGood = False

                bonuses.append(t)
        self.dx = 0
