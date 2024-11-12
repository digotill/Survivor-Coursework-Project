import time

import pygame, queue
from Initialize import *
from Entities import *


class BackgroundAndHud():
          def __init__(self, game):
                    self.game = game
                    self.font = pygame.font.Font(FONT, 15)
                    self.fps_enabled = START_WITH_FPS
                    self.fps_queue = queue.Queue(5)
                    self.fps_queue.put(200)
                    self.health_bar_rect = Health_bar.get_rect()
                    self.stamina_bar_rect = Stamina_bar.get_rect()

          def update(self):
                    pass

          def draw_border(self):
                    self.game.display_screen.blit(border)

          def draw_bars(self):
                    if self.game.player.health > 0:
                              Health_bar_surface = pygame.Surface((self.health_bar_rect.width * self.game.player.health / PLAYER_HEALTH, self.health_bar_rect.height))
                              Health_bar_surface.blit(Health_bar)
                              self.game.display_screen.blit(Health_bar_surface, (55 - 0.5 * self.health_bar_rect.width, 27 - 0.5 * self.health_bar_rect.height))
                    if self.game.player.stamina > 0:
                              Stamina_bar_surface = pygame.Surface((self.stamina_bar_rect.width * self.game.player.stamina / PLAYER_STAMINA, self.stamina_bar_rect.height))
                              Stamina_bar_surface.blit(Stamina_bar)
                              self.game.display_screen.blit(Stamina_bar_surface, (REN_RES[0] - 55 - 0.5 * self.stamina_bar_rect.width, 27 - 0.5 * self.stamina_bar_rect.height))

          def draw_fps(self):
                    copy_fps_queue = self.fps_queue
                    total = 0
                    numbers_of_additions = 0
                    while not copy_fps_queue.empty():
                              total += copy_fps_queue.get()
                              numbers_of_additions += 1
                    total /= numbers_of_additions
                    if self.fps_enabled:
                              text = self.font.render(str(total), False, pygame.Color("orange"))
                              self.game.display_screen.blit(text, (32, 1))
                    if self.fps_queue.full():
                              self.fps_queue.get()
                    self.fps_queue.put(int(self.game.clock.get_fps()))
