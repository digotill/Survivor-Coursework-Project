import time

import pygame, queue
from _internal.Variables.Variables import *
from _internal.Classes.Entities import *


class BackgroundAndHud():
          def __init__(self, game):
                    self.game = game
                    self.font = pygame.font.Font(FONT, int(FPS_AND_TIME_SIZE * REN_RES[0] / 640))
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
                              Health_bar_surface = pygame.Surface((
                                        self.health_bar_rect.width * self.game.player.health / PLAYER_HEALTH * REN_RES[0] / 640,
                                        self.health_bar_rect.height * REN_RES[0] / 640))
                              Health_bar_surface.blit(Health_bar)
                              self.game.display_screen.blit(Health_bar_surface, (
                                        (HEALTH_BAR_POS[0] - 0.5 * self.health_bar_rect.width) * REN_RES[0] / 640, (HEALTH_BAR_POS[1] - 0.5 * self.health_bar_rect.height) * REN_RES[0] / 640))
                    if self.game.player.stamina > 0:
                              Stamina_bar_surface = pygame.Surface((
                                        self.stamina_bar_rect.width * self.game.player.stamina / PLAYER_STAMINA * REN_RES[0] / 640,
                                        self.stamina_bar_rect.height * REN_RES[0] / 640))
                              Stamina_bar_surface.blit(Stamina_bar)
                              self.game.display_screen.blit(Stamina_bar_surface, (
                                        REN_RES[0] - (STAMINA_BAR_POS[0] + 0.5 * self.stamina_bar_rect.width) * REN_RES[0] / 640,
                                        (STAMINA_BAR_POS[1] - 0.5 * self.stamina_bar_rect.height) * REN_RES[0] / 640))

          def draw_fps(self):
                    copy_fps_queue = self.fps_queue
                    total = 0
                    numbers_of_additions = 0
                    while not copy_fps_queue.empty():
                              total += copy_fps_queue.get()
                              numbers_of_additions += 1
                    total /= numbers_of_additions
                    if self.fps_enabled:
                              text = self.font.render(str(total) + "  FPS", False, pygame.Color("orange"))
                              center = FPS_POS[0] * REN_RES[0] / 640, FPS_POS[1] * REN_RES[0] / 640
                              text_rect = text.get_rect(center=center)
                              self.game.display_screen.blit(text, text_rect)
                    if self.fps_queue.full():
                              self.fps_queue.get()
                    self.fps_queue.put(int(self.game.clock.get_fps()))

          def draw_time(self):
                    text = self.font.render(str(int(self.game.game_time)) + " SECONDS", False,
                                            pygame.Color("orange"))
                    text_rect = text.get_rect(center=(REN_RES[0] - TIME_POS[0] * REN_RES[0] / 640, TIME_POS[1] * REN_RES[0] / 640))
                    self.game.display_screen.blit(text, text_rect)
