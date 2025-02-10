from Code.DataStructures.HashMap import *
from Code.Individuals.Experience import *

class ExperienceManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(self.game, GENERAL["hash_maps"][7])
                    self.pool = set()

          def add_experience(self, name, location):
                    if bool(self.pool):
                              xp = self.pool.pop()
                              xp.reset(location, name)
                    else:
                              xp = Experience(self.game, location, name)
                              self.grid.insert(xp)

          def update(self):
                    for xp in self.grid.items.copy():
                              xp.update()
                              if xp.is_collected and xp in self.grid.items:
                                        self.grid.remove(xp)
                                        self.pool.add(xp)
                    self.grid.rebuild()
