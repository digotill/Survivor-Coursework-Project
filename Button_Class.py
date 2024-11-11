import pygame
from Variables import *


class Button:
          def __init__(self, image, pos, game, text, text_input=None, font=None, base_color=None, hovering_color=None):
                    self.game = game
                    self.image = image
                    self.org_image = self.image
                    self.ratio_x = pos[0] / WIN_RES[0]
                    self.ratio_y = pos[1] / WIN_RES[1]
                    self.x_pos = pos[0]
                    self.y_pos = pos[1]
                    self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
                    self.has_text = text
                    if self.has_text is True:
                              self.font_size = int(self.image.height / 1.1)
                              self.font_path = font
                              self.font = pygame.font.Font(self.font_path, self.font_size)
                              self.base_color, self.hovering_color = base_color, hovering_color
                              self.text_input = text_input
                              self.text = self.font.render(self.text_input, False, self.base_color)
                              self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

          def draw(self):
                    self.game.display.blit(self.image, self.rect)
                    if self.has_text is True:
                              self.game.display.blit(self.text, self.text_rect)

          def check_for_input(self, position):
                    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                                      self.rect.bottom):
                              return True
                    return False

          def changeColor(self, position):
                    if self.has_text is True:
                              if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top,
                                                                                                      self.text_rect.bottom):
                                        self.text = self.font.render(self.text_input, False, self.hovering_color)
                              else:
                                        self.text = self.font.render(self.text_input, False, self.base_color)

          def update_pos(self):
                    self.x_pos = pygame.display.get_window_size()[0] * self.ratio_x
                    self.y_pos = pygame.display.get_window_size()[1] * self.ratio_y
                    self.image = pygame.transform.scale(self.org_image, (
                              self.org_image.get_width() * pygame.display.get_window_size()[0] / REN_RES[0],
                              self.org_image.get_height() * pygame.display.get_window_size()[1] / REN_RES[1]))
                    self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
                    if self.has_text is True:
                              self.font = pygame.font.Font(self.font_path, int(self.font_size * pygame.display.get_window_size()[1] / WIN_RES[1]))
                              self.text = self.font.render(self.text_input, False, self.base_color)
                              self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
