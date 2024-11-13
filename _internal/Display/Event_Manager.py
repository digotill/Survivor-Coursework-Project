import time
from _internal.Variables.Variables import *


class Event_Manager:
          def __init__(self, game):
                    self.game = game
                    self.Last_Fullscreen = 0
                    self.Last_FPS_Toggle = 0
                    self.Fullscreen_Toggled = START_FULLSCREEN
                    self.FPS_Toggled = START_WITH_FPS
                    self.Fullscreen_Cooldown = FULLSCREEN_COOLDOWN
                    self.FPS_Cooldown = FPS_COOLDOWN


          def update_window_events(self):
                    for event in pygame.event.get():
                              if event.type == pygame.QUIT or self.game.keys[ESCAPE_KEY]: self.game.running = False

          def update_size(self):
                    if self.game.keys[FULLSCREEN_KEY] and self.Last_Fullscreen + self.Fullscreen_Cooldown < time.time():
                              self.Fullscreen_Toggled = not self.Fullscreen_Toggled
                              if self.Fullscreen_Toggled:
                                        pygame.display.set_window_position((0, 0))
                                        self.game.display = pygame.display.set_mode(MAX_WIN_RES, pygame.NOFRAME)
                              else:
                                        pygame.display.set_window_position((MAX_WIN_RES[0] / 2 - REN_RES[0] / 2,
                                                                            MAX_WIN_RES[1] / 2 - REN_RES[1] / 2))
                                        self.game.display = pygame.display.set_mode(REN_RES, pygame.RESIZABLE)
                              self.Last_Fullscreen = time.time()

          def update_fps_toggle(self):
                    if self.game.keys[TOGGLE_FPS_KEY] and self.Last_FPS_Toggle + self.FPS_Cooldown < time.time():
                              self.game.background.fps_enabled = not self.game.background.fps_enabled
                              self.Last_FPS_Toggle = time.time()

          def update_grab(self):
                    if self.game.mouse_state[0]: pygame.event.set_grab(True)
                    elif self.game.keys[UNGRAB_KEY]: pygame.event.set_grab(False)


