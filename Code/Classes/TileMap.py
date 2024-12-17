from pygame import Vector2

from Code.Utilities.Grid import *


class Tile:
          def __init__(self, tile_type, position):
                    self.tile_type = tile_type
                    self.position = Vector2(position)
                    self.size = General_Settings['tilemap_size']
                    self.rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
                    if tile_type in Tiles_Congifig["animated_tiles"]:
                              self.images = Tile_Images[tile_type]
                    else:
                              self.images = [random.choice(Tile_Images[tile_type])]
                    self.transition = None

          def draw(self, surface, offset, frame):
                    draw_position = self.position - offset
                    surface.blit(self.images[int(frame % len(self.images))], draw_position)


class TileMap:
          def __init__(self, game):
                    self.game = game

                    self.tile_size = 16
                    self.grid = HashMap(game, self.tile_size)
                    self.width = GAME_SIZE[0] // self.tile_size + 1
                    self.height = GAME_SIZE[1] // self.tile_size + 1

                    self.animation_speed = Tiles_Congifig["animation_speed"]
                    self.frames = {tile_type: 0 for tile_type in Tiles_Congifig["animated_tiles"]}

                    self.terrain_generator()
                    self.grass_generator()

                    self.grid.rebuild()

          def add_tile(self, tile_type, grid_position):
                    pixel_position = (grid_position[0] * self.tile_size, grid_position[1] * self.tile_size)
                    tile = Tile(tile_type, pixel_position)
                    self.grid.insert(tile)

          def draw(self):
                    if not self.game.changing_settings:
                              for tile_type in self.frames:
                                        self.frames[tile_type] += self.game.dt * self.animation_speed
                    for tile in self.grid.window_query():
                              if tile.tile_type in self.frames:
                                        tile.draw(self.game.display_screen, self.game.camera.offset_rect.topleft,
                                                  self.frames[tile.tile_type])
                              else:
                                        tile.draw(self.game.display_screen, self.game.camera.offset_rect.topleft, 0)

          @staticmethod
          def get_tile_type(x, y):
                    noise_value = Perlin_Noise["1 octave"]([x * 0.05, y * 0.05])
                    for tile in Tiles_Congifig["Tile_Ranges"].keys():
                              if noise_value < Tiles_Congifig["Tile_Ranges"][tile]:
                                        return tile

          def _get_cell(self, position):
                    return int(position[0] // self.cell_size), int(position[1] // self.cell_size)

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

          def apply_transition_tiles(self, tile1, tile2):
                    directions = ["top", "bottom", "right", "left"]
                    all_direction_positions = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]
                    direction_positions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
                    changes = 0
                    for tile in self.grid.items:
                              if tile.tile_type == tile2:
                                        grid_x, grid_y = int(tile.position.x // self.tile_size), int(
                                                  tile.position.y // self.tile_size)
                                        neighbours = [
                                                  self.get((grid_x + dx, grid_y + dy))
                                                  for dx, dy in direction_positions
                                        ]

                                        number_of_trans = 0
                                        current_transition = ""
                                        for i, neighbour in enumerate(neighbours):
                                                  if neighbour and neighbour.tile_type == tile1:
                                                            number_of_trans += 1
                                                            current_transition += directions[i]

                                        if 0 < number_of_trans <= 2:
                                                  if not current_transition in ["topbottom", "rightleft"]:
                                                            tile.images = [random.choice(
                                                                      Tile_Images[tile1 + "_" + tile2 + "4x4"][
                                                                                current_transition])]
                                                            tile.transition = current_transition
                                                  else:
                                                            tile.__init__(tile1,
                                                                          (tile.position.x, tile.position.y))
                                        if number_of_trans >= 3:
                                                  tile.__init__(tile1, (tile.position.x, tile.position.y))
                                                  changes += 1
                    if changes != 0:
                              self.apply_transition_tiles(tile1, tile2)

                    for tile in self.grid.items:
                              if tile.tile_type == tile2:
                                        grid_x, grid_y = int(tile.position.x // self.tile_size), int(
                                                  tile.position.y // self.tile_size)
                                        neighbours = [
                                                  self.get((grid_x + dx, grid_y + dy))
                                                  for dx, dy in direction_positions
                                        ]
                                        all_neighbours = [
                                                  self.get((grid_x + dx, grid_y + dy))
                                                  for dx, dy in all_direction_positions
                                        ]

                                        number_of_trans = 0
                                        current_transition = ""
                                        if not any(neighbour and neighbour.tile_type != tile2 for neighbour in
                                                   neighbours) and any(
                                                neighbour and neighbour.tile_type != tile2 for neighbour in
                                                all_neighbours):
                                                  for i, neighbour in enumerate(neighbours):
                                                            if neighbour and neighbour.tile_type == tile2 and neighbour.transition is not None:
                                                                      number_of_trans += 1
                                                                      current_transition += directions[i]

                                                  if number_of_trans == 2:
                                                            if not current_transition in ["topbottom", "rightleft"]:
                                                                      tile.images = [random.choice(
                                                                                Tile_Images[
                                                                                          tile1 + "_" + tile2 + "2x2"][
                                                                                          current_transition])]
                                                  elif number_of_trans == 3:
                                                            current_transition = remove_opposite_directions(
                                                                      current_transition)
                                                            tile_in_current_transition = neighbours[
                                                                      directions.index(current_transition)]
                                                            if tile_in_current_transition and tile_in_current_transition.transition:
                                                                      if (
                                                                              "top" in tile_in_current_transition.transition or "bottom" in tile_in_current_transition.transition) and \
                                                                              (
                                                                                      "left" in tile_in_current_transition.transition or "right" in tile_in_current_transition.transition):
                                                                                if current_transition in ["top",
                                                                                                          "bottom"]:
                                                                                          current_transition += remove_string(
                                                                                                    tile_in_current_transition.transition,
                                                                                                    "top" if "top" in current_transition else "bottom")
                                                                                else:
                                                                                          current_transition = remove_string(
                                                                                                    tile_in_current_transition.transition,
                                                                                                    "left" if "left" in current_transition else "right") + current_transition
                                                                      elif "top" in tile_in_current_transition.transition or "bottom" in tile_in_current_transition.transition:
                                                                                current_transition = tile_in_current_transition.transition + current_transition
                                                                      elif "left" in tile_in_current_transition.transition or "right" in tile_in_current_transition.transition:
                                                                                current_transition += tile_in_current_transition.transition

                                                            if current_transition in Tile_Images[
                                                                      tile1 + "_" + tile2 + "2x2"]:
                                                                      tile.images = [random.choice(
                                                                                Tile_Images[
                                                                                          tile1 + "_" + tile2 + "2x2"][
                                                                                          current_transition])]
                                                            else: print(f"Warning: Invalid transition '{current_transition}' for Grass_Tile_Water_Tile2x2")

          def terrain_generator(self):
                    for x in range(self.width):
                              for y in range(self.height):
                                        tile_type = self.get_tile_type(x, y)
                                        self.add_tile(tile_type, (x, y))

                    for key in Tile_Images.keys():
                              if string_ends_with(key, "_Tile"):
                                        for key2 in Tile_Images.keys():
                                                  if string_ends_with(key2, "_Tile"):
                                                            if Tile_Images.get(key + "_" + key2 + "4x4",
                                                                               None) is not None and Tile_Images.get(
                                                                    key + "_" + key2 + "2x2", None) is not None:
                                                                      self.apply_transition_tiles(key, key2)

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
