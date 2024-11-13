import time
from _internal.Variables.Initialize import *
from _internal.Classes.Entities import *
from pygame.math import Vector2 as v2
from _internal.Utilities.Grid import *


class EnemyManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    self.enemy_list = set()
                    self.spawn_cooldown = ENEMY_SPAWN_RATE
                    self.last_spawn = 0
                    self.damage_multiplier = 1
                    self.health_multiplier = 1

          def update_enemies(self):
                    for enemy in self.grid.items:
                              enemy.update()
                              enemy.update_frame()
                              enemy.update_facing()
                              if enemy.dead: self.enemy_list.remove(enemy)
                    self.add_enemies()
                    self.grid.rebuild()

          def draw_enemies(self):
                    for enemies in self.grid.window_query(): enemies.blit()

          def add_enemies(self):
                    if time.time() - self.last_spawn > self.spawn_cooldown:
                              self.last_spawn = time.time()
                              coordinates = random_xy(pygame.Rect(0, 0, self.game.big_window[0], self.game.big_window[1]), self.game.small_window.rect, ENEMY_RES[0], ENEMY_RES[1])
                              angle = v2(self.game.player.pos.x + 0.5 * self.game.player.res[0] - coordinates[0], self.game.player.pos.y + 0.5 * self.game.player.res[1] - coordinates[1]).angle_to((0, 1))
                              entity = Enemy(self.game, coordinates, ENEMY_RES, ENEMY_VEL, ENEMY_NAME, ENEMY_HEALTH, ENEMY_DAMAGE, Enemy_idle, angle)
                              self.grid.insert(entity)


class BulletManager:

          def __init__(self, game):
                    self.game = game
                    self.bullets = []

          def update(self):
                    pass

          def draw(self):
                    pass


class ParticleManager:
          def __init__(self, game):
                    self.game = game
                    self.particle_list = []

          def update_particles(self):
                    pass

          def draw_particles(self):
                    pass


class ObjectManager:
          def __init__(self, game):
                    self.current_objects = []
                    self.game = game
                    self.interaction = True
                    self.position = 0

          def update(self):
                    pass

          def draw(self):
                    pass


class SoundManager:
          def __init__(self, game):
                    self.game = game
                    self.sounds = {}

class BG_Entities_Manager:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    for i in range(int(PLAYABLE_AREA[0] / 200 * BG_ENTITIES_DENSITY)):
                              coordinates = random.randint(0, self.game.big_window[0]), random.randint(0, self.game.big_window[1])
                              entity = BG_entities(self.game, coordinates, BG_ENTITIES_RES)
                              collision = False
                              for u in self.grid.items:
                                        if pygame.Rect.colliderect(entity.rect, u.rect): collision = True
                              if not collision: self.grid.insert(entity)

          def draw(self):
                    for entity in self.grid.window_query(): entity.blit()


