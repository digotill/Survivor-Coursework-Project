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




class Settings_Button:
    def __init__(self, game, image, pos, text, axis, axis_location, movement_time, text_input=None, font=None, base_color=None, hovering_color=None):
        self.game = game
        self.original_pos = pos
        self.image = image
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))
        self.has_text = text
        self.text_input = text_input
        self.font_path = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.active = False
        self.movement_time = movement_time
        self.axis = axis
        self.axis_location = axis_location
        if axis == "x":
            if axis_location == "max":
                self.starting_x = REN_RES[0] + self.rect.width * 0.5
            else:
                self.starting_x = -self.rect.width * 0.5
            self.starting_y = pos[1]
        elif axis == "y":
            self.starting_x = pos[0]
            if axis_location == "max":
                self.starting_y = REN_RES[1] + self.rect.height * 0.5
            else:
                self.starting_y = -self.rect.height * 0.5
        self.rect.center = (self.starting_x, self.starting_y)

        if self.has_text:
            self.font_size = int(self.rect.height / BUTTONS_SIZE / 2.1)
            self.font = pygame.font.Font(self.font_path, self.font_size)
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.text_rect = self.text.get_rect(center=(self.rect.centerx, self.rect.centery))

    def draw(self):
        if self.active:
            self.game.display_screen.blit(self.image, self.rect)
            if self.has_text:
                self.game.display_screen.blit(self.text, self.text_rect)

    def update(self):
              target_x = self.original_pos[0] if self.active else self.starting_x
              target_y = self.original_pos[1] if self.active else self.starting_y

              if self.axis == "x":
                        distance = (target_x - self.rect.centerx) / self.movement_time
                        self.rect.centerx += distance
              else:  # axis == "y"
                        distance = (target_y - self.rect.centery) / self.movement_time
                        self.rect.centery += distance

              # Ensure the button doesn't overshoot its target
              if self.active:
                        if self.axis == "x":
                                  if (self.axis_location == "max" and self.rect.centerx < target_x) or \
                                          (self.axis_location == "min" and self.rect.centerx > target_x):
                                            self.rect.centerx = target_x
                        else:
                                  if (self.axis_location == "max" and self.rect.centery < target_y) or \
                                          (self.axis_location == "min" and self.rect.centery > target_y):
                                            self.rect.centery = target_y
              else:
                        if self.axis == "x":
                                  if (self.axis_location == "max" and self.rect.centerx > target_x) or \
                                          (self.axis_location == "min" and self.rect.centerx < target_x):
                                            self.rect.centerx = target_x
                        else:
                                  if (self.axis_location == "max" and self.rect.centery > target_y) or \
                                          (self.axis_location == "min" and self.rect.centery < target_y):
                                            self.rect.centery = target_y

              self.text_rect.center = self.rect.center


    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.has_text:
            if self.text_rect.collidepoint(position):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)
