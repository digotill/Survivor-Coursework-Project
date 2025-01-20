from Code.Variables.SettingsVariables import *


class EventManager:
          def __init__(self, game):
                    self.game = game

                    self.Last_Fullscreen = - General_Settings['cooldowns'][0]
                    self.Last_FPS_Toggle = -General_Settings['cooldowns'][0]
                    self.Last_Changing_settings = - General_Settings['cooldowns'][0]
                    self.Fullscreen_Cooldown = General_Settings['cooldowns'][0]
                    self.FPS_Cooldown = General_Settings['cooldowns'][0]
                    self.Changing_settings_Cooldown = General_Settings['cooldowns'][0]

                    pygame.display.toggle_fullscreen()
                    pygame.display.toggle_fullscreen()

          def handle_quitting(self):
                    for event in pygame.event.get():
                              if event.type == pygame.QUIT or self.game.keys[Keys['escape']]:
                                        self.game.running = False

          def fullscreen_toggle(self):
                    if self.game.keys[Keys[
                              'fullscreen']] and self.Last_Fullscreen + self.Fullscreen_Cooldown < pygame.time.get_ticks() / 1000:
                              pygame.display.toggle_fullscreen()
                              self.Last_Fullscreen = pygame.time.get_ticks() / 1000

          def update_fps_toggle(self):
                    if self.game.keys[Keys[
                              'fps']] and self.Last_FPS_Toggle + self.FPS_Cooldown < pygame.time.get_ticks() / 1000 and not self.game.in_menu:
                              self.game.ui_manager.fps_enabled = not self.game.ui_manager.fps_enabled
                              self.Last_FPS_Toggle = pygame.time.get_ticks() / 1000

          def update_grab(self):
                    if self.game.mouse_state[0] and not self.game.changing_settings and not self.game.in_menu:
                              pygame.event.set_grab(True)
                    elif self.game.keys[Keys['ungrab']]:
                              pygame.event.set_grab(False)
                    elif self.game.in_menu:
                              pygame.event.set_grab(False)

          def update_changing_settings(self):
                    if self.game.keys[Keys[
                              'ungrab']] and self.Last_Changing_settings + self.Changing_settings_Cooldown < pygame.time.get_ticks() / 1000 and not self.game.in_menu:
                              self.game.changing_settings = not self.game.changing_settings
                              self.Last_Changing_settings = pygame.time.get_ticks() / 1000

          def handle_all_events(self):
                    self.handle_quitting()
                    self.update_grab()
                    self.fullscreen_toggle()
                    self.update_changing_settings()
                    self.update_fps_toggle()
