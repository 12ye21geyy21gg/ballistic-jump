import pygame, graph_engine, game


class Main:
    def __init__(self, vw, vh, screen):
        self.view_width = vw
        self.view_height = vh
        self.screen = screen
        self.mode = 2
        self.graph_engine = graph_engine.Graphical_Engine(vw, vh, screen)
        self.graph_engine.mode = self.mode
        self.game = game.Game(vw, vh, screen, self.graph_engine)

        self.dx = 0
        self.dy = 0
        self.mouse_clock = pygame.time.Clock()
        self.mouse_velocity = 10

    def prepare(self):
        if self.mode == 1:
            pass
        elif self.mode == 2:
            self.game.prepare()

    def pass_to_game_right(self):
        dt = self.mouse_clock.tick() / 1000
        self.game.pass_right(self.dx * dt * self.mouse_velocity, self.dy * dt * self.mouse_velocity)

    def update(self):
        if self.mode == 1:
            pass
        elif self.mode == 2:
            if main.game.right:
                self.pass_to_game_right()
            self.game.update()


if __name__ == '__main__':

    pygame.init()
    size = width, height = 1200, 700
    screen = pygame.display.set_mode(size)
    main = Main(width, height, screen)
    main.prepare()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left
                    if main.mode == 2:
                        main.game.left = True
                        if not main.game.map.player.isFlying:
                            main.graph_engine.isAiming = True
                        main.game.pass_left(event.pos[0], event.pos[1])
                elif event.button == 3:  # right
                    if main.mode == 2:
                        main.game.right = True
                        main.mouse_clock.tick()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if main.mode == 2:
                        main.game.left = False
                        main.graph_engine.isAiming = False
                        main.game.pass_left(event.pos[0], event.pos[1])
                elif event.button == 3:
                    if main.mode == 2:
                        main.game.right = False
                        main.dx = 0
                        main.dy = 0

            if event.type == pygame.MOUSEMOTION:
                if main.mode == 2:
                    if main.game.left:
                        main.game.pass_left(event.pos[0], event.pos[1])
                    else:
                        main.dx += event.rel[0]
                        main.dy -= event.rel[1]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if main.mode == 2:
                        main.game.camera.change_state()
        main.update()
        pygame.display.flip()

    pygame.quit()
