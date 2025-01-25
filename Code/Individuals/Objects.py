from Code.Variables.SettingsVariables import *

class Object:
          def __init__(self, game, image, res, pos):
                    self.game = game
                    self.original_image = image
                    self.image = image
                    self.res = v2(res)
                    self.pos = pos
                    self.rect = self.image.get_rect(center=self.pos)

          def draw(self, surface=None):
                    if surface is None:
                              surface = self.game.display_surface
                    draw_pos = self.rect.x - self.game.camera.offset_rect.x, self.rect.y - self.game.camera.offset_rect.y
                    surface.blit(self.image, draw_pos)

          def draw_shadow(self, surface=None):
                    if surface is None:
                              surface = self.game.display_surface
                    shadow_image = self.game.methods.get_shadow_image(self, self.image)
                    surface.blit(shadow_image, (self.rect.x, self.rect.y + self.res[1] - shadow_image.height))