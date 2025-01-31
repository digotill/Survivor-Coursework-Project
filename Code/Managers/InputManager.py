from Code.DataStructures.Timer import *


class InputManager:
          def __init__(self, game):
                    self.game = game
                    self.keys = {
                              'move_up': Input(self.game, pygame.K_w),
                              'move_left': Input(self.game, pygame.K_a),
                              'move_down': Input(self.game, pygame.K_s),
                              'move_right': Input(self.game, pygame.K_d),
                              'sprint': Input(self.game, pygame.K_LSHIFT),
                              'dodge': Input(self.game, pygame.K_SPACE, 1),
                              'toggle_fullscreen': Input(self.game, pygame.K_F11, 0.5),
                              'toggle_fps': Input(self.game, pygame.K_F12, 0.2),
                              'quit': Input(self.game, pygame.K_F10),
                              'ungrab': Input(self.game, pygame.K_ESCAPE)
                    }
                    self.mouse = {
                              'left': False,
                              'right': False,
                              'position': v2(0, 0),
                              "rel_position": v2(0, 0)
                    }

          def update(self):
                    pass

          def update_keys(self):
                    pass

          def update_mouse(self):
                    pass


class Input:
          def __init__(self, game, pygame_input, cooldown=None):
                    self.game = game
                    self.input = pygame_input
                    self.state = False
                    self.timer = Timer(cooldown, self.game.ticks) if cooldown else None

          def update(self):
                    if self.timer is not None:
                              if self.timer.check(self.game.ticks):
                                        self.state = self.input
                              else:
                                        self.state = False
                    else:
                              self.state = self.input
