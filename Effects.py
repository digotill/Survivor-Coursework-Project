import pygame
from Initialize import *


class BackgroundAndHud:
          def __init__(self, game):
                    self.game = game
                    self.border = pygame.image.load("BG\\border.png").convert_alpha()

          def update(self):
                    pass

          def draw(self):
                    self.game.display_screen.blit(self.border)



