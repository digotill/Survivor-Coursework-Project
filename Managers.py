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
                              if (abs(self.game.player.pos.x + 0.5 * self.game.player.res[0] - enemy.pos.x - 0.5 * enemy.rect.width) +
                                      abs(self.game.player.pos.y + 0.5 * self.game.player.res[1] - enemy.pos.y - 0.5 * enemy.rect.height) > 25):
                                        new_angle = enemy.calc_angle()
                                        rotate = enemy.angle - new_angle
                                        enemy.vel_vector.rotate_ip(rotate)
                                        enemy.angle = new_angle
                                        enemy.pos.x += enemy.vel_vector.x * self.game.dt
                                        enemy.pos.y += enemy.vel_vector.y * self.game.dt
                                        enemy.rect.x = enemy.pos.x
                                        enemy.rect.y = enemy.pos.y
                              enemy.frame += enemy.animation * self.game.dt
                              if self.game.player.pos.x - enemy.pos.x > 0:
                                        enemy.facing = "right"
                              elif self.game.player.pos.x - enemy.pos.x < 0:
                                        enemy.facing = "left"
                              if enemy.dead: self.delete_enemies(enemy)
                    self.add_enemies()
                    self.game.grids.enemy1_entities.rebuild()

          def draw_enemies(self):
                    for enemies in self.game.grids.enemy1_entities.query(self.game.small_window.rect): enemies.blit()

          def add_enemies(self):
                    if time.time() - self.last_spawn > self.spawn_cooldown:
                              self.last_spawn = time.time()
                              coordinates = random_xy(pygame.Rect(0, 0, self.game.big_window[0], self.game.big_window[1]), self.game.small_window.rect, ENEMY_RES[0], ENEMY_RES[1])
                              angle = v2(self.game.player.pos.x + 0.5 * self.game.player.res[0] - coordinates[0], self.game.player.pos.y + 0.5 * self.game.player.res[1] - coordinates[1]).angle_to((0, 1))
                              self.game.grids.enemy1_entities.insert(Entity(self.game, ENEMY_HEALTH, ENEMY_RES, ENEMY_VEL, ENEMY_DAMAGE, coordinates,ENEMY_NAME, angle=angle, idle=Enemy_idle))

          def delete_enemies(self, enemy):
                    self.enemy_list.remove(enemy)
                    #add animation to death


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
          def __init__(self, game, number):
                    self.game = game
                    for i in range(number):
                              coordinates = random.randint(0, self.game.big_window[0]), random.randint(0, self.game.big_window[1])
                              image = BG_sprites[random.randint(0, len(BG_sprites) - 1)]
                              entity2 = Entity(self.game, 0, image.get_size(), 0, 0, coordinates, "BG_Entity", idle=BG_sprites)
                              collision = False
                              for u in self.game.grids.window_entities.items:
                                        if pygame.Rect.colliderect(entity2.rect, u.rect): collision = True
                              if not collision: self.game.grids.window_entities.insert(entity2)

          def draw(self):
                    for entity in self.game.grids.window_entities.query(self.game.small_window.rect): entity.blit()


