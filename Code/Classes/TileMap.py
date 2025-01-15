from pygame import Vector2
from perlin_noise import PerlinNoise
from Code.Utilities.Grid import *


class Tile:
          def __init__(self, game, tile_type, position):
                    self.game = game
                    self.tile_type = tile_type
                    self.position = Vector2(position)
                    self.size = General_Settings['tilemap_size']
                    self.rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
                    if tile_type in Tiles_Congifig["animated_tiles"]:
                              self.images = self.game.assets[tile_type]
                    else:
                              self.images = [random.choice(self.game.assets[tile_type])]
                    self.transition = False

          def draw(self, surface, offset, frame):
                    draw_position = self.position - offset
                    surface.blit(self.images[int(frame % len(self.images))], draw_position)


class TileMap:
          def __init__(self, game):
                    self.game = game

                    self.tile_size = 16
                    self.grid = HashMap(game, self.tile_size)
                    self.grid2 = HashMap(game, self.tile_size)
                    self.width = GAME_SIZE[0] // self.tile_size + 1
                    self.height = GAME_SIZE[1] // self.tile_size + 1

                    self.animation_speed = Tiles_Congifig["animation_speed"]
                    self.frames = {tile_type: 0 for tile_type in Tiles_Congifig["animated_tiles"]}
                    self.perlin_noise = PerlinNoise(1, random.randint(0, 100000))

                    self.terrain_generator()
                    self.grass_generator()

                    self.grid.rebuild()

          def add_tile(self, tile_type, grid_position):
                    pixel_position = (grid_position[0] * self.tile_size, grid_position[1] * self.tile_size)
                    tile = Tile(self.game, tile_type, pixel_position)
                    self.grid.insert(tile)

          def draw(self):
                    if not self.game.changing_settings:
                              for tile_type in self.frames:
                                        self.frames[tile_type] += self.game.dt * self.animation_speed
                    for grid in [self.grid, self.grid2]:
                              for tile in grid.window_query():
                                        frame = self.frames.get(tile.tile_type, 0)
                                        tile.draw(self.game.display_screen, self.game.camera.offset_rect.topleft, frame)

          def get_tile_type(self, x, y):
                    noise_value = self.perlin_noise([x * 0.05, y * 0.05])
                    for tile in Tiles_Congifig["Tile_Ranges"].keys():
                              if noise_value < Tiles_Congifig["Tile_Ranges"][tile]:
                                        return tile

          def tile_collision(self, rect, *tile_types):
                    for tile in self.grid.query(rect):
                              for tile_type in tile_types:
                                        if tile.tile_type == tile_type:
                                                  return True
                    return False

          def get(self, grid_position):
                    pixel_position = (grid_position[0] * self.tile_size, grid_position[1] * self.tile_size)
                    tile = self.grid.grid.get(grid_position, None)
                    if isinstance(tile, list) and tile:
                              for i in tile:
                                        if i.rect.topleft == pixel_position:
                                                  return i
                    return None

          def apply_transition_tiles(self, transition_array, stop=False):
                    directions2 = [(0, -1), (0, 1), (1, 0), (-1, 0)]  # "top", "bottom", "right", "left"
                    t = "" if stop else "1"
                    for tile in self.grid.items:
                              if tile.tile_type == transition_array[1]:
                                        grid_x, grid_y = int(tile.position.x // self.tile_size), int(
                                                  tile.position.y // self.tile_size)
                                        neighbours = [
                                                  self.get((grid_x + dx, grid_y + dy))
                                                  for dx, dy in directions2
                                        ]
                                        neighbours_string = ''.join([
                                                  '2' if neighbour and neighbour.tile_type == transition_array[1] and neighbour.transition else
                                                  '1' if neighbour and neighbour.tile_type == transition_array[1] else
                                                  '0'
                                                  for neighbour in neighbours
                                        ])
                                        for key in self.game.assets[transition_array[0][:6] + "tileset" + t].keys():
                                                  if stop:
                                                            print(key)
                                                  if key == neighbours_string:
                                                            pixel_position = (grid_x * self.tile_size,
                                                                              grid_y * self.tile_size)
                                                            new_tile = Tile(self.game, transition_array[0], pixel_position)
                                                            tile.transition = True
                                                            #tile.tile_type = transition_array[0]
                                                            new_tile.images = self.game.assets[transition_array[0][:6] + "tileset" + t][key]
                                                            self.grid2.insert(new_tile)

                    if not stop:
                              self.apply_transition_tiles(transition_array, True)
                    self.grid2.rebuild()

          def terrain_generator(self):
                    for x in range(self.width):
                              for y in range(self.height):
                                        tile_type = self.get_tile_type(x, y)
                                        self.add_tile(tile_type, (x, y))

                    for array in Tiles_Congifig["transitions"]:
                              self.apply_transition_tiles(array)

          def grass_generator(self):
                    for tile in self.grid.items:
                              if tile.tile_type == "Grass_Tile":
                                        v = random.random()
                                        if v < Grass["Density"]:
                                                  self.game.grass_manager.place_tile(
                                                            (tile.position.x // Grass["Grass_Settings"]["tile_size"],
                                                             tile.position.y // Grass["Grass_Settings"]["tile_size"]),
                                                            int(v * 12),
                                                            [0, 1, 2, 3, 4])
