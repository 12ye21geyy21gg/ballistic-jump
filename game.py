import game_objects, map_gen, graph_engine, pygame, math, random, store_menu

KOEF = 1


def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Game:
    def __init__(self, vw, vh, graph_engine, saver):
        self.sprites = pygame.sprite.Group()
        self.saver = saver
        self.map_gen = map_gen.Map_Gen(self.sprites)
        self.map = map_gen.Map(vw, vh, self.sprites)
        self.map_gen.generate(self.map.platforms, self.map.bonuses, 50)
        self.camera = game_objects.Camera(-30, 0, vw, vh, self.map.player)
        self.graph_engine = graph_engine
        self.view_width = vw
        self.view_height = vh
        self.clock = pygame.time.Clock()
        self.portal_clock = pygame.time.Clock()
        self.portal_duration = 2000
        self.end = False
        self.lx = 0
        self.ly = 0
        self.rx = 0
        self.ry = 0
        self.right = False
        self.left = False
        self.time_scale = 6
        self.debug = True
        self.map.set_sprites()
        self.isUpdated = True
        self.counter = 0
        self.store = self.load_store()
        self.load_player()
        if self.store is None:
            self.store = store_menu.Store(self.graph_engine.num_cols * self.graph_engine.num_rows)
            self.store.portal_height = self.view_height // 2
            self.store.prepare()

    def load_player(self):
        t = self.saver.load()
        if t is not None:
            self.map.player.v0 = t[0]
            self.map.player.starter_I = t[1]
            self.map.player.starter_II = t[2]
            self.map.player.starter_III = t[3]
            self.map.player.wind_protection = t[4]
            self.map.player.money = t[5]

    def load_store(self):
        t = self.saver.load()
        if t is not None:
            return t[-1]

    def prepare(self):
        self.graph_engine.prepare(self.camera, self.map, self.store, self.sprites)
        temp, temp2 = self.map.get_nearest_objects(self.camera.x)
        temp.extend(temp2)
        self.graph_engine.set_objects(temp)
        self.map.change_wind()
        self.prep_imgs()

    def restart(self):
        self.clock = pygame.time.Clock()
        self.end = False
        self.lx = 0
        self.ly = 0
        self.rx = 0
        self.ry = 0
        self.right = False
        self.left = False
        self.time_scale = 6
        self.debug = True
        self.map.bonuses.clear()
        self.map.platforms.clear()
        self.map.reset()
        self.map.change_wind()
        self.map_gen = map_gen.Map_Gen(self.sprites)
        self.camera = game_objects.Camera(-30, 0, self.view_width, self.view_height, self.map.player)
        self.map_gen.generate(self.map.platforms, self.map.bonuses, 50)
        self.portal_duration = 2000
        self.portal_clock = pygame.time.Clock()
        self.prep_imgs()

    def move_player(self):
        if self.map.player.isFlying:
            dt = self.clock.tick() / 1000 * self.time_scale
            fracs = int(max(abs(self.map.player.vx), abs(self.map.player.vy)))
            if fracs != 0:
                dt = dt / fracs * KOEF
                for i in range(fracs):
                    self.move_player_hidden(dt)
            else:
                self.move_player_hidden(dt)
            if self.map.player.x >= self.map_gen.prev_x - 2 * self.view_width:
                self.map_gen.generate(self.map.platforms, self.map.bonuses, 50)
                self.prep_imgs()

    def move_player_hidden(self, dt):
        self.map.player.x += self.map.player.vx * dt + (
                self.map.player.calc_wind_accel(self.map.wind_accel) * dt ** 2) / 2
        self.map.player.y += self.map.player.vy * dt + (self.map.gravity_accel * dt ** 2) / 2
        self.map.player.vy += self.map.gravity_accel * dt
        self.map.player.vx += self.map.player.calc_wind_accel(self.map.wind_accel) * dt
        platforms, bonuses = self.map.get_nearest_objects(self.map.player.x)
        for i in platforms:

            if i.rel_pos(self.map.player) == 5:
                if i.r_pos == 1:
                    self.map.player.isFlying = False
                    self.map.player.y = i.y + i.height
                    self.map.player.vx = 0
                    self.map.player.vy = 0
                elif i.r_pos == 2:
                    self.map.player.vx = 0
                    self.map.player.x = i.x - self.map.player.width
                elif i.r_pos == 3:
                    self.map.player.vx = 0
                    self.map.player.x = i.x + i.width
                elif i.r_pos == 4:
                    self.map.player.vy = 0
                    self.map.player.y = i.y - self.map.player.height
            i.r_pos = i.rel_pos(self.map.player)
        for i in bonuses:
            if i.rel_pos(self.map.player) == 5 and type(i) is not game_objects.Portal:
                if i.type == 1:
                    self.map.player.num_I += 1
                elif i.type == 2:
                    self.map.player.num_II += 1
                elif i.type == 3:
                    self.map.player.num_III += 1
                self.map.bonuses.remove(i)
        if self.map.player.y + self.map.player.height < 0:
            self.end = True
            self.graph_engine.paused = True
            self.map.player.isFlying = False
        self.map.player.distance = max(self.map.player.distance, self.map.player.x)

    def update(self):
        if not self.end and not self.graph_engine.paused:
            if not self.map.player.isFlying and not self.left and self.lx != 0 and self.ly != 0:
                self.start_jump(self.lx, self.ly)
                self.lx = 0
                self.ly = 0
            self.move_player()
            self.map.clean(self.map.player.x)
            temp, temp2 = self.map.get_nearest_objects(self.camera.x)
            temp.extend(temp2)
            self.check_portals()
            self.graph_engine.set_objects(temp)
            self.camera_update()
            self.graph_engine.draw()
            if not self.isUpdated and not self.map.player.isFlying and not self.end:
                self.map.player.update_money()
                self.saver.save(self.save())
                self.isUpdated = True
            pass
        else:
            self.graph_engine.draw()

    def camera_update(self):
        self.camera.dx = int(self.rx)
        self.camera.dy = int(self.ry)
        self.rx = 0
        self.ry = 0
        self.camera.update()

    def save(self):
        return [self.map.player.v0, self.map.player.starter_I, self.map.player.starter_II, self.map.player.starter_III,
                self.map.player.wind_protection, self.map.player.money, self.store]

    def start_jump(self, x, y):
        self.isUpdated = False
        self.map.player.isFlying = True

        x = self.camera.x + x - self.map.player.x - self.map.player.width // 2
        y = self.camera.y + self.view_height - y - self.map.player.y - self.map.player.height // 2
        length = math.sqrt(x ** 2 + y ** 2)
        if length >= self.map.player.precision:
            v0 = self.map.player.v0
        else:
            v0 = self.map.player.v0 * length / self.map.player.precision
        a = math.atan2(y, x)
        v0 *= self.map.player.boost
        self.map.player.boost = 1
        self.map.player.vx = v0 * math.cos(a)
        self.map.player.vy = v0 * math.sin(a)
        self.clock.tick()

    def pass_left(self, x, y):
        if not self.graph_engine.paused:
            self.lx = x
            self.ly = y

            self.graph_engine.x = x
            self.graph_engine.y = y

    def pass_right(self, dx, dy):

        if not self.graph_engine.paused:
            self.rx += dx
            self.ry += dy

    def pass_player(self, x, y):
        self.map.player.x = self.camera.x + x
        self.map.player.y = self.camera.y + y

    def pause(self):
        if not self.end:
            if self.graph_engine.paused:
                self.graph_engine.paused = False
                self.clock.tick()
                self.portal_clock.tick()
            else:
                self.graph_engine.paused = True

    def check_portals(self):
        dt = self.portal_clock.tick()
        for i in self.map.bonuses:
            if type(i) == game_objects.Portal:
                if not i.check(dt):
                    self.map.bonuses.remove(i)

    def clear_imgs(self):
        self.map.player.image = None
        self.map.player.rect = None
        for i in self.map.platforms:
            i.image = None
            i.rect = None
        for i in self.map.bonuses:
            i.image = None
            i.rect = None
        self.map.background.image = None
        self.map.group = None
        self.map_gen.group = None

    def prep_imgs(self):
        self.map.group = self.sprites
        self.map_gen.group = self.sprites
        self.map.player.set_image('doodle.bmp', -1)
        self.map.set_sprites()
        self.map.background.set()

    def use_first(self):
        if not self.graph_engine.paused and self.map.player.isFlying and self.map.player.num_I > 0:
            self.map.player.isFlying = False
            self.map.player.vx = 0
            self.map.player.vy = 0
            self.map.platforms.append(
                game_objects.Platform(self.map.player.x, self.map.player.y - 30, 20, 30, self.sprites))
            self.map.set_sprites()
            self.map.player.num_I -= 1
            if self.map.player.num_I < 0:
                self.map.player.num_I = 0

    def use_second(self):
        if not self.graph_engine.paused and not self.map.player.isFlying and self.map.player.boost == 1 and self.map.player.num_II > 0:
            self.map.player.boost = self.store.boost
            self.map.player.num_II -= 1
            if self.map.player.num_II < 0:
                self.map.player.num_II = 0

    def use_third(self):
        if not self.graph_engine.paused and self.map.player.isFlying and self.map.player.num_III > 0:
            self.map.player.num_III -= 1
            self.map.bonuses.append(
                game_objects.Portal(self.map.player.x, self.map.player.y, 1, self.portal_duration, self.sprites))
            self.map.player.y += self.store.portal_height
            self.map.bonuses.append(
                game_objects.Portal(self.map.player.x, self.map.player.y, 2, self.portal_duration, self.sprites))
            if self.map.player.num_III < 0:
                self.map.player.num_III = 0
