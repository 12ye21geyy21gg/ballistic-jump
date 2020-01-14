import pygame, os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.r_pos = 6  # unknown
        self.image = None

    """def collide(self, object):
        if self.collide_rect(object):
            return True
        else:
            return False # skip
    """

    def set_image(self, image):
        self.image = load_image(image)
        self.rect = self.image.get_rect()

    def connect_coords(self, vh):
        self.rect.x = self.x
        self.rect.y = vh - self.y - self.height

    def collide_rect(self, object):
        if self.x <= object.x + object.width:
            if self.x + self.width >= object.x:
                if self.y <= object.y + object.height:
                    if self.y + self.height >= object.y:
                        return True
        return False

    def rel_pos(self, object):
        if object.y >= self.y + self.height:  # 1 up
            return 1
        else:
            if object.y + object.height <= self.y:
                return 4  # down
            else:
                if object.x + object.width <= self.x:
                    return 2  # left
                elif object.x >= self.x + self.width:
                    return 3  # right
                else:
                    return 5  # inside


class Player(Object):
    def __init__(self, x, y, group):
        super().__init__(x, y, 20, 30, group)
        self.group = group
        self.prev_dist = 0
        self.v0 = 80.0
        self.precision = 200
        self.wind_protection = 0.0
        self.distance = 0
        self.isFlying = False
        self.vx = 0.0
        self.vy = 0.0
        self.bonuses = list()
        self.boost = 1
        self.money = 0
        self.num_I = 0
        self.num_II = 0
        self.starter_I = 1
        self.starter_II = 2
        self.update_bonuses()

    def update_bonuses(self):
        self.num_I = self.starter_I
        self.num_II = self.starter_II
        for i in range(self.starter_I):
            self.bonuses.append(Bonus(0, 0, 1, self.group))
        for i in range(self.starter_II):
            self.bonuses.append(Bonus(0, 0, 2, self.group))
    def calc_wind_accel(self, wind_a):
        return (1 - self.wind_protection) * wind_a

    def update_money(self):
        if int((self.distance - self.prev_dist) // 10000) > 0:
            self.money += int((self.distance - self.prev_dist) // 10000)
            self.prev_dist = self.distance


class Platform(Object):
    def __init__(self, x, y, width, height, group):
        super().__init__(x, y, width, height, group)


class Bonus(Object):
    def __init__(self, x, y, type, group):  # type?
        super().__init__(x, y, 25, 25, group)
        self.type = type
        self.get_image_by_type()

    def get_image_by_type(self):
        pass


class Camera:
    def __init__(self, x, y, vw, vh, player):
        self.x = x
        self.y = y
        self.view_width = vw
        self.view_height = vh
        self.player = player
        self.followPlayer = True
        self.dx = 0
        self.dy = 0

    def update(self):
        if self.followPlayer:
            self.x = self.player.x - self.view_width // 2
            self.y = self.player.y - self.view_height // 2
        else:
            self.x += self.dx
            self.y += self.dy
            self.dx = 0
            self.dy = 0

    def change_state(self):
        self.dx = 0
        self.dy = 0
        if self.followPlayer:
            self.followPlayer = False
        else:
            self.followPlayer = True


class Cursor(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = None
        self.x = 0
        self.y = 0

    def set_image(self, image):
        self.image = load_image(image)
        self.rect = self.image.get_rect()

    def connect_coords(self, vh):
        self.rect.x = self.x
        self.rect.y = vh - self.y - self.height


class Background(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = None
