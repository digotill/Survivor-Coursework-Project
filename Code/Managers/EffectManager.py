from Code.Variables.SettingsVariables import *
from Code.Individuals.Effect import *
from Code.DataStructures.HashMap import *


class EffectManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(self.game, General_Settings["hash_maps"][6])

          def update(self):
                    for effect in self.grid.items.copy():
                              effect.update()
                              if effect.alpha <= 0 and effect in self.grid.items: self.grid.remove(effect)
                    self.grid.rebuild()

          def draw(self):
                    array = self.grid.window_query()
                    for effect in array:
                              rect = pygame.Rect(effect.pos.x, effect.pos.y, effect.res[0] / 3, effect.res[1] / 3)
                              if not self.game.tilemap_manager.tile_collision(rect, "water_tile") or effect.frame < effect.end_frame:
                                        effect.draw()

          def add_effect(self, pos, direction, dictionary):
                    effect = Effect(self.game, pos, direction, dictionary)
                    self.grid.insert(effect)
