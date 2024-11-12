import pygame
from Initialize import *
from Entities import *


class BackgroundAndHud():
          def __init__(self, game):
                    self.game = game

          def update(self):
                    pass

          def draw_border(self):
                    self.game.display_screen.blit(border)

          def draw_bars(self):
                    pass



