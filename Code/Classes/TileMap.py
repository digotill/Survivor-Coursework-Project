from pygame import Vector2
from perlin_noise import PerlinNoise
from Code.Utilities.Grid import *


class Tile:
          def __init__(self, game, tile_type, position):
                    self.game = game
                    self.tile_type = tile_type
                    self.position = Vector2(position)
                    self.size = General_Settings["hash_maps"][2]
                    self.rect = pygame.Rect(self.position.x, self.position.y, self.size - 1, self.size - 1)
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

                    self.tile_size = General_Settings["hash_maps"][2]
                    self.grid = HashMap(game, self.tile_size)
                    self.grid2 = HashMap(game, self.tile_size)
                    self.width = GAME_SIZE[0] // self.tile_size + 1
                    self.height = GAME_SIZE[1] // self.tile_size + 1

                    self.animation_speed = Tiles_Congifig["animation_speed"]
                    self.frames = {tile_type: 0 for tile_type in Tiles_Congifig["animated_tiles"]}
                    self.perlin_noise = PerlinNoise(Perlin_Noise["overworld_map"][1], random.randint(0, 100000))

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
                    noise_value = self.perlin_noise([x * Perlin_Noise["overworld_map"][0], y * Perlin_Noise["overworld_map"][0]])
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

          def apply_transition_tiles(self, transition_array, count=0):
                    directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]  # "top", "bottom", "right", "left"
                    for tile in self.grid.items:
                              if tile.tile_type == transition_array[1]:
                                        grid_x, grid_y = int(tile.position.x // self.tile_size), int(tile.position.y // self.tile_size)
                                        neighbours = [self.get((grid_x + dx, grid_y + dy)) for dx, dy in directions]

                                        def neighbor_value(n):
                                                  if not n or n.tile_type != transition_array[1]:
                                                            return '0'
                                                  return '2' if count > 2 and n.transition else '1'

                                        neighbours_string = ''.join(map(neighbor_value, neighbours))

                                        if neighbours_string in ["1100", "0011", "0000", "1000", "0100", "0010", "0001"] and count == 0:
                                                  tile.images = [self.game.assets[transition_array[0]][0].copy()]
                                                  tile.tile_type = transition_array[0]
                                        elif neighbours_string in ["1101", "1011", "0111", "1110"] and count == 1:
                                                  self.add_grid2_tile(tile, grid_x, grid_y, transition_array, neighbours_string)
                                        elif neighbours_string in ["0101", "0110", "1001", "1010"] and count == 2:
                                                  self.add_grid2_tile(tile, grid_x, grid_y, transition_array, neighbours_string)
                                        elif neighbours_string in ["2121", "2112", "1221", "1212", "1222", "2122", "2212", "2221", "2222"] and count == 3:
                                                  neighbour_check = self.check_corners(tile)
                                                  if neighbour_check is not True:
                                                            self.add_grid2_tile(tile, grid_x, grid_y, transition_array, neighbour_check)

                    count += 1
                    if count < 4:
                              self.apply_transition_tiles(transition_array, count)
                    self.grid2.rebuild()

          def check_corners(self, tile):
                    grid_x, grid_y = int(tile.position.x // self.tile_size), int(tile.position.y // self.tile_size)
                    neighbours = [self.get((grid_x + dx, grid_y + dy)) for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]]
                    return_data = []
                    for neighbour in neighbours:
                              if neighbour is None or neighbour.tile_type != tile.tile_type:
                                        return_data.append(["2112", "2121", "1212", "1221"][neighbours.index(neighbour)])
                    if len(return_data) == 0: return True
                    elif len(return_data) == 1: return return_data[0]
                    elif "2112" in return_data: return "1"
                    else: return "2"

          def add_grid2_tile(self, tile, grid_x, grid_y, transition_array, index):
                    pixel_position = (grid_x * self.tile_size, grid_y * self.tile_size)
                    new_tile = Tile(self.game, transition_array[0], pixel_position)
                    new_tile.images = self.game.assets[transition_array[0][:6] + "tileset"][index]
                    tile.transition = True
                    self.grid2.insert(new_tile)

          def terrain_generator(self):
                    for x in range(self.width):
                              for y in range(self.height):
                                        tile_type = self.get_tile_type(x, y)
                                        self.add_tile(tile_type, (x, y))

                    for array in Tiles_Congifig["transitions"]: self.apply_transition_tiles(array)

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
