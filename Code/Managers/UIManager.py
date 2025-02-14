from Code.Variables.SettingVariables import *


class UIManager:
          def __init__(self, game):
                    self.game = game  # Store reference to the game instance
                    self.fps_enabled = False  # Flag to enable/disable FPS display
                    self.health_bar_rect = self.game.assets["health_bar"].get_rect()  # Get rect for health bar image
                    self.stamina_bar_rect = self.game.assets["stamina_bar"].get_rect()  # Get rect for stamina bar image
                    self.brightness = 50  # Default brightness value

          def draw_bars(self):
                    # Draw Health Bar
                    health = max(self.game.player.health, 1)  # Ensure health is at least 1
                    health_ratio = health / self.game.player.max_health  # Calculate health ratio
                    self._draw_bar(
                              bar_image=self.game.assets["health_bar"],  # Image for health bar
                              outer_image=self.game.assets["bar_outline"],  # Outline image for health bar
                              ratio=health_ratio,  # Ratio of current health to max health
                              position=MISC["ui_bars"],  # Position of health bar on screen
                              is_flipped=False  # Health bar is not flipped
                    )

                    # Draw Stamina Bar
                    stamina = max(self.game.player.stamina, 1)  # Ensure stamina is at least 1
                    stamina_ratio = stamina / PLAYER['stamina']  # Calculate stamina ratio
                    self._draw_bar(
                              bar_image=self.game.assets["stamina_bar"],  # Image for stamina bar
                              outer_image=self.game.assets["bar_outline"],  # Outline image for stamina bar
                              ratio=stamina_ratio,  # Ratio of current stamina to max stamina
                              position=MISC["ui_bars"],  # Position of stamina bar on screen
                              is_flipped=True  # Stamina bar is flipped
                    )

          def _draw_bar(self, bar_image, outer_image, ratio, position, is_flipped):
                    bar_rect = bar_image.get_rect()  # Get rect for bar image
                    outer_rect = outer_image.get_rect()  # Get rect for outer image

                    bar_surface = pygame.Surface((bar_rect.width, bar_rect.height), pygame.SRCALPHA)  # Create surface for bar

                    if is_flipped:
                              # For flipped bars (e.g., stamina), crop from the right
                              crop_rect = pygame.Rect(bar_rect.width * (1 - ratio), 0, bar_rect.width * ratio, bar_rect.height)
                              bar_surface.blit(bar_image, (bar_rect.width * (1 - ratio), 0), crop_rect)
                              bar_x = self.game.render_resolution[0] - (position[0] + 0.5 * bar_rect.width) + 1
                              outer_x = self.game.render_resolution[0] - (position[0] + 0.5 * outer_rect.width)
                    else:
                              # For non-flipped bars (e.g., health), crop from the left
                              crop_rect = pygame.Rect(0, 0, bar_rect.width * ratio, bar_rect.height)
                              bar_surface.blit(bar_image, (0, 0), crop_rect)
                              bar_x = position[0] - 0.5 * bar_rect.width
                              outer_x = position[0] - 0.5 * outer_rect.width + 1

                    bar_y = position[1] - 0.5 * bar_rect.height  # Calculate y position for bar
                    outer_y = position[1] - 0.5 * outer_rect.height  # Calculate y position for outer image

                    self.game.uiS.blit(bar_surface, (bar_x, bar_y))  # Draw bar on UI surface
                    if is_flipped:
                              outer_image = pygame.transform.flip(outer_image, True, False)  # Flip outer image if needed
                    self.game.uiS.blit(outer_image, (outer_x, outer_y))  # Draw outer image on UI surface

          def draw_fps(self):
                    if self.fps_enabled:  # Only draw FPS if enabled
                              fps = str(int(  # Get current FPS, clamped to min/max values
                                        max(min(BUTTONS["Sliders"]["fps"]["max_value"], self.game.clock.get_fps()),
                                            BUTTONS["Sliders"]["fps"]["min_value"])))
                              text = self.game.assets["font14"].render(fps + "  FPS", False, pygame.Color("orange"))  # Render FPS text
                              text_rect = text.get_rect(center=(MISC["ui_bars"][0], MISC["ui_bars"][1] - 20))  # Position FPS text
                              self.game.uiS.blit(text, text_rect)  # Draw FPS text on UI surface

          def draw_time(self):
                    if self.fps_enabled:  # Only draw time if FPS is enabled
                              text = self.game.assets["font14"].render(str(int(self.game.game_time)) + " SECONDS", False,
                                                                       pygame.Color("orange"))  # Render time text
                              text_rect = text.get_rect(center=(
                                        self.game.render_resolution[0] - MISC["ui_bars"][0], MISC["ui_bars"][1] - 20))  # Position time text
                              self.game.uiS.blit(text, text_rect)  # Draw time text on UI surface

          def display_mouse(self):
                    if pygame.mouse.get_focused():  # Only display cursor if mouse is focused
                              if self.game.inputM.get("left_click"):
                                        image = self.game.assets["cursor"][1]  # Use clicked cursor image
                              else:
                                        image = self.game.assets["cursor"][0]  # Use normal cursor image
                              self.game.uiS.blit(image,  # Draw cursor on UI surface
                                                 (self.game.inputM.get("position")[0] - image.get_rect().width / 2,
                                                  self.game.inputM.get("position")[1] - image.get_rect().height / 2))

          def darken_screen(self):
                    if self.game.changing_settings:  # Darken screen when changing settings
                              a = GENERAL['brightness'][2]
                              self.game.displayS.fill((a, a, a),
                                                      special_flags=pygame.BLEND_RGB_SUB)

          def draw_brightness(self):
                    if self.brightness == 50: return None  # No adjustment needed at 50% brightness
                    if self.brightness > 50:
                              # Increase brightness
                              self.game.displayS.fill([int(GENERAL['brightness'][1] * (
                                      self.brightness - 50)) for _ in range(3)],
                                                      special_flags=pygame.BLEND_RGB_ADD)
                    elif self.brightness < 50:
                              # Decrease brightness
                              self.game.displayS.fill([int(GENERAL['brightness'][0] * (
                                      50 - self.brightness)) for _ in range(3)],
                                                      special_flags=pygame.BLEND_RGB_SUB)

          def draw(self):
                    self.darken_screen()  # Apply screen darkening effect
                    self.draw_xp_underbar()   # Draw XP underbar
                    self.draw_bars()  # Draw health and stamina bars
                    self.draw_fps()  # Draw FPS counter
                    self.draw_time()  # Draw game time

          def update_display(self):
                    self.display_mouse()  # Display custom mouse cursor
                    self.draw_ui_surface()  # Draw UI elements
                    self.draw_brightness()  # Apply brightness adjustment
                    self.apply_color_filter()  # Apply color filter for color blindness modes

          def draw_xp_underbar(self):
                    if not self.game.in_menu and not self.game.died and not self.game.playing_transition:
                              rect = self.game.assets["xp_bar_outline"].get_rect(center=(MISC["xp_bar"][0] + self.game.assets["xp_bar_coloured"].width / 2 + 10, MISC["xp_bar"][1]))
                              self.game.uiS.blit(self.game.assets["xp_bar_outline"], rect)  # Draw UI bar on UI surface

          def draw_xp_bar(self):
                    if not self.game.in_menu and not self.game.died and not self.game.playing_transition:
                              res = self.game.assets["xp_bar_coloured"].width * max(min(self.game.player.xp / self.game.player.max_xp, 1), 0), self.game.assets["xp_bar_uncoloured"].height
                              surface = pygame.Surface(res)
                              surface.blit(self.game.assets["xp_bar_coloured"], (-self.game.assets["xp_bar_coloured"].width / 2 + res[0] / 2, 0))
                              rect = surface.get_rect(center=(MISC["xp_bar"][0] + self.game.assets["xp_bar_coloured"].width / 2 + 10, MISC["xp_bar"][1]))
                              self.game.uiS.blit(surface, rect)  # Draw UI bar on UI surface

          def apply_color_filter(self):
                    if self.game.colour_mode == 50:  # Normal vision, no filter applied
                              return

                    filter_surface = pygame.Surface(self.game.render_resolution, pygame.SRCALPHA)

                    if self.game.colour_mode < 50:  # Protanopia (red-green color blindness)
                              red_value = max(0, min(255, int(200 * self.game.colour_mode / 50)))
                              filter_color = (red_value, 255, 255, 255)
                    elif self.game.colour_mode > 50:  # Deuteranopia (another type of red-green color blindness)
                              green_value = max(0, min(255, int(200 * (100 - self.game.colour_mode) / 50)))
                              filter_color = (255, green_value, 255, 255)
                    else:
                              return  # This case shouldn't occur, but just in case

                    filter_surface.fill(filter_color)
                    self.game.displayS.blit(filter_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

          def draw_ui_surface(self):
                    self.game.displayS.blit(self.game.uiS, (0, 0))  # Draw UI surface on main display
                    self.game.uiS.fill((0, 0, 0, 0))  # Clear UI surface for next frame
