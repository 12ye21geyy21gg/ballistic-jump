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
            self.graph_engine.draw()
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
                                    main.mode = 1
                                    main.graph_engine.mode = 1
                                    main.graph_engine.paused = False
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
                                main.game.clock.tick()
                                main.game.portal_clock.tick()
                    elif main.mode == 1:
                        if not main.graph_engine.paused:
                            num = main.graph_engine.get_button(event.pos[0], event.pos[1])
                            main.game.store.buy(num, main.game.map.player, game)
                            pass
                        else:
                            choice = main.graph_engine.menu.pass_coords(event.pos[0], event.pos[1])
                            if choice == 1:
                                main.graph_engine.paused = False
                            elif choice == 2:
                                main.mode = 2
                                main.graph_engine.mode = 2
                                main.game.saver.save(main.game.save())
                                main.game.clock.tick()
                                main.game.portal_clock.tick()
                                main.graph_engine.paused = False  # back to game # add saving while in
                                if main.game.end:
                                    main.graph_engine.paused = True
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
                if main.graph_engine.paused:
                    main.graph_engine.active = main.game.graph_engine.menu.pass_coords(event.pos[0], event.pos[1])
                if main.mode == 1 and not main.graph_engine.paused:
                    main.graph_engine.active_store = main.graph_engine.get_button(event.pos[0], event.pos[1])



            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if main.mode == 2:
                        main.game.camera.change_state()
                if event.key == pygame.K_ESCAPE:
                    if main.mode == 2:
                        main.game.pause()
                    elif main.mode == 1:
                        if main.graph_engine.paused:
                            main.graph_engine.paused = False
                        else:
                            main.graph_engine.paused = True
                if event.key == pygame.K_SPACE:
                    if main.mode == 2:
                        main.game.use_first()
                if event.key == pygame.K_LSHIFT:
                    if main.mode == 2:
                        main.game.use_second()
                if event.key == pygame.K_LCTRL:
                    if main.mode == 2:
                        main.game.use_third()
        main.update()
        pygame.display.flip()

    pygame.quit()
