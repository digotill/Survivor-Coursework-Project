import time
from Initialize import *
from Entities import *
from pygame.math import Vector2 as v2


class EnemyManager:
          def __init__(self, game):
                    self.game = game
                    self.enemy_list = set()
                    self.spawn_cooldown = ENEMY_SPAWN_RATE
                    self.last_spawn = 0
                    self.damage_multiplier = 1
                    self.health_multiplier = 1

          def update_enemies(self):
                    for enemy in self.game.grids.enemy1_entities.items:
                              enemy.update()
                              enemy.update_frame()
                              enemy.update_facing()
                              if enemy.dead: self.enemy_list.remove(enemy)
                    self.add_enemies()
                    self.game.grids.enemy1_entities.rebuild()

          def draw_enemies(self):
                    for enemies in self.game.grids.enemy1_entities.query(self.game.small_window.rect): enemies.blit()

          def add_enemies(self):
                    if time.time() - self.last_spawn > self.spawn_cooldown:
                              self.last_spawn = time.time()
                              coordinates = random_xy(pygame.Rect(0, 0, self.game.big_window[0], self.game.big_window[1]), self.game.small_window.rect, ENEMY_RES[0], ENEMY_RES[1])
                              angle = v2(self.game.player.pos.x + 0.5 * self.game.player.res[0] - coordinates[0], self.game.player.pos.y + 0.5 * self.game.player.res[1] - coordinates[1]).angle_to((0, 1))
                              entity = Enemy(self.game, coordinates, ENEMY_RES, ENEMY_VEL, ENEMY_NAME, ENEMY_HEALTH, ENEMY_DAMAGE, Enemy_idle, angle)
                              self.game.grids.enemy1_entities.insert(entity)


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

class BG_entities_manager:
          def __init__(self, game):
                    self.game = game
                    for i in range(int(PLAYABLE_AREA[0] / 200 * BG_ENTITIES_DENSITY)):
                              coordinates = random.randint(0, self.game.big_window[0]), random.randint(0, self.game.big_window[1])
                              entity = BG_entities(self.game, coordinates, BG_ENTITIES_RES, 0, "BG_Entity")
                              collision = False
                              for u in self.game.grids.window_entities.items:
                                        if pygame.Rect.colliderect(entity.rect, u.rect): collision = True
                              if not collision: self.game.grids.window_entities.insert(entity)

          def draw(self):
                    for entity in self.game.grids.window_entities.query(self.game.small_window.offset_rect): entity.blit()


