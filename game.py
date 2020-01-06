import game_objects, map_gen, graph_engine, pygame, math

KOEF = 10


def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Game:
    def __init__(self, vw, vh, screen, graph_engine):
        self.sprites = pygame.sprite.Group()
        self.map = map_gen.Map(vw, vh, self.sprites)
        self.map_gen = map_gen.Map_Gen(self.sprites)
        self.camera = game_objects.Camera(10, 50, vw, vh, self.map.player)  # ssss
        self.graph_engine = graph_engine  # graph_engine.Graphical_Engine(vw,vh,screen,self.camera,self.map.player,self.map.background)
        self.view_width = vw
        self.view_height = vh
        self.clock = pygame.time.Clock()
        self.end = False
        self.lx = 0
        self.ly = 0
        self.rx = 0
        self.ry = 0
        self.right = False
        self.left = False
        self.debug = True
    def prepare(self):
        self.graph_engine.prepare(self.map.player, self.map.background, self.camera)
        self.map_gen.generate(self.map.platforms, self.map.bonuses, 50)
        self.map.set_sprites()

    def move_player(self):
        if self.map.player.isFlying:
            dt = self.clock.tick() / 1000  # add time fractions
            fracs = abs(int(max(self.map.player.vx, self.map.player.vy)))
            if fracs != 0 and not self.debug:
                dt = dt / fracs * KOEF
                for i in range(fracs):
                    self.move_player_hidden(dt)
            else:
                self.move_player_hidden(dt)

    def move_player_hidden(self, dt):
        self.map.player.x += self.map.player.vx * dt + (
                self.map.player.calc_wind_accel(self.map.wind_accel) * dt ** 2) / 2
        self.map.player.y += self.map.player.vy * dt + (self.map.gravity_accel * dt ** 2) / 2
        self.map.player.vy += self.map.gravity_accel * dt
        self.map.player.vx += self.map.player.calc_wind_accel(self.map.wind_accel) * dt
        platforms, bonuses = self.map.get_nearest_objects(self.map.player.x)
        if not self.debug:
            for i in platforms:
                if self.map.player.collide_rect(i):
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
                else:
                    i.r_pos = self.map.player.rel_pos(i)
                    if i.r_pos == 5:
                        print('error')
        for i in bonuses:
            if self.map.player.collide_rect(i):
                if i.r_pos == 1:
                    pass  # consume bonus
            else:
                i.r_pos = self.map.player.rel_pos(i)
                if i.r_pos == 5:
                    print('error')
        if self.debug:
            if self.map.player.y < 10:
                self.map.player.y = 10
                self.map.player.isFlying = False
                self.map.player.vx = 0
                self.map.player.vy = 0
        else:
            if self.map.player.y + self.map.player.height < 0:
                self.end = True
                self.map.player.isFlying = False

    def update(self):
        if not self.end:
            if not self.map.player.isFlying and not self.left and self.lx != 0 and self.ly != 0:
                self.start_jump(self.lx, self.ly)
                self.lx = 0
                self.ly = 0
            self.move_player()
            temp, temp2 = self.map.get_nearest_objects(self.camera.x)
            temp.extend(temp2)
            temp.append(self.map.player)
            self.graph_engine.set_objects(temp)
            self.camera_update()
            self.graph_engine.draw()
            self.map.clean(self.map.player.x)
            pass
        else:
            pass  # call main menu

    def camera_update(self):
        self.camera.dx = int(self.rx)
        self.camera.dy = int(self.ry)
        self.rx = 0
        self.ry = 0
        self.camera.update()

    def start_jump(self, x, y):
        self.map.player.isFlying = True
        # x = x - self.map.player.x
        # y = y - self.map.player.y
        x = self.camera.x + x - self.map.player.x
        y = self.camera.y + y - self.map.player.y
        a = math.atan(y / x)
        print(x, y, a * 180 / 3.14)
        self.map.player.vx = self.map.player.v0 * math.cos(a)
        self.map.player.vy = self.map.player.v0 * math.sin(a)

    def pass_left(self, x, y):
        self.lx = x
        self.ly = y
        # self.graph_engine.isAiming = True
        self.graph_engine.x = x
        self.graph_engine.y = y

    def pass_right(self, dx, dy):  # dx,dy - float
        # dy is not inversed
        self.rx += dx
        self.ry += dy
