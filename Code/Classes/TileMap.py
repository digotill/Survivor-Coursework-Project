from pygame import Vector2
from Code.Variables.Variables import *
from Code.Utilities.Utils import *
from Code.Utilities.Grid import *
from Code.Variables.Initialize import *


class Tile:
          def __init__(self, image, position):
                    self.image = image
                    self.position = Vector2(position)
                    self.rect = pygame.Rect(self.position.x, self.position.y, TILEMAP_SIZE, TILEMAP_SIZE)

          def draw(self, surface, offset):
                    draw_position = self.position - offset
                    surface.blit(self.image, draw_position)


class TileMap:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    self.tile_size = TILEMAP_SIZE
                    self.tiles = {}
                    for x in range(PLAYABLE_AREA_SIZE[0] // self.tile_size):
                              for y in range(PLAYABLE_AREA_SIZE[1] // self.tile_size):
                                        self.add_tile(grass, (x * self.tile_size, y * self.tile_size))
                    self.grid.rebuild()

          def add_tile(self, image, position):
                    grid_x = position[0] // self.tile_size
                    grid_y = position[1] // self.tile_size
                    grid_position = (grid_x, grid_y)

                    tile = Tile(image, (grid_x * self.tile_size, grid_y * self.tile_size))

                    self.tiles[grid_position] = tile
                    self.grid.insert(tile)

          def get_tile(self, position):
                    grid_x = position[0] // self.tile_size
                    grid_y = position[1] // self.tile_size
                    return self.tiles.get((grid_x, grid_y))

          def draw(self):
                    for tile in self.grid.window_query():
                              tile.draw(self.game.display_screen, self.game.window.offset_rect.topleft)
