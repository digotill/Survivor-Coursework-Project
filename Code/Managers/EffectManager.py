from Code.Variables.SettingsVariables import *
from Code.Individuals.Effect import *
from Code.DataStructures.HashMap import *


class EffectManager:
          def __init__(self, game):
                    self.game = game
                    # Initialize a spatial hash map for efficient effect management
                    self.grid = HashMap(self.game, GENERAL["hash_maps"][6])

          def update(self):
                    # Update all effects and remove those that have faded out
                    for effect in self.grid.items.copy():
                              effect.update()
                              # Remove effect if it has completely faded (alpha <= 0)
                              if effect.alpha <= 0 and effect in self.grid.items:
                                        self.grid.remove(effect)
                    # Rebuild the spatial hash map after updates
                    self.grid.rebuild()

          def draw(self):
                    # Draw all effects that are within the visible window
                    for effect in self.grid.window_query():
                              effect.draw()

          def add_effect(self, pos, direction, dictionary):
                    # Create a new effect and add it to the grid
                    effect = Effect(self.game, pos, direction, dictionary)
                    self.grid.insert(effect)
