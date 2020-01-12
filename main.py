import pygame, graph_engine, game, saver, os


class Main:
    def __init__(self, vw, vh, screen):
        self.view_width = vw
        self.view_height = vh
        self.screen = screen
        self.mode = 2
        self.graph_engine = graph_engine.Graphical_Engine(vw, vh, screen)
        self.saver = saver.Saver()
        self.graph_engine.mode = self.mode
        self.game = game.Game(vw, vh, screen, self.graph_engine, self.saver)
        self.x0 = 0
        self.y0 = 0
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
        if not self.game.camera.followPlayer:
            dx = self.dx - self.x0
            dy = self.dy - self.y0
            dt = self.mouse_clock.tick() / 1000
            self.game.pass_right(dx * dt * self.mouse_velocity, dy * dt * self.mouse_velocity)

    def update(self):
        if self.mode == 1:
            pass
        elif self.mode == 2:
            if main.game.right:
                self.pass_to_game_right()
            self.game.update()


if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption('Ballistic Jumper')
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
                        if not main.graph_engine.paused:
                            main.game.left = True
                            if not main.game.map.player.isFlying:
                                main.graph_engine.isAiming = True
                            main.game.pass_left(event.pos[0], event.pos[1])
                        else:
                            choice = main.game.graph_engine.menu.pass_coords(event.pos[0], event.pos[1])
                            main.game.left = False
                            if choice is not None:
                                if choice == 1:
                                    if main.game.end:
                                        main.game.restart()
                                        main.game.prepare()
                                    main.graph_engine.paused = False
                                elif choice == 2:
                                    pass
                                elif choice == 3:
                                    # delete save
                                    if os.path.isfile('data/save.dat'):
                                        os.remove('data/save.dat')
                                    main.game = game.Game(main.view_width, main.view_height, main.screen,
                                                          main.graph_engine, main.saver)
                                    main.game.prepare()
                                    main.graph_engine.paused = False
                                elif choice == 4:
                                    running = False
                elif event.button == 3:  # right
                    if main.mode == 2:
                        main.game.right = True
                        main.mouse_clock.tick()
                        main.x0 = event.pos[0]
                        main.y0 = height - event.pos[1]
                        main.dx = main.x0
                        main.dy = main.y0
                elif event.button == 5:
                    if main.mode == 2:
                        main.game.pass_player(event.pos[0], height - event.pos[1])
                # print(event.button)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if main.mode == 2:
                        if main.game.left and not main.game.map.player.isFlying:
                            main.game.left = False
                            main.graph_engine.isAiming = False
                            main.game.pass_left(event.pos[0], event.pos[1])

                elif event.button == 3:
                    if main.mode == 2:
                        main.game.right = False
                        main.x0 = 0
                        main.y0 = 0
                        main.dx = 0
                        main.dy = 0
                        main.game.rx = 0
                        main.game.ry = 0
                        main.game.camera.dx = 0
                        main.game.camera.dy = 0

            if event.type == pygame.MOUSEMOTION:
                if main.mode == 2:
                    if main.game.left:
                        main.game.pass_left(event.pos[0], event.pos[1])
                    elif main.game.right:
                        main.dx = event.pos[0]
                        main.dy = height - event.pos[1]


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if main.mode == 2:
                        main.game.camera.change_state()
                if event.key == pygame.K_ESCAPE:
                    if main.mode == 2:
                        main.game.pause()
                if event.key == pygame.K_SPACE:
                    if main.mode == 2:
                        main.game.use_first()
                if event.key == pygame.K_LSHIFT:
                    if main.mode == 2:
                        main.game.use_second()
        main.update()
        pygame.display.flip()

    pygame.quit()
