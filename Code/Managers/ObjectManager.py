from Code.Individuals.Buttons import *
from Code.Individuals.Objects import *
from Code.DataStructures.Grid import *
from pygame.math import Vector2 as v2
from perlin_noise import PerlinNoise
import pygame, random


class ObjectManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, General_Settings["hash_maps"][4])
                    self.biome_noise = PerlinNoise(octaves=Perlin_Noise["biome_map"][1], seed=random.randint(0, 100000))
                    self.density_noise = PerlinNoise(octaves=Perlin_Noise["density_map"][1], seed=random.randint(0, 100000))
                    self.generate_objects()

          def generate_objects(self):

                    # Generate biome and density maps
                    biome_map = self.generate_noise_map(self.biome_noise, Perlin_Noise["biome_map"][0])
                    density_map = self.generate_noise_map(self.density_noise, Perlin_Noise["density_map"][0])

                    size = General_Settings["tree"][1]
                    sorted_biomes = sorted(Biomes_Config.items(), key=lambda x_: x_[1])
                    # Generate trees based on biome and density
                    for y in range(0, GAME_SIZE[1], size):
                              for x in range(0, GAME_SIZE[0], size):
                                        biome_value = biome_map[y // size][x // size]
                                        density_value = density_map[y // size][x // size]
                                        biome_density_factor = 1

                                        biome = "green"
                                        for biome_name, data in sorted_biomes:
                                                  if biome_value < data[0]:
                                                            biome = biome_name
                                                            biome_density_factor = data[1]
                                                            break

                                        # Check if we should place a tree based on density
                                        if random.random() < density_value * General_Settings["tree"][0] * biome_density_factor:  # Adjust 0.1 to control overall tree density
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
                                        if not self.game.tilemap.tile_collision(rect, "water_tile"):
                                                  return v2(x, y)
                    return None

          @staticmethod
          def generate_noise_map(noise, scale):
                    size = General_Settings["tree"][1]
                    width, height = GAME_SIZE[0] // size, GAME_SIZE[1] // size
                    noise_map = [[noise([i * scale, j * scale]) for j in range(width)] for i in range(height)]
                    return (np.array(noise_map) + 1) / 2  # Normalize to [0, 1]