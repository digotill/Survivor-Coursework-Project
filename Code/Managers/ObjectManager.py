from Code.Individuals.Objects import *
from Code.DataStructures.HashMap import *


class ObjectManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, GENERAL["hash_maps"][4])
                    self.biome_map, self.density_map = self.game.tilemap_manager.biome_map, self.game.tilemap_manager.density_map
                    self.generate_objects()
                    self.generate_grass()
                    self.draw_shadows()

          def draw_shadows(self):
                    for object1 in self.grid.items:
                              object1.draw_shadow(self.game.tilemap_manager.cached_surface)

          def generate_objects(self):
                    self._generate_trees()
                    self._generate_rocks()
                    self.grid.rebuild()

          def _generate_trees(self):
                    size = GENERAL["tree"][1]
                    sorted_biomes = sorted(BIOMES.items(), key=lambda x: x[1])
                    for y in range(0, GAME_SIZE[1], size):
                              for x in range(0, GAME_SIZE[0], size):
                                        biome_value = self.biome_map[y // size][x // size]
                                        density_value = self.density_map[y // size][x // size]
                                        biome, biome_density_factor = self._get_biome_info(biome_value, sorted_biomes)

                                        if self._should_place_tree(density_value, biome_density_factor):
                                                  self._place_tree(x, y, biome)

          def _generate_rocks(self):
                    for _ in range(GENERAL["rock"][0]):
                              image = random.choice(AM.assets["rock"])
                              pos = self.generate_valid_position(image.size)
                              if pos:
                                        self.grid.insert(Object(self.game, image, image.size, pos))

          def generate_grass(self):
                    size = GENERAL["tree"][1]
                    for tile in self.game.tilemap_manager.grid.items:
                              if tile.tile_type == "grass_tile":
                                        biome_x, biome_y = int(tile.position.x) // size, int(tile.position.y) // size
                                        if self._is_valid_biome_position(biome_x, biome_y):
                                                  self._place_grass(tile, biome_x, biome_y)

          def generate_valid_position(self, size, base_x=None, base_y=None):
                    base_x = base_x or random.randint(0, GAME_SIZE[0])
                    base_y = base_y or random.randint(0, GAME_SIZE[1])
                    v = 30
                    for _ in range(10):
                              x = base_x + random.randint(-v, v)
                              y = base_y + random.randint(-v, v)
                              if self._is_valid_position(x, y, size):
                                        return v2(x, y)
                    return None

          def _is_valid_position(self, x, y, size):
                    if 0 <= x < GAME_SIZE[0] - size[0] and 0 <= y < GAME_SIZE[1] - size[1]:
                              rect = pygame.Rect(x - size[0] * 0.25, y + size[1] * 0.5, size[0] / 2, size[1] / 10)
                              return not self.game.tilemap_manager.tile_collision(rect, "water_tile")
                    return False

          @staticmethod
          def _get_biome_from_value(biome_value):
                    sorted_biomes = sorted(BIOMES.items(), key=lambda x: x[1][0])
                    for biome_name, data in sorted_biomes:
                              if biome_value < data[0]:
                                        return biome_name
                    return sorted_biomes[-1][0]

          @staticmethod
          def _get_biome_info(biome_value, sorted_biomes):
                    biome = "forest"
                    biome_density_factor = 1
                    for biome_name, data in sorted_biomes:
                              if biome_value < data[0]:
                                        biome = biome_name
                                        biome_density_factor = data[1]
                                        break
                    return biome, biome_density_factor

          @staticmethod
          def _should_place_tree(density_value, biome_density_factor):
                    return random.random() < density_value * GENERAL["tree"][0] * biome_density_factor

          def _place_tree(self, x, y, biome):
                    tree_image = random.choice(self.game.assets[biome + "_tree"])
                    pos = self.generate_valid_position(tree_image.size, x, y)
                    if pos:
                              self.grid.insert(Object(self.game, tree_image, tree_image.size, pos))

          def _is_valid_biome_position(self, biome_x, biome_y):
                    return 0 <= biome_x < len(self.biome_map[0]) and 0 <= biome_y < len(self.biome_map)

          def _place_grass(self, tile, biome_x, biome_y):
                    biome_value = self.biome_map[biome_y][biome_x]
                    biome = self._get_biome_from_value(biome_value)
                    v = random.random()
                    if v < self.game.grass_manager.density:
                              grass_asset_key = f"{biome}_grass"
                              grass_x = int(tile.position.x) // GRASS["tile_size"]
                              grass_y = int(tile.position.y) // GRASS["tile_size"]
                              self.game.grass_manager.place_tile(
                                        (grass_x, grass_y),
                                        int(v * 12),
                                        GRASS["positions"][grass_asset_key]
                              )
