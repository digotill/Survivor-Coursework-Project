from Code.Classes.Entities import *


class UI:
          def __init__(self, game):
                    self.game = game
                    self.font = pygame.font.Font(Font_Config['font'], UI_Settings["fps_time_size"])
                    self.fps_enabled = False
                    self.health_bar_rect = Bar_Images["Health_bar"].get_rect()
                    self.stamina_bar_rect = Bar_Images["Stamina_bar"].get_rect()
                    self.brightness = General_Settings['brightness']

          def draw_bars(self):
                    # Draw Health Bar
                    health = max(self.game.player.health, 1)
                    health_ratio = health / self.game.player.max_health
                    self._draw_bar(
                              bar_image=Bar_Images["Health_bar"],
                              outer_image=Bar_Images["Outside_Health_bar"],
                              ratio=health_ratio,
                              position=UI_Settings["health_bar"],
                              is_flipped=False
                    )

                    # Draw Stamina Bar
                    stamina = max(self.game.player.stamina, 1)
                    stamina_ratio = stamina / Player_Attributes['stamina']
                    self._draw_bar(
                              bar_image=Bar_Images["Stamina_bar"],
                              outer_image=Bar_Images["Outside_Health_bar"],
                              ratio=stamina_ratio,
                              position=UI_Settings["stamina_bar"],
                              is_flipped=True
                    )

          def _draw_bar(self, bar_image, outer_image, ratio, position, is_flipped):
                    bar_rect = bar_image.get_rect()
                    outer_rect = outer_image.get_rect()

                    bar_surface = pygame.Surface((bar_rect.width * ratio, bar_rect.height))
                    bar_surface.blit(bar_image, (0, 0))

                    if is_flipped:
                              bar_x = REN_RES[0] - (position[0] + 0.5 * bar_rect.width)
                              outer_x = REN_RES[0] - (position[0] + 0.5 * outer_rect.width) - 1
                    else:
                              bar_x = position[0] - 0.5 * bar_rect.width
                              outer_x = position[0] - 0.5 * outer_rect.width + 1

                    bar_y = position[1] - 0.5 * bar_rect.height
                    outer_y = position[1] - 0.5 * outer_rect.height

                    self.game.ui_surface.blit(bar_surface, (bar_x, bar_y))
                    if is_flipped:
                              outer_image = pygame.transform.flip(outer_image, True, False)
                    self.game.ui_surface.blit(outer_image, (outer_x, outer_y))

          def draw_fps(self):
                    if self.fps_enabled:
                              fps = str(int(
                                        max(min(AllButtons["Sliders"]["fps"]["max_value"], self.game.clock.get_fps()),
                                            AllButtons["Sliders"]["fps"]["min_value"])))
                              text = self.font.render(fps + "  FPS", False,
                                                      pygame.Color("orange"))
                              text_rect = text.get_rect(center=UI_Settings["fps"])
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
                                        image = Cursor_Config["Cursor_Images"][1]
                              else:
                                        image = Cursor_Config["Cursor_Images"][0]
                              new_image = pygame.transform.scale(image, (
                                        image.get_rect().width * 1 / self.game.window_ratio,
                                        image.get_rect().height * 1 / self.game.window_ratio))
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
