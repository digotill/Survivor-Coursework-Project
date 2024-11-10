import pygame
from Variables import *

class Button:
          def __init__(self, image, ratiox, ratioy, game):
                    self.game = game
                    self.image = image
                    self.org_image = self.image
                    self.ratio_x = ratiox
                    self.ratio_y = ratioy
                    self.x_pos = ratiox * game.screen.get_width()
                    self.y_pos = ratioy * game.screen.get_height()
                    self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

          def update(self):
                    self.game.display.blit(self.image, self.rect)

          def check_for_input(self, position):
                    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                                      self.rect.bottom):
                              return True
                    return False

          def update_pos(self, width, height):
                    self.x_pos = pygame.display.get_window_size()[0] * self.ratio_x
                    self.y_pos = pygame.display.get_window_size()[1] * self.ratio_y
                    self.image = pygame.transform.scale(self.org_image, (
                              self.org_image.get_width() * width / 1920,
                              self.org_image.get_height() * height / 1080))
                    self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

