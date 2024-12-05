from itertools import product
from Code.Variables.Variables import *


class SpatialHash:
          def __init__(self, game):
                    self.grid = {}
                    self.items = set()
                    self.game = game

          def rebuild(self):
                    self.grid = {}
                    for item in self.items: self.insert(item)

          @staticmethod
          def _rect_cells(rect):
                    x1, y1 = rect.topleft
                    x1 //= window_attributes['spatial_hash_map_size']
                    y1 //= window_attributes['spatial_hash_map_size']
                    x2, y2 = rect.bottomright
                    x2 = x2 // window_attributes['spatial_hash_map_size'] + 1
                    y2 = y2 // window_attributes['spatial_hash_map_size'] + 1
                    return product(range(x1, x2), range(y1, y2))

          def insert(self, entity):
                    self.items.add(entity)
                    for cell in self._rect_cells(entity.rect):
                              items = self.grid.get(cell)
                              if items is None:
                                        self.grid[cell] = [entity]
                              else:
                                        items.append(entity)

          def query(self, rect):
                    items = set()
                    for cell in self._rect_cells(rect): items.update(self.grid.get(cell, ()))
                    return items

          def remove(self, entity):
                    self.items.remove(entity)
                    for cell in self._rect_cells(entity.rect):
                              items = self.grid.get(cell)
                              if items is not None: items.remove(entity)

          def window_query(self):
                    items = set()
                    for cell in self._rect_cells(self.game.window.offset_rect): items.update(self.grid.get(cell, ()))
                    return items
