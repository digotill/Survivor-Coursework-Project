import time

import pygame, queue
from Code.Variables.Variables import *
from Code.Classes.Entities import *


class UI:
          def __init__(self, game):
                    self.game = game
                    self.font = pygame.font.Font(FONT, int(FPS_AND_TIME_SIZE * REN_RES[0] / 640))
                    self.fps_enabled = START_WITH_FPS_AND_TIME
                    self.fps_queue = queue.Queue(5)
                    self.fps_queue.put(200)
                    self.health_bar_rect = Health_bar.get_rect()
                    self.stamina_bar_rect = Stamina_bar.get_rect()
                    self.current_border_frame = 0
                    self.brightness = INITIAL_BRIGHTNESS

          def draw_border(self):
                    self.game.ui_surface.blit(New_Border_Images[int(self.current_border_frame) % len(New_Border_Images)])
                    self.current_border_frame += BORDER_ANIMATION_SPEED * self.game.dt

          def draw_bars(self):
                    if self.game.player.health > 0:
                              health = self.game.player.health
                    else:
                              health = 1
                    Health_bar_surface = pygame.Surface((
                                        self.health_bar_rect.width * health / PLAYER_HEALTH,
                                        self.health_bar_rect.height))
                    Health_bar_surface.blit(Health_bar)
                    self.game.ui_surface.blit(Health_bar_surface, ((HEALTH_BAR_POS[0] - 0.5 * self.health_bar_rect.width) * REN_RES[0] / 640,
                                                                                 (HEALTH_BAR_POS[1] - 0.5 * self.health_bar_rect.height) * REN_RES[0] / 640 - 1))
                    self.game.ui_surface.blit(Outside_Health_bar, ((HEALTH_BAR_POS[0] - 0.5 * Outside_Health_bar.get_rect().width) * REN_RES[0] / 640,
                                                                                 (HEALTH_BAR_POS[1] - 0.5 * Outside_Health_bar.get_rect().height) * REN_RES[0] / 640 - 5))
                    if self.game.player.stamina > 0:
                              stamina = self.game.player.stamina
                    else:
                              stamina = 1
                    Stamina_bar_surface = pygame.Surface((
                                        self.stamina_bar_rect.width * stamina / PLAYER_STAMINA,
                                        self.stamina_bar_rect.height))
                    Stamina_bar_surface.blit(Stamina_bar)
                    self.game.ui_surface.blit(Stamina_bar_surface, (
                                        REN_RES[0] - (STAMINA_BAR_POS[0] + 0.5 * self.stamina_bar_rect.width) * REN_RES[0] / 640,
                                        (STAMINA_BAR_POS[1] - 0.5 * self.stamina_bar_rect.height) * REN_RES[0] / 640 - 1))
                    self.game.ui_surface.blit(pygame.transform.flip(Outside_Health_bar, True, False), (
                              REN_RES[0] - (STAMINA_BAR_POS[0] + 0.5 * Outside_Health_bar.get_rect().width) * REN_RES[0] / 640 - 2,
                              (STAMINA_BAR_POS[1] - 0.5 * Outside_Health_bar.get_rect().height) * REN_RES[0] / 640 - 5))

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
                              self.game.ui_surface.blit(text, text_rect)
                    if self.fps_queue.full():
                              self.fps_queue.get()
                    self.fps_queue.put(int(self.game.clock.get_fps()))

          def draw_time(self):
                    if self.fps_enabled:
                              text = self.font.render(str(int(self.game.game_time)) + " SECONDS", False,
                                            pygame.Color("orange"))
                              text_rect = text.get_rect(center=(REN_RES[0] - TIME_POS[0] * REN_RES[0] / 640, TIME_POS[1] * REN_RES[0] / 640))
                              self.game.ui_surface.blit(text, text_rect)

          def display_mouse(self):
                    if pygame.mouse.get_focused():
                              if self.game.mouse_state[0]: image = cursor1
                              else: image = cursor2
                              new_image = pygame.transform.scale(image, (image.get_rect().width * self.game.display.width / REN_RES[0],
                                                                         image.get_rect().height * self.game.display.height / REN_RES[1]))
                              self.game.display.blit(new_image, (self.game.mouse_pos[0] - new_image.get_rect().width / 2,
                                                                 self.game.mouse_pos[1] - new_image.get_rect().height / 2))

          def darken_screen(self):
                    if self.game.changing_settings:
                              self.game.display_screen.fill(SETTINGS_DARKENING, special_flags=pygame.BLEND_RGB_SUB)

          def draw_brightness(self):
                    if self.brightness == 50: return None
                    if self.brightness > 50: self.game.display.fill((int(MAX_BRIGHTNESS * (self.brightness - 50)), int(MAX_BRIGHTNESS * (self.brightness - 50)), int(MAX_BRIGHTNESS * (self.brightness - 50))), special_flags=pygame.BLEND_RGB_ADD)
                    elif self.brightness < 50: self.game.display.fill((int(MAX_DARKNESS * (50 - self.brightness)), int(MAX_DARKNESS * (50 - self.brightness)), int(MAX_DARKNESS * (50 - self.brightness))), special_flags=pygame.BLEND_RGB_SUB)
