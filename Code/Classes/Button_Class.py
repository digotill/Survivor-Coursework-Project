import pygame
from Code.Variables.Variables import *

class Button:
    def __init__(self, image, pos, game, text, text_input=None, font=None, base_color=None, hovering_color=None):
        self.game = game
        self.org_image = image
        self.original_pos = pos
        self.has_text = text
        self.text_input = text_input
        self.font_path = font
        self.base_color = base_color
        self.hovering_color = hovering_color

        self.update_size_and_position()

    def update_size_and_position(self):
        current_res = pygame.display.get_window_size()
        scale_x = current_res[0] / REN_RES[0]
        scale_y = current_res[1] / REN_RES[1]

        scaled_width = int(self.org_image.get_width() * scale_x)
        scaled_height = int(self.org_image.get_height() * scale_y)
        self.image = pygame.transform.scale(self.org_image, (scaled_width, scaled_height))

        self.x_pos = int(self.original_pos[0] * scale_x)
        self.y_pos = int(self.original_pos[1] * scale_y)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        if self.has_text:
            self.font_size = int(scaled_height / BUTTONS_SIZE / 2.1)
            self.font = pygame.font.Font(self.font_path, self.font_size)
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def draw(self):
        self.game.display.blit(self.image, self.rect)
        if self.has_text:
            self.game.display.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.has_text:
            if self.text_rect.collidepoint(position):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)

    def update_pos(self):
        self.update_size_and_position()