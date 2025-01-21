from Code.Individuals.Objects import *
from Code.DataStructures.Grid import *


class ObjectManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, General_Settings["hash_maps"][4])
                    self.biome_noise = PerlinNoise(octaves=Map_Config["biomes_map"][1], seed=random.randint(0, 100000))
                    self.density_noise = PerlinNoise(octaves=Map_Config["biomes_density_map"][1], seed=random.randint(0, 100000))
                    self.biome_map = self.generate_noise_map(self.biome_noise, Map_Config["biomes_map"][0])
                    self.density_map = self.generate_noise_map(self.density_noise, Map_Config["biomes_density_map"][0])
                    self.generate_objects()
                    self.generate_grass()

          def generate_objects(self):

                    size = General_Settings["tree"][1]
                    sorted_biomes = sorted(Biomes_Config.items(), key=lambda x_: x_[1])
                    # Generate trees based on biome and density
                    for y in range(0, GAME_SIZE[1], size):
                              for x in range(0, GAME_SIZE[0], size):
                                        biome_value = self.biome_map[y // size][x // size]
                                        density_value = self.density_map[y // size][x // size]
                                        biome_density_factor = 1

                                        biome = "forest"
                                        for biome_name, data in sorted_biomes:
                                                  if biome_value < data[0]:
                                                            biome = biome_name
                                                            biome_density_factor = data[1]
                                                            break

                                        # Check if we should place a tree based on density
                                        if random.random() < density_value * General_Settings["tree"][0] * biome_density_factor:
                                                  tree_image = random.choice(self.game.assets[biome + "_tree"])
                                                  pos = self.generate_valid_position(tree_image.size, x, y)
                                                  if pos:
                                                            self.grid.insert(
                                                                      Object(self.game, tree_image, tree_image.size,
                                                                             pos, True))

                    for _ in range(General_Settings["rock"][0]):
                              image = random.choice(AM.assets["rock"])
                              pos = self.generate_valid_position(image.size)
                              if pos:
                                        self.grid.insert(Object(self.game, image, image.size, pos, General_Settings["rock"][1]))

                    self.grid.rebuild()

          def generate_valid_position(self, size, base_x=None, base_y=None):
                    if base_x is None or base_y is None:
                              base_x, base_y = random.randint(0, GAME_SIZE[0]), random.randint(0, GAME_SIZE[1])

                    v = 30
                    for _ in range(10):
                              x = base_x + random.randint(-v, v)
                              y = base_y + random.randint(-v, v)
                              if 0 <= x < GAME_SIZE[0] - size[0] and 0 <= y < GAME_SIZE[1] - size[1]:
                                        rect = pygame.Rect(x - size[0] * 0.25, y + size[1] * 0.5, size[0] / 2, size[1] / 10)
                                        if not self.game.tilemap_manager.tile_collision(rect, "water_tile"):
                                                  return v2(x, y)
                    return None

          def generate_grass(self):
                    size = General_Settings["tree"][1]
                    for tile in self.game.tilemap_manager.grid.items:
                              if tile.tile_type == "grass_tile":
                                        # Convert tile position to biome map indices
                                        biome_x = int(tile.position.x) // size
                                        biome_y = int(tile.position.y) // size

                                        # Ensure we're within the bounds of the biome map
                                        if 0 <= biome_x < len(self.biome_map[0]) and 0 <= biome_y < len(self.biome_map):
                                                  biome_value = self.biome_map[biome_y][biome_x]
                                                  biome = self.get_biome_from_value(biome_value)

                                                  v = random.random()
                                                  if v < self.game.grass_manager.density:
                                                            grass_asset_key = f"{biome}_grass"
                                                            # Convert tile position to grass tile coordinates
                                                            grass_x = int(tile.position.x) // Grass_Attributes["tile_size"]
                                                            grass_y = int(tile.position.y) // Grass_Attributes["tile_size"]
                                                            self.game.grass_manager.place_tile(
                                                                      (grass_x, grass_y),
                                                                      int(v * 12),
                                                                      Grass_positions[grass_asset_key]
                                                            )

          @staticmethod
          def get_biome_from_value(biome_value):
                    sorted_biomes = sorted(Biomes_Config.items(), key=lambda x: x[1][0])
                    for biome_name, data in sorted_biomes:
                              if biome_value < data[0]:
                                        return biome_name
                    return sorted_biomes[-1][0]  # Return the last biome if no match found

          @staticmethod
          def generate_noise_map(noise, scale):
                    size = General_Settings["tree"][1]
                    width, height = GAME_SIZE[0] // size + 1, GAME_SIZE[1] // size + 1
                    noise_map = [[noise([i * scale, j * scale]) for j in range(width)] for i in range(height)]
                    return (np.array(noise_map) + 1) / 2  # Normalize to [0, 1]
