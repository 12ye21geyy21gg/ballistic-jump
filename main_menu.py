import pygame


class Main_Menu:
    def __init__(self, vw, vh, screen):
        self.margin_vert = 75
        self.margin_hor = 200
        self.btw_btns = 25
        self.num_of_btns = 4
        self.view_width = vw
        self.view_height = vh
        self.screen = screen
        self.button_width = self.view_width - 2 * self.margin_hor
        self.button_height = (self.view_height - 2 * self.margin_vert - (
                self.num_of_btns - 1) * self.btw_btns) // self.num_of_btns
        self.prev_y = 0
        self.main_font = pygame.font.Font(None, 50)
        self.main_font.set_bold(False)
        self.active_color = (255, 255, 0)
        self.not_active = (255, 100, 0)

    def draw_button(self, pos, text=None, active=None):
        if active is None:
            pygame.draw.rect(self.screen, self.active_color, (
                (self.margin_hor, self.margin_vert + (self.button_height + self.btw_btns) * (pos - 1)),
                (self.button_width, self.button_height)), 0)
            pygame.draw.rect(self.screen, self.not_active, (
                (self.margin_hor, self.margin_vert + (self.button_height + self.btw_btns) * (pos - 1)),
                (self.button_width, self.button_height)), 5)
        else:
            pygame.draw.rect(self.screen, self.not_active, (
                (self.margin_hor, self.margin_vert + (self.button_height + self.btw_btns) * (pos - 1)),
                (self.button_width, self.button_height)), 0)
            pygame.draw.rect(self.screen, self.active_color, (
                (self.margin_hor, self.margin_vert + (self.button_height + self.btw_btns) * (pos - 1)),
                (self.button_width, self.button_height)), 5)
        if text is not None:
            i = self.main_font.render(text, 1, (0, 0, 0))
            r = i.get_rect()
            r.x = self.margin_hor + self.button_width // 2 - r.width // 2
            r.y = self.margin_vert + (self.button_height + self.btw_btns) * (
                    pos - 1) + self.button_height // 2 - r.height // 2
            self.screen.blit(i, r)

    def pass_coords(self, x, y):
        if x >= self.margin_hor and x <= self.margin_hor + self.button_width:
            if y >= self.margin_vert and y <= self.margin_vert + self.button_height:
                return 1  # resume
            elif y >= self.margin_vert + (self.button_height + self.btw_btns) and y <= self.margin_vert + (
                    self.button_height + self.btw_btns) + self.button_height:
                return 2  # store
            elif y >= self.margin_vert + (self.button_height + self.btw_btns) * 2 and y <= self.margin_vert + (
                    self.button_height + self.btw_btns) * 2 + self.button_height:
                return 3  # full restart
            elif y >= self.margin_vert + (self.button_height + self.btw_btns) * 3 and y <= self.margin_vert + (
                    self.button_height + self.btw_btns) * 3 + self.button_height:
                return 4  # quit
