from Code.Variables.SettingsVariables import *

class ScreenEffect:
          def __init__(self, game, frames, animation_speed):
                    self.game = game
                    self.frame = 0
                    self.length = len(frames) - 1
                    self.images = frames
                    self.animation_speed = animation_speed
                    self.opacity = 1

          def draw(self, order=1):
                    if 0 <= self.frame <= self.length:
                              self._blit_with_opacity(self.images[int(self.frame)])
                              self.frame += order * self.animation_speed * self.game.dt
                              return False
                    elif self.frame > self.length:
                              self._blit_with_opacity(self.images[self.length])
                              self.frame += order * self.animation_speed * self.game.dt
                              return True
                    else:
                              return True

          def draw_frame(self, frame):
                    if 0 <= frame <= self.length:
                              self._blit_with_opacity(self.images[frame])

          def _blit_with_opacity(self, image):
                    temp_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
                    temp_surface.fill((255, 255, 255, int(self.opacity * 255)))
                    temp_surface.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    self.game.ui_surface.blit(temp_surface, (0, 0))

          def set_opacity(self, opacity):
                    self.opacity = max(0, min(1, opacity))
