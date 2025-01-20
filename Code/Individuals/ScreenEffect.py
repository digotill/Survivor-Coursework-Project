from Code.Variables.SettingsVariables import *

class ScreenEffect:
          def __init__(self, game, frames, animation_speed):
                    self.game = game
                    self.frame = 0
                    self.length = len(frames) - 1
                    self.images = frames
                    self.animation_speed = animation_speed

          def draw(self, order=1):
                    if 0 <= self.frame <= self.length:
                              self.game.ui_surface.blit(self.images[int(self.frame)])
                              self.frame += order * self.animation_speed * self.game.dt
                              return False
                    elif self.frame > self.length:
                              self.game.ui_surface.blit(self.images[self.length])
                              self.frame += order * self.animation_speed * self.game.dt
                              return True
                    else:
                              return True

          def draw_frame(self, frame):
                    self.game.ui_surface.blit(self.images[frame])
