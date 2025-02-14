from Code.Variables.SettingVariables import *


class EventManager:
          def __init__(self, game):
                    self.game = game

                    current_time = self.game.ticks

                    self.fullscreen_timer = Timer(GENERAL['cooldowns'][0], current_time)  # Timer to prevent rapid fullscreen toggles
                    self.fps_timer = Timer(GENERAL['cooldowns'][0], current_time)  # Timer to prevent rapid FPS display toggles
                    self.settings_timer = Timer(GENERAL['cooldowns'][0], current_time)  # Timer to prevent rapid settings menu toggles

          def handle_quitting(self):
                    for event in pygame.event.get():
                              if event.type == pygame.QUIT or self.game.inputM.get("quit"):  # Check for quit events (window close or escape key)
                                        self.game.running = False

          def toggle_fullscreen(self):
                    current_time = self.game.ticks
                    if self.game.inputM.get("toggle_fullscreen") and self.fullscreen_timer.check(current_time):  # Toggle fullscreen if key pressed and cooldown elapsed
                              pygame.display.toggle_fullscreen()
                              self.fullscreen_timer.reactivate(current_time)  # Reset the cooldown timer

          def toggle_grab(self):
                    if self.game.inputM.get("left_click") and not self.game.changing_settings and not self.game.in_menu:  # Grab mouse if clicked and not in menus
                              pygame.event.set_grab(True)
                    elif self.game.inputM.get("ungrab") or self.game.in_menu:  # Release mouse grab if key pressed or in menu
                              pygame.event.set_grab(False)
                    if self.game.died:  # Release mouse if player died
                              pygame.event.set_grab(False)

          def toggle_fps(self):
                    current_time = self.game.ticks
                    if self.game.inputM.get("toggle_fps") and self.fps_timer.check(current_time) and not self.game.in_menu:  # Toggle FPS display if key pressed, cooldown elapsed, and not in menu
                              self.game.uiM.fps_enabled = not self.game.uiM.fps_enabled
                              self.fps_timer.reactivate(current_time)  # Reset the cooldown timer

          def toggle_settings(self):
                    current_time = self.game.ticks
                    if self.game.inputM.get("ungrab") and self.settings_timer.check(current_time) and not self.game.in_menu and not self.game.died:  # Toggle settings menu if conditions met
                              self.game.changing_settings = not self.game.changing_settings
                              self.settings_timer.reactivate(current_time)  # Reset the cooldown timer

          def handle_events(self):
                    self.handle_quitting()  # Check for quit events
                    self.toggle_grab()  # Manage mouse grabbing
                    self.toggle_fullscreen()  # Handle fullscreen toggling
                    self.toggle_settings()  # Manage settings menu access
                    self.toggle_fps()  # Toggle FPS display
