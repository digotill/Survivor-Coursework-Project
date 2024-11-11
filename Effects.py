import pygame
from Initialize import *


class BackgroundAndHud:
          def __init__(self, game):
                    self.game = game
                    self.border = pygame.image.load("BG\\border.png").convert_alpha()

          def update(self):
                    pass

          def draw(self):
                    self.game.display.blit(
                              pygame.transform.scale(self.border, (self.game.display.width, self.game.display.height)))
                    pygame.draw.rect(self.game.display, "red",
                                     pygame.Rect(89, 60, int((self.game.player.health / PLAYER_HEALTH) * 204), 20))
                    pygame.draw.rect(self.game.display, "blue", pygame.Rect(
                              self.game.display.width - 30 - int((self.game.player.stamina / PLAYER_STAMINA) * 280) - 3,
                              55, 267, 20))
                    self.game.display.blit(Health_bar, (10, 15))
                    self.game.display.blit(Mana_bar, (
                              self.game.display.width - 30 - int((self.game.player.stamina / PLAYER_STAMINA) * 300),
                              40 * 1080 / self.game.display.height))

                    #* 1920 / pygame.display.get_window_size()[0]
                    #* 1080 / pygame.display.get_window_size()[1]
                    #/ 1080 *
