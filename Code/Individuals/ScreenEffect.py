from Code.Variables.SettingsVariables import *

class ScreenEffect:
          def __init__(self, game, frames, animation_speed):
                    self.game = game
                    self.frame = 0
                    self.length = len(frames) - 1
                    self.images = frames
                    self.animation_speed = animation_speed
                    self.alpha = 0

          def draw(self, order=1, surface=None):
                    if surface is None:
                              surface = self.game.ui_surface
                    if 0 <= self.frame <= self.length:
                              self.blit(self.images[int(self.frame)], surface)
                              self.frame += order * self.animation_speed * self.game.dt
                              return False
                    elif self.frame > self.length:
                              self.blit(self.images[self.length], surface)
                              self.frame += order * self.animation_speed * self.game.dt
                              return True
                    else:
                              return True

          def blit(self, image, surface):
                    temp_surface = self.game.methods.get_transparent_image(image, self.alpha)
                    surface.blit(temp_surface)
