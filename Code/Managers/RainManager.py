from Code.Individuals.Rain import *
from Code.DataStructures.Grid import *


class RainManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, General_Settings["hash_maps"][3])
                    self.cooldown = Rain_Config['spawn_rate']
                    self.last_spawn = - Rain_Config['spawn_rate']

                    self.grid.rebuild()

          def update(self):
                    if not self.game.changing_settings:
                              for rain_droplet in self.grid.items:
                                        rain_droplet.update()
                                        if rain_droplet.hit_ground:
                                                  rain_droplet.update_frame()
                                                  self.game.drawing_manager.drawables.append(rain_droplet)
                              self.create()
                              self.check_dead()
                              self.grid.rebuild()

          def draw(self):
                    for rain_droplet in self.grid.window_query():
                              if not rain_droplet.hit_ground:
                                        rain_droplet.draw()

          def create(self):
                    if self.game.game_time - self.last_spawn > self.cooldown:
                              for _ in range(Rain_Config['amount_spawning']):
                                        self.grid.insert(Rain(self.game, Rain_Config))
                                        self.last_spawn = self.game.game_time

          def check_dead(self):
                    for rain_droplet in self.grid.items.copy():
                              if rain_droplet.frame >= len(rain_droplet.animation):
                                        self.grid.items.remove(rain_droplet)