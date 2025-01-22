from Code.Variables.SettingsVariables import *


class EventManager:
          def __init__(self, game):
                    self.game = game

                    cooldown = General_Settings['cooldowns'][0]
                    current_time = pygame.time.get_ticks() / 1000

                    self.fullscreen_timer = Timer(cooldown, current_time)
                    self.fps_timer = Timer(cooldown, current_time)
                    self.settings_timer = Timer(cooldown, current_time)

          def handle_quitting(self):
                    for event in pygame.event.get():
                              if event.type == pygame.QUIT or self.game.keys[Keys['escape']]:
                                        self.game.running = False

          def toggle_fullscreen(self):
                    current_time = pygame.time.get_ticks() / 1000
                    if self.game.keys[Keys['fullscreen']] and self.fullscreen_timer.check(current_time):
                              pygame.display.toggle_fullscreen()
                              self.fullscreen_timer.reactivate(current_time)

          def toggle_fps(self):
                    current_time = pygame.time.get_ticks() / 1000
                    if self.game.keys[Keys['fps']] and self.fps_timer.check(current_time) and not self.game.in_menu:
                              self.game.ui_manager.fps_enabled = not self.game.ui_manager.fps_enabled
                              self.fps_timer.reactivate(current_time)

          def toggle_grab(self):
                    if self.game.mouse_state[0] and not self.game.changing_settings and not self.game.in_menu:
                              pygame.event.set_grab(True)
                    elif self.game.keys[Keys['ungrab']] or self.game.in_menu:
                              pygame.event.set_grab(False)

          def toggle_settings(self):
                    current_time = pygame.time.get_ticks() / 1000
                    if self.game.keys[Keys['ungrab']] and self.settings_timer.check(current_time) and not self.game.in_menu:
                              self.game.changing_settings = not self.game.changing_settings
                              self.settings_timer.reactivate(current_time)

          def handle_events(self):
                    self.handle_quitting()
                    self.toggle_grab()
                    self.toggle_fullscreen()
                    self.toggle_settings()
                    self.toggle_fps()
