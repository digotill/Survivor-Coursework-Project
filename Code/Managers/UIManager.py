from Code.Variables.SettingsVariables import *

class UIManager:
          def __init__(self, game):
                    self.game = game
                    self.fps_enabled = False
                    self.health_bar_rect = self.game.assets["health_bar"].get_rect()
                    self.stamina_bar_rect = self.game.assets["stamina_bar"].get_rect()
                    self.brightness = 50

          def draw_bars(self):
                    # Draw Health Bar
                    health = max(self.game.player.health, 1)
                    health_ratio = health / self.game.player.max_health
                    self._draw_bar(
                              bar_image=self.game.assets["health_bar"],
                              outer_image=self.game.assets["bar_outline"],
                              ratio=health_ratio,
                              position=UI_Settings["health_bar"],
                              is_flipped=False
                    )

                    # Draw Stamina Bar
                    stamina = max(self.game.player.stamina, 1)
                    stamina_ratio = stamina / Player_Attributes['stamina']
                    self._draw_bar(
                              bar_image=self.game.assets["stamina_bar"],
                              outer_image=self.game.assets["bar_outline"],
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
                              text = self.game.assets["font14"].render(fps + "  FPS", False,
                                                                       pygame.Color("orange"))
                              text_rect = text.get_rect(center=(UI_Settings["health_bar"][0], UI_Settings["health_bar"][1] - 20))
                              self.game.ui_surface.blit(text, text_rect)

          def draw_time(self):
                    if self.fps_enabled:
                              text = self.game.assets["font14"].render(str(int(self.game.game_time)) + " SECONDS", False,
                                                                       pygame.Color("orange"))
                              text_rect = text.get_rect(center=(
                                        REN_RES[0] - UI_Settings["stamina_bar"][0], UI_Settings["stamina_bar"][1] - 20))
                              self.game.ui_surface.blit(text, text_rect)

          def display_mouse(self):
                    if pygame.mouse.get_focused():
                              if self.game.mouse_state[0]:
                                        image = self.game.assets["cursor"][1]
                              else:
                                        image = self.game.assets["cursor"][0]
                              self.game.ui_surface.blit(image,
                                                        (self.game.correct_mouse_pos[0] - image.get_rect().width / 2,
                                                         self.game.correct_mouse_pos[1] - image.get_rect().height / 2))

          def darken_screen(self):
                    if self.game.changing_settings:
                              a = General_Settings['brightness'][2]
                              self.game.display_screen.fill((a, a, a),
                                                            special_flags=pygame.BLEND_RGB_SUB)

          def draw_brightness(self):
                    if self.brightness == 50: return None
                    if self.brightness > 50:
                              self.game.display_screen.fill([int(General_Settings['brightness'][1] * (
                                      self.brightness - 50)) for _ in range(3)],
                                                            special_flags=pygame.BLEND_RGB_ADD)
                    elif self.brightness < 50:
                              self.game.display_screen.fill([int(General_Settings['brightness'][0] * (
                                      50 - self.brightness)) for _ in range(3)],
                                                            special_flags=pygame.BLEND_RGB_SUB)

          def draw(self):
                    self.darken_screen()
                    self.draw_bars()
                    self.draw_fps()
                    self.draw_time()
