import pygame
from Code.Variables.Variables import *
from pygame.math import Vector2 as v2

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


class Paused_Buttons:
          def __init__(self, game, image, pos, res, text, axis, axis_location, speed, text_input=None, font=None,
                       base_color=None, hovering_color=None):
                    self.game = game
                    self.image = pygame.transform.scale(image, res)
                    self.rect = self.image.get_rect(center=pos)
                    self.original_pos = v2(pos)
                    self.has_text = text
                    self.text_input = text_input
                    self.font_path = font
                    self.base_color = base_color
                    self.hovering_color = hovering_color
                    self.active = False
                    self.speed = speed
                    self.axis = axis
                    self.axis_location = axis_location

                    self.starting_pos = self.calculate_starting_position()
                    self.current_pos = v2(self.starting_pos)
                    self.rect.center = self.current_pos

                    if self.has_text:
                              self.setup_text()

          def calculate_starting_position(self):
                    if self.axis == "x":
                              x = REN_RES[
                                            0] + self.rect.width / 2 + 1 if self.axis_location == "max" else -self.rect.width / 2 - 1
                              return x, self.original_pos.y
                    else:
                              y = REN_RES[
                                            1] + self.rect.height / 2 + 1 if self.axis_location == "max" else -self.rect.height / 2 - 1
                              return self.original_pos.x, y

          def setup_text(self):
                    self.font_size = int(self.rect.height / BUTTONS_SIZE )
                    self.font = pygame.font.Font(self.font_path, self.font_size)
                    self.text = self.font.render(self.text_input, True, self.base_color)
                    self.text_rect = self.text.get_rect(center=self.rect.center)

          def draw(self):
                    if self.is_visible_on_screen():
                              self.game.display_screen.blit(self.image, self.rect)
                              if self.has_text:
                                        self.game.display_screen.blit(self.text, self.text_rect)

          def is_visible_on_screen(self):
                    screen_rect = self.game.display_screen.get_rect()
                    return self.rect.colliderect(screen_rect)


          def update(self):
                    target = self.original_pos if self.active else v2(self.starting_pos)
                    distance = (target - self.current_pos).length()

                    speed_factor = min(distance / SETTINGS_BUTTON_FRICTION,
                                                 1)

                    direction = (target - self.current_pos).normalize() if distance > 0 else v2(0, 0)
                    movement = direction * self.speed * speed_factor * self.game.dt

                    if movement.length() > distance:
                              self.current_pos = target
                    else:
                              self.current_pos += movement

                    self.rect.center = self.current_pos
                    if self.has_text:
                              self.text_rect.center = self.rect.center

          def check_for_input(self):
                    return self.rect.collidepoint(self.game.correct_mouse_pos)

          def changeColor(self):
                    if self.has_text:
                              color = self.hovering_color if self.rect.collidepoint(self.game.correct_mouse_pos) else self.base_color
                              self.text = self.font.render(self.text_input, True, color)
                              self.text_rect = self.text.get_rect(center=self.rect.center)
