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

    def draw_button(self, pos, text=None):
        pygame.draw.rect(self.screen, pygame.Color('grey'), (
            (self.margin_hor, self.margin_vert + (self.button_height + self.btw_btns) * (pos - 1)),
            (self.button_width, self.button_height)), 0)
        if text is not None:
            r = text.get_rect()
            r.y = self.margin_vert + (self.button_height + self.btw_btns) * (pos - 1)
            pygame.blit(text, r)

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
