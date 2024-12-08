from Code.Classes.Entities import *


class UI:
          def __init__(self, game):
                    self.game = game
                    self.font = pygame.font.Font(General_Settings['font'], General_Settings["fps_size"])
                    self.fps_enabled = False
                    self.health_bar_rect = Bar_Images["Health_bar"].get_rect()
                    self.stamina_bar_rect = Bar_Images["Stamina_bar"].get_rect()
                    self.brightness = General_Settings['brightness']

          def draw_bars(self):
                    if self.game.player.health > 0:
                              health = self.game.player.health
                    else:
                              health = 1
                    Health_bar_surface = pygame.Surface((
                              self.health_bar_rect.width * health / self.game.player.max_health,
                              self.health_bar_rect.height))
                    Health_bar_surface.blit(Bar_Images["Health_bar"])
                    self.game.ui_surface.blit(Health_bar_surface, (
                              (UI_Settings["health_bar"][0] - 0.5 * self.health_bar_rect.width),
                              (UI_Settings["health_bar"][1] - 0.5 * self.health_bar_rect.height)))
                    self.game.ui_surface.blit(Bar_Images["Outside_Health_bar"], (
                              (UI_Settings["health_bar"][0] - 0.5 * Bar_Images["Outside_Health_bar"].get_rect().width + 1),
                              (UI_Settings["health_bar"][1] - 0.5 * Bar_Images["Outside_Health_bar"].get_rect().height)))
                    if self.game.player.stamina > 0:
                              stamina = self.game.player.stamina
                    else:
                              stamina = 1
                    Stamina_bar_surface = pygame.Surface(
                              (self.stamina_bar_rect.width * stamina / Player_Attributes['stamina'],
                               self.stamina_bar_rect.height))
                    Stamina_bar_surface.blit(Bar_Images["Stamina_bar"])
                    self.game.ui_surface.blit(Stamina_bar_surface, (
                              REN_RES[0] - (UI_Settings["stamina_bar"][0] + 0.5 * self.stamina_bar_rect.width),
                              (UI_Settings["stamina_bar"][1] - 0.5 * self.stamina_bar_rect.height)))
                    self.game.ui_surface.blit(pygame.transform.flip(Bar_Images["Outside_Health_bar"], True, False),
                                              (REN_RES[0] - (UI_Settings["stamina_bar"][0] + 0.5 *
                                                             Bar_Images["Outside_Health_bar"].get_rect().width) - 1,
                                               (UI_Settings["stamina_bar"][1] - 0.5 * Bar_Images["Outside_Health_bar"].get_rect().height)))

          def draw_fps(self):
                    if self.fps_enabled:
                              text = self.font.render(str(int(self.game.clock.get_fps())) + "  FPS", False,
                                                      pygame.Color("orange"))
                              center = UI_Settings["fps"][0], UI_Settings["fps"][1]
                              text_rect = text.get_rect(center=center)
                              self.game.ui_surface.blit(text, text_rect)

          def draw_time(self):
                    if self.fps_enabled:
                              text = self.font.render(str(int(self.game.game_time)) + " SECONDS", False,
                                                      pygame.Color("orange"))
                              text_rect = text.get_rect(center=(
                                        REN_RES[0] - UI_Settings["time"][0], UI_Settings["time"][1]))
                              self.game.ui_surface.blit(text, text_rect)

          def display_mouse(self):
                    if pygame.mouse.get_focused():
                              if self.game.mouse_state[0]:
                                        image = Cursor_Images["Cursor_Clicking"]
                              else:
                                        image = Cursor_Images["Cursor_Not_Clicking"]
                              new_image = pygame.transform.scale(image, (
                                        image.get_rect().width * self.game.display.width / REN_RES[0],
                                        image.get_rect().height * self.game.display.height / REN_RES[1]))
                              self.game.display.blit(new_image,
                                                     (self.game.mouse_pos[0] - new_image.get_rect().width / 2,
                                                      self.game.mouse_pos[1] - new_image.get_rect().height / 2))

          def darken_screen(self):
                    if self.game.changing_settings:
                              self.game.display_screen.fill(General_Settings['darkness'],
                                                            special_flags=pygame.BLEND_RGB_SUB)

          def draw_brightness(self):
                    if self.brightness == General_Settings['brightness']: return None
                    if self.brightness > General_Settings['brightness']:
                              self.game.display.fill([int(General_Settings['min_brightness'] * (
                                      self.brightness - General_Settings['brightness'])) for _ in range(3)],
                                                     special_flags=pygame.BLEND_RGB_ADD)
                    elif self.brightness < General_Settings['brightness']:
                              self.game.display.fill([int(General_Settings['max_brightness'] * (
                                      General_Settings['brightness'] - self.brightness)) for _ in range(3)],
                                                     special_flags=pygame.BLEND_RGB_SUB)
