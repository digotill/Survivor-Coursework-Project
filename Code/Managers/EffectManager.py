from Code.Variables.SettingsVariables import *
from Code.Individuals.Effect import *
from Code.DataStructures.HashMap import *


class EffectManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(self.game, GENERAL["hash_maps"][6])

          def update(self):
                    for effect in self.grid.items.copy():
                              effect.update()
                              if effect.alpha <= 0 and effect in self.grid.items: self.grid.remove(effect)
                    self.grid.rebuild()

          def draw(self):
                    for effect in self.grid.window_query():
                              effect.draw()

          def add_effect(self, pos, direction, dictionary):
                    effect = Effect(self.game, pos, direction, dictionary)
                    self.grid.insert(effect)
