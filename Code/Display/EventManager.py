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
                              elif event.type == pygame.VIDEORESIZE:
                                        self.handle_resize(event.size)
                              elif event.type in (
                                        pygame.WINDOWMAXIMIZED, pygame.WINDOWMINIMIZED, pygame.WINDOWRESTORED):
                                        self.handle_window_state(event)

          def update_size(self, always_toggle=False):
                    if self.game.keys[Keys[
                              'fullscreen']] and self.Last_Fullscreen + self.Fullscreen_Cooldown < pygame.time.get_ticks() / 1000 or always_toggle:
                              self.Fullscreen_Toggled = not self.Fullscreen_Toggled
                              if self.Fullscreen_Toggled:
                                        pygame.display.set_window_position((0, 0))
                                        self.game.display = pygame.display.set_mode(MONITER_RES,
                                                                                    pygame.NOFRAME | pygame.DOUBLEBUF)
                              else:
                                        pygame.display.set_window_position((MONITER_RES[0] / 2 - MIN_WIN_RES[0] / 2,
                                                                            MONITER_RES[1] / 2 - MIN_WIN_RES[1] / 2))
                                        self.game.display = pygame.display.set_mode(MIN_WIN_RES,
                                                                                    pygame.RESIZABLE | pygame.DOUBLEBUF)
                              self.Last_Fullscreen = pygame.time.get_ticks() / 1000

          def handle_resize(self, size):
                    if not self.Fullscreen_Toggled:
                              aspect_ratio = MONITER_RES[0] / MONITER_RES[1]
                              new_w = max(MIN_WIN_RES[0], min(size[0], MONITER_RES[0]))
                              new_h = int(new_w / aspect_ratio)

                              if new_h < MIN_WIN_RES[1]:
                                        new_h = MIN_WIN_RES[1]
                                        new_w = int(new_h * aspect_ratio)
                              elif new_h > MONITER_RES[1]:
                                        new_h = MONITER_RES[1]
                                        new_w = int(new_h * aspect_ratio)

                              new_size = (new_w, new_h)

                              self.game.display = pygame.display.set_mode(new_size, pygame.RESIZABLE | pygame.DOUBLEBUF)

          def handle_window_state(self, event):
                    if event.type == pygame.WINDOWMAXIMIZED:
                              new_size = pygame.display.get_window_size()
                              self.handle_resize(new_size)
                    elif event.type == pygame.WINDOWRESTORED:
                              new_size = pygame.display.get_window_size()
                              self.handle_resize(new_size)

          def update_fps_toggle(self):
                    if self.game.keys[Keys[
                              'fps']] and self.Last_FPS_Toggle + self.FPS_Cooldown < pygame.time.get_ticks() / 1000:
                              self.game.ui.fps_enabled = not self.game.ui.fps_enabled
                              self.Last_FPS_Toggle = pygame.time.get_ticks() / 1000

          def update_grab(self):
                    if self.game.mouse_state[0] and not self.game.changing_settings and not self.game.in_menu:
                              pygame.event.set_grab(True)
                    elif self.game.keys[Keys['ungrab']]:
                              pygame.event.set_grab(False)

          def update_changing_settings(self):
                    if self.game.keys[Keys[
                              'ungrab']] and self.Last_Changing_settings + self.Changing_settings_Cooldown < pygame.time.get_ticks() / 1000 and not self.game.in_menu:
                              self.game.changing_settings = not self.game.changing_settings
                              self.Last_Changing_settings = pygame.time.get_ticks() / 1000
