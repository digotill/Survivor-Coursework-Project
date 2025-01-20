from Code.Variables.SettingsVariables import *

class ScreenEffect:
          def __init__(self, game, frames, animation_speed):
                    self.game = game
                    self.frame = 0
                    self.length = len(frames) - 1
                    self.images = frames
                    self.animation_speed = animation_speed

          def draw(self):
                    if self.frame < self.length:
                              self.game.ui_surface.blit(self.images[int(self.frame) % self.length])
                              self.frame += self.animation_speed * self.game.dt
                              return False
                    else:
                              return True
