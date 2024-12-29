import time
from Code.Variables.Variables import *


class EventManager:
          def __init__(self, game):
                    self.game = game
                    self.Last_Fullscreen = 0
                    self.Last_FPS_Toggle = 0
                    self.Last_Changing_settings = 0
                    self.Fullscreen_Toggled = START_FULLSCREEN
                    self.Fullscreen_Cooldown = Cooldowns['fullscreen']
                    self.FPS_Cooldown = Cooldowns['fps']
                    self.Changing_settings_Cooldown = Cooldowns['settings']

          def handle_events(self):
                    for event in pygame.event.get():
                              if event.type == pygame.QUIT or self.game.keys[Keys['escape']]:
                                        self.game.running = False

          def update_fps_toggle(self):
                    if self.game.keys[Keys[
                              'fps']] and self.Last_FPS_Toggle + self.FPS_Cooldown < pygame.time.get_ticks() / 1000:
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
                              'ungrab']] and self.Last_Changing_settings + self.Changing_settings_Cooldown < pygame.time.get_ticks() / 1000:
                              self.game.changing_settings = not self.game.changing_settings
                              self.Last_Changing_settings = pygame.time.get_ticks() / 1000
