from Code.Variables.SettingsVariables import *

class ScreenEffect:
          def __init__(self, frames):
                    self.frame = 0
                    self.length = len(frames) - 1
                    self.images = frames

          def draw(self, surface, animation_speed, dt):
                    if self.frame < self.length:
                              surface.blit(self.images[int(self.transition_frame) % self.length])
                              self.frame += animation_speed * dt
                              return True
                    else:
                              return False
