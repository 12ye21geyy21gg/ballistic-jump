import game_objects, map_gen, graph_engine, pygame, math, random

KOEF = 1


def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Game:
    def __init__(self, vw, vh, screen, graph_engine):
        self.sprites = pygame.sprite.Group()
        self.map = map_gen.Map(vw, vh, self.sprites)
        self.map_gen = map_gen.Map_Gen(self.sprites)
        self.camera = game_objects.Camera(-30, 0, vw, vh, self.map.player)  # ssss
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
        self.time_scale = 6
        self.debug = True
        self.map.set_sprites()
    def prepare(self):
        self.graph_engine.prepare(self.map.player, self.map.background, self.camera, self.map)
        self.map_gen.generate(self.map.platforms, self.map.bonuses, 50)
        self.map.change_wind()

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
        self.map = map_gen.Map(self.view_width, self.view_height, self.sprites)
        self.map_gen = map_gen.Map_Gen(self.sprites)
        self.camera = game_objects.Camera(-30, 0, self.view_width, self.view_height, self.map.player)

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

    def move_player_hidden(self, dt):
        self.map.player.x += self.map.player.vx * dt + (
                self.map.player.calc_wind_accel(self.map.wind_accel) * dt ** 2) / 2
        self.map.player.y += self.map.player.vy * dt + (self.map.gravity_accel * dt ** 2) / 2
        self.map.player.vy += self.map.gravity_accel * dt
        self.map.player.vx += self.map.player.calc_wind_accel(self.map.wind_accel) * dt
        platforms, bonuses = self.map.get_nearest_objects(self.map.player.x)
        for i in platforms:
            # if self.map.player.collide_rect(i):
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
            if i.rel_pos(self.map.player) == 5:
                print(i.type)
                self.map.player.bonuses.append(i)
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
            temp.append(self.map.player)

            self.graph_engine.set_objects(temp)
            self.camera_update()
            self.graph_engine.draw()
            pass
        else:
            self.graph_engine.draw()

    def camera_update(self):
        self.camera.dx = int(self.rx)
        self.camera.dy = int(self.ry)
        self.rx = 0
        self.ry = 0
        self.camera.update()

    def start_jump(self, x, y):  # rel to center
        self.map.player.isFlying = True
        # x = x - self.map.player.x
        # y = y - self.map.player.y
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
        self.map.player.vx = v0 * math.cos(a)  # * math.copysign(1,x)
        self.map.player.vy = v0 * math.sin(a)  # * math.copysign(1,y)
        self.clock.tick()

    def pass_left(self, x, y):
        if not self.graph_engine.paused:
            self.lx = x
            self.ly = y
            # self.graph_engine.isAiming = True
            self.graph_engine.x = x
            self.graph_engine.y = y

    def pass_right(self, dx, dy):  # dx,dy - float
        # dy is not inversed
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
            else:
                self.graph_engine.paused = True

    def use_first(self):
        for i in self.map.player.bonuses:
            if i.type == 1 and not self.graph_engine.paused and self.map.player.isFlying:
                self.map.player.isFlying = False
                self.map.player.vx = 0
                self.map.player.vy = 0
                self.map.platforms.append(
                    game_objects.Platform(self.map.player.x, self.map.player.y - 30, 20, 30, self.sprites))
                self.map.player.bonuses.remove(i)
                break

    def use_second(self):
        for i in self.map.player.bonuses:
            if i.type == 2 and not self.graph_engine.paused and not self.map.player.isFlying and self.map.player.boost == 1:
                self.map.player.boost = self.map_gen.boost
                self.map.player.bonuses.remove(i)
                break
