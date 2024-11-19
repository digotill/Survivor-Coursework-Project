import time
from Code.Variables.Initialize import *
from Code.Classes.Entities import *
from pygame.math import Vector2 as v2
from Code.Utilities.Grid import *
from Code.Classes.Button_Class import *


class EnemyManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    self.spawn_cooldown = ENEMY_SPAWN_RATE
                    self.last_spawn = 0

          def update_enemies(self):
                    for enemy in self.grid.items:
                              if enemy.should_move():
                                        enemy.move()
                              enemy.update_frame()
                              enemy.update_facing()
                    self.remove_enemy()
                    self.add_enemies()
                    self.grid.rebuild()

          def draw_enemies(self):
                    for enemies in self.grid.window_query(): enemies.blit()

          def add_enemies(self):
                    if self.last_spawn + self.spawn_cooldown < self.game.game_time and len(self.grid.items) < MAX_ENEMIES:
                              self.last_spawn = self.game.game_time
                              coordinates = random_xy(pygame.Rect(0, 0, self.game.big_window[0], self.game.big_window[1]),
                                                      self.game.window.rect, ENEMY_RES[0], ENEMY_RES[1])
                              angle = v2(self.game.player.pos.x + 0.5 * self.game.player.res[0] - coordinates[0],
                                         self.game.player.pos.y + 0.5 * self.game.player.res[1] - coordinates[1]).angle_to((0, 1))
                              entity = Enemy(self.game, coordinates, ENEMY_RES, ENEMY_VEL, ENEMY_NAME, ENEMY_HEALTH,
                                             ENEMY_DAMAGE, Enemy_idle, angle)
                              self.grid.insert(entity)

          def remove_enemy(self):
                    for enemy in self.grid.items.copy():
                              if enemy.health <= 0: enemy.dead = True
                              if enemy.dead:
                                        self.grid.items.remove(enemy)
                                        self.game.window.add_screen_shake(duration=ENEMY_SCREEN_SHAKE_DURATION,
                                                                          magnitude=ENEMY_SCREEN_SHAKE_MAGNITUDE)

class BulletManager:

          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    self.player_bullets = set()
                    self.enemy_bullets = set()

          def update(self):
                    for bullet in self.grid.items:
                              bullet.update()
                              if bullet.creation_time + bullet.lifetime < self.game.game_time: bullet.dead = True
                    self.check_for_collisions()
                    self.grid.rebuild()
                    self.remove_bullet()

          def draw(self):
                    for bullet in self.grid.window_query():
                              self.game.display_screen.blit(bullet.image, (bullet.rect.x - self.game.window.offset_rect.x,
                                                                           bullet.rect.y - self.game.window.offset_rect.y))

          def add_bullet(self, bullet):
                    self.grid.insert(bullet)
                    if bullet.name == "Player Bullet": self.player_bullets.add(bullet)
                    elif bullet.name == "Enemy Bullet": self.enemy_bullets.add(bullet)

          def remove_bullet(self):
                    new_set = self.grid.items.copy()
                    for bullet in new_set:
                              if bullet.dead:
                                        self.grid.items.remove(bullet)
                                        if bullet.name == "Player Bullet": self.player_bullets.remove(bullet)
                                        elif bullet.name == "Enemy Bullet": self.enemy_bullets.remove(bullet)

          def check_for_collisions(self):
                    for bullet in self.player_bullets:
                              for enemy in self.game.enemy_manager.grid.query(bullet.rect):
                                        if bullet.check_collision(enemy):
                                                  if bullet.health <= 0:
                                                            bullet.dead = True
                                                            break

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
                    for i in range(int(PLAYABLE_AREA_SIZE[0] / 480 * BG_ENTITIES_DENSITY)):
                              coordinates = random.randint(0, self.game.big_window[0]), random.randint(0, self.game.big_window[1])
                              entity = BG_entities(self.game, coordinates, BG_ENTITIES_RES)
                              collision = False
                              for u in self.grid.items:
                                        if pygame.Rect.colliderect(entity.rect, u.rect): collision = True
                              if not collision: self.grid.insert(entity)

          def draw(self):
                    for entity in self.grid.window_query(): entity.blit()


class ButtonManager:
          def __init__(self, game):
                    self.game = game
                    self.play_button = Paused_Buttons(self.game, Buttons[0], (240, 135), PLAY_BUTTON_RES, True, "y", "max",
                                                      SETTINGS_BUTTON_SPEED, "Play", FONT, (255, 255, 255), (255, 0, 0))
                    self.buttons = [self.play_button]

          def update_buttons(self):
                    for button in self.buttons:
                              button.active = self.game.changing_settings
                              button.update()
                              button.changeColor()
                    if self.game.mouse_state[0]:
                              if self.play_button.check_for_input(): print(True)

          def draw_buttons(self):
                    for button in self.buttons:
                              button.draw()


