from Code.Classes.Entities import *


class UI:
          def __init__(self, game):
                    self.game = game
                    self.font = pygame.font.Font(general_settings['font'], general_settings["fps_size"])
                    self.fps_enabled = False
                    self.health_bar_rect = Health_bar.get_rect()
                    self.stamina_bar_rect = Stamina_bar.get_rect()
                    self.brightness = window_attributes['brightness']

          def draw_bars(self):
                    if self.game.player.health > 0:
                              health = self.game.player.health
                    else:
                              health = 1
                    Health_bar_surface = pygame.Surface((
                              self.health_bar_rect.width * health / self.game.player.max_health,
                              self.health_bar_rect.height))
                    Health_bar_surface.blit(Health_bar)
                    self.game.ui_surface.blit(Health_bar_surface, (
                              (ui["health_bar"][0] - 0.5 * self.health_bar_rect.width),
                              (ui["health_bar"][1] - 0.5 * self.health_bar_rect.height)))
                    self.game.ui_surface.blit(Outside_Health_bar, (
                              (ui["health_bar"][0] - 0.5 * Outside_Health_bar.get_rect().width + 1),
                              (ui["health_bar"][1] - 0.5 * Outside_Health_bar.get_rect().height)))
                    if self.game.player.stamina > 0:
                              stamina = self.game.player.stamina
                    else:
                              stamina = 1
                    Stamina_bar_surface = pygame.Surface(
                              (self.stamina_bar_rect.width * stamina / player_attributes['stamina'],
                               self.stamina_bar_rect.height))
                    Stamina_bar_surface.blit(Stamina_bar)
                    self.game.ui_surface.blit(Stamina_bar_surface, (
                              REN_RES[0] - (ui["stamina_bar"][0] + 0.5 * self.stamina_bar_rect.width),
                              (ui["stamina_bar"][1] - 0.5 * self.stamina_bar_rect.height)))
                    self.game.ui_surface.blit(pygame.transform.flip(Outside_Health_bar, True, False),
                                              (REN_RES[0] - (ui["stamina_bar"][0] + 0.5 *
                                                             Outside_Health_bar.get_rect().width) - 1,
                                               (ui["stamina_bar"][1] - 0.5 * Outside_Health_bar.get_rect().height)))

          def draw_fps(self):
                    if self.fps_enabled:
                              text = self.font.render(str(int(self.game.clock.get_fps())) + "  FPS", False,
                                                      pygame.Color("orange"))
                              center = ui["fps"][0], ui["fps"][1]
                              text_rect = text.get_rect(center=center)
                              self.game.ui_surface.blit(text, text_rect)

          def draw_time(self):
                    if self.fps_enabled:
                              text = self.font.render(str(int(self.game.game_time)) + " SECONDS", False,
                                                      pygame.Color("orange"))
                              text_rect = text.get_rect(center=(
                                        REN_RES[0] - ui["time"][0], ui["time"][1]))
                              self.game.ui_surface.blit(text, text_rect)

          def display_mouse(self):
                    if pygame.mouse.get_focused():
                              if self.game.mouse_state[0]:
                                        image = Cursor_Clicking
                              else:
                                        image = Cursor_Not_Clicking
                              new_image = pygame.transform.scale(image, (
                                        image.get_rect().width * self.game.display.width / REN_RES[0],
                                        image.get_rect().height * self.game.display.height / REN_RES[1]))
                              self.game.display.blit(new_image,
                                                     (self.game.mouse_pos[0] - new_image.get_rect().width / 2,
                                                      self.game.mouse_pos[1] - new_image.get_rect().height / 2))

          def darken_screen(self):
                    if self.game.changing_settings:
                              self.game.display_screen.fill(window_attributes['darkness'],
                                                            special_flags=pygame.BLEND_RGB_SUB)

          def draw_brightness(self):
                    if self.brightness == window_attributes['brightness']: return None
                    if self.brightness > window_attributes['brightness']:
                              self.game.display.fill([int(window_attributes['min_brightness'] * (
                                      self.brightness - window_attributes['brightness'])) for _ in range(3)],
                                                     special_flags=pygame.BLEND_RGB_ADD)
                    elif self.brightness < window_attributes['brightness']:
                              self.game.display.fill([int(window_attributes['max_brightness'] * (
                                      window_attributes['brightness'] - self.brightness)) for _ in range(3)],
                                                     special_flags=pygame.BLEND_RGB_SUB)
