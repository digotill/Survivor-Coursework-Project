from pygame import Vector2

from Code.Utilities.Grid import *
from Code.Variables.Initialize import *


class Tile:
          def __init__(self, image, position):
                    self.image = image
                    self.position = Vector2(position)
                    self.rect = pygame.Rect(self.position.x, self.position.y, window_attributes['tilemap_size'],
                                            window_attributes['tilemap_size'])

          def draw(self, surface, offset):
                    draw_position = self.position - offset
                    surface.blit(self.image, draw_position)


class TileMap:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    self.tile_size = window_attributes['tilemap_size']
                    for x in range(PLAYABLE_AREA_SIZE[0] // self.tile_size):
                              for y in range(PLAYABLE_AREA_SIZE[1] // self.tile_size):
                                        self.add_tile(Grass_Tile, (x * self.tile_size, y * self.tile_size))
                    self.grid.rebuild()

          def add_tile(self, image, position):
                    grid_x = position[0] // self.tile_size
                    grid_y = position[1] // self.tile_size

                    tile = Tile(image, (grid_x * self.tile_size, grid_y * self.tile_size))

                    self.grid.insert(tile)

          def draw(self):
                    for tile in self.grid.window_query():
                              tile.draw(self.game.display_screen, self.game.window.offset_rect.topleft)
