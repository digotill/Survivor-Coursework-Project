from Code.Individuals.Rain import *
from Code.DataStructures.HashMap import *


class RainManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, General_Settings["hash_maps"][3])

                    self.spawn_timer = Timer(RAIN['spawn_rate'], self.game.game_time, self.spawn_rain)
                    self.rain_surface = pygame.Surface(self.game.display_surface.get_size(), pygame.SRCALPHA)
                    self.grid.rebuild()

          def update(self):
                    if not self.game.changing_settings:
                              for rain_droplet in self.grid.items:
                                        rain_droplet.update()
                                        if rain_droplet.hit_ground:
                                                  rain_droplet.update_frame()

                              # Update the timer
                              if self.spawn_timer.update(self.game.game_time):
                                        self.spawn_rain()
                                        self.spawn_timer.reactivate(self.game.game_time)

                              self.check_dead()
                              self.grid.rebuild()

          def draw(self):
                    self.rain_surface.fill((0, 0, 0, 0))  # Clear the surface with transparent color
                    for rain_droplet in self.grid.window_query():
                              if not rain_droplet.hit_ground:
                                        pos = (rain_droplet.rect.x - self.game.camera.offset_rect.x,
                                               rain_droplet.rect.y - self.game.camera.offset_rect.y)
                                        self.rain_surface.blit(rain_droplet.animation[0], pos)

                    self.game.display_surface.blit(self.rain_surface, (0, 0))

          def spawn_rain(self):
                    for _ in range(RAIN['amount_spawning']):
                              rain = Rain(self.game, RAIN)
                              self.grid.insert(rain)

          def check_dead(self):
                    for rain_droplet in self.grid.items.copy():
                              if rain_droplet.frame >= len(rain_droplet.animation):
                                        self.grid.items.remove(rain_droplet)