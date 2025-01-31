from Code.Variables.SettingVariables import *
from Code.Individuals.Grass import *

# the main object that manages the grass system
class GrassManager():
          def __init__(self, game):
                    self.game = game
                    # asset manager
                    self.ga = GrassAssets(self)

                    self.game.methods.set_attributes(self, GRASS)

                    # caching variables
                    self.grass_id = 0
                    self.grass_cache = {}
                    self.shadow_cache = {}
                    self.formats = {}

                    # tile data
                    self.grass_tiles = {}

                    self.count = 0
                    self.rendered_shadows = None

          # either creates a new grass tile layout or returns an existing one if the cap has been hit
          def get_format(self, format_id, data, tile_id):
                    if format_id not in self.formats:
                              self.formats[format_id] = {'count': 1, 'data': [(tile_id, data)]}
                    elif self.formats[format_id]['count'] >= self.max_unique:
                              return deepcopy(random.choice(self.formats[format_id]['data']))
                    else:
                              self.formats[format_id]['count'] += 1
                              self.formats[format_id]['data'].append((tile_id, data))

          def place_tile(self, location, density, grass_options):
                    # ignore if a tile was already placed in this location
                    if tuple(location) not in self.grass_tiles:
                              self.grass_tiles[tuple(location)] = GrassTile(self.game, self.tile_size, (
                                        location[0] * self.tile_size, location[1] * self.tile_size), density,
                                                                            grass_options,
                                                                            self.ga, self)

          # apply a force to the grass that causes the grass to bend away
          def apply_force(self, location, radius, dropoff):
                    location = (int(location[0]), int(location[1]))
                    grid_pos = (int(location[0] // self.tile_size), int(location[1] // self.tile_size))
                    tile_range = math.ceil((radius + dropoff) / self.tile_size)
                    for y in range(tile_range * 2 + 1):
                              y = y - tile_range
                              for x in range(tile_range * 2 + 1):
                                        x = x - tile_range
                                        pos = (grid_pos[0] + x, grid_pos[1] + y)
                                        if pos in self.grass_tiles:
                                                  self.grass_tiles[pos].apply_force(location, radius, dropoff)

          # an update and render combination function
          def draw(self):
                    self.count += 1
                    if self.rendered_shadows is None and self.count > 1:
                              self.draw_shadows()
                              self.rendered_shadows = True
                    surf = self.game.displayS
                    offset = self.game.cameraM.offset_rect.topleft

                    # Increase the rendering area by adding a buffer
                    visible_tile_range = (
                              int(surf.get_width() // self.tile_size) + 1,
                              int(surf.get_height() // self.tile_size) + 2
                    )
                    base_pos = (
                              int(offset[0] // self.tile_size),
                              int(offset[1] // self.tile_size)
                    )

                    # Create a list of tiles to render
                    render_list = [
                              (base_pos[0] + x, base_pos[1] + y)
                              for y in range(visible_tile_range[1])
                              for x in range(visible_tile_range[0])
                              if (base_pos[0] + x, base_pos[1] + y) in self.grass_tiles
                    ]

                    # Prepare grass tiles for rendering
                    drawables = [self.grass_tiles[pos] for pos in render_list]
                    self.game.drawingM.drawables.extend(drawables)

          def draw_shadows(self):
                    for pos in self.grass_tiles:
                              self.grass_tiles[pos].render_shadow(self.game.tilemapM.cached_surface,
                                                                  offset=(-self.shadow_shift[0], -self.shadow_shift[1]))


# an asset manager that contains functionality for rendering blades of grass
class GrassAssets:
          def __init__(self, gm):
                    self.gm = gm
                    self.blades = AM.assets["grass"]

          def render_blade(self, surf, blade_id, location, rotation):
                    # rotate the blade
                    rot_img = pygame.transform.rotate(self.blades[blade_id], rotation)

                    # shade the blade of grass based on its rotation
                    shade = pygame.Surface(rot_img.get_size())
                    shade_amt = self.gm.shade_amount * (abs(rotation) / 90)
                    shade.set_alpha(shade_amt)
                    rot_img.blit(shade, (0, 0))

                    # render the blade
                    surf.blit(rot_img,
                              (location[0] - rot_img.get_width() // 2, location[1] - rot_img.get_height() // 2))

