from Code.Individuals.Parent import *

class Object(main):
          def __init__(self, game, image, res, pos, collisions):
                    self.game = game
                    self.original_image = image
                    self.image = image
                    self.res = v2(res)
                    self.collisions = collisions
                    self.pos = pos
                    self.rect = self.image.get_rect(center=self.pos)

          def draw(self, surface=None):
                    if surface is None:
                              surface = self.game.display_surface
                    draw_pos = self.rect.x - self.game.camera.offset_rect.x, self.rect.y - self.game.camera.offset_rect.y
                    self.game.display_surface.blit(self.image, draw_pos)
                    shadow_image = self.generate_shadow_image(self.image)
                    surface.blit(shadow_image, (draw_pos[0], draw_pos[1] + self.res[1] - shadow_image.height / 2))