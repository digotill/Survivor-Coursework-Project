import time
from Code.Variables.Initialize import *
from Code.Classes.Entities import *
from pygame.math import Vector2 as v2
from Code.Utilities.Grid import *
from Code.Classes.Buttons import *
from Code.Utilities.Particles import Spark


class EnemyManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    self.enemy_pool = set()
                    self.spawn_cooldown = ENEMY_SPAWN_RATE
                    self.last_spawn = 0
                    self.enemy_multiplier = 1
                    self.separation_radius = 15
                    self.separation_strength = 0.4

          def update_enemies(self):
                    for enemy in self.grid.items:
                              separation_force = self.calculate_separation(enemy)
                              enemy.apply_force(separation_force)
                              enemy.update()
                    self.remove_enemy()
                    self.add_enemies()
                    self.grid.rebuild()

          def draw_enemies(self):
                    for enemies in self.grid.window_query(): enemies.blit()

          def add_enemies(self):
                    if self.last_spawn + self.spawn_cooldown < self.game.game_time and len(
                            self.grid.items) < MAX_ENEMIES:
                              self.last_spawn = self.game.game_time
                              coordinates = random_xy(
                                        pygame.Rect(0, 0, self.game.big_window[0], self.game.big_window[1]),
                                        self.game.window.rect, ENEMY_RES[0], ENEMY_RES[1])
                              if not bool(self.enemy_pool):
                                        entity = Enemy(self.game, coordinates, ENEMY_RES, ENEMY_VEL, ENEMY_NAME,
                                                       ENEMY_HEALTH * self.enemy_multiplier,
                                                       ENEMY_DAMAGE * self.enemy_multiplier, Enemy_idle)
                                        self.grid.insert(entity)
                              else:
                                        entity = self.enemy_pool.pop()
                                        entity.pos = v2(coordinates)
                                        entity.rect.center = coordinates
                                        entity.vel_vector = v2(0, 0)
                                        entity.acceleration = v2(0, 0)
                                        entity.health = ENEMY_HEALTH * self.enemy_multiplier
                                        entity.dead = False
                                        self.grid.insert(entity)

          def remove_enemy(self):
                    for enemy in self.grid.items.copy():
                              if enemy.health <= 0: enemy.dead = True
                              if enemy.dead:
                                        self.grid.items.remove(enemy)
                                        self.game.window.add_screen_shake(duration=ENEMY_SCREEN_SHAKE_DURATION, magnitude=ENEMY_SCREEN_SHAKE_MAGNITUDE)
                                        self.enemy_pool.add(enemy)

          def calculate_separation(self, enemy):
                    steering = v2(0, 0)
                    total = 0
                    for other in self.grid.query(
                            enemy.rect.inflate(self.separation_radius * 2, self.separation_radius * 2)):
                              if other != enemy:
                                        distance = enemy.pos.distance_to(other.pos)
                                        if distance < self.separation_radius:
                                                  diff = enemy.pos - other.pos
                                                  diff = diff.normalize()
                                                  diff /= distance  # Weight by distance
                                                  steering += diff
                                                  total += 1

                    if total > 0:
                              steering /= total
                              if steering.length() > 0:
                                        steering = steering.normalize() * enemy.vel
                                        steering -= enemy.vel_vector
                                        if steering.length() > enemy.vel:
                                                  steering = steering.normalize() * enemy.vel

                    return steering * self.separation_strength

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
                              self.game.display_screen.blit(bullet.image, (bullet.rect.x - self.game.window.offset_rect.x, bullet.rect.y - self.game.window.offset_rect.y))

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
                                                  location = [bullet.rect.centerx, bullet.rect.centery]
                                                  for _ in range(BULLET_SPARK_AMOUNT):
                                                            self.game.particle_manager.sparks.add(Spark(self.game, location, math.radians(random.randint(int(270 - bullet.angle)
                                                                      - BULLET_SPARK_SPREAD, int(270 - bullet.angle) + BULLET_SPARK_SPREAD)),
                                                                                random.randint(3, 6), BULLET_SPARK_COLOUR, BULLET_SPARK_SIZE))
                                                  if bullet.health <= 0:
                                                            bullet.dead = True
                                                            break

class ParticleManager:
          def __init__(self, game):
                    self.game = game
                    self.sparks = set()

          def update(self):
                    for _, spark in sorted(enumerate(self.sparks), reverse=True):
                              spark.move()
                              if not spark.alive:
                                        self.sparks.remove(spark)

          def draw(self):
                    for _, spark in sorted(enumerate(self.sparks), reverse=True):
                              spark.draw()

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


class BGEntitiesManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    for i in range(int(PLAYABLE_AREA_SIZE[0] / 480 * BG_ENTITIES_DENSITY)):
                              coordinates = random.randint(0, PLAYABLE_AREA_SIZE[0]), random.randint(0, PLAYABLE_AREA_SIZE[1])
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
                    self.resume_button = SlidingButtons(self.game, Buttons[0], RESUME_BUTTON_POS, "y", "max", text_input="Resume")
                    self.fps_slider = NewSlider(self.game, Buttons[1], FPS_SLIDER_POS, "x", "max", text_input="Max FPS: ",
                                                text_pos="right", max_value=240, min_value=60, initial_value=pygame.display.get_current_refresh_rate())
                    self.brightness_slider = NewSlider(self.game, Buttons[1], BRIGHTNESS_SLIDER_POS, "x", "max", text_input="Brightness: ",
                                                       text_pos="right", max_value=100, min_value=0, initial_value=INITIAL_BRIGHTNESS)
                    self.fullscreen_button = SlidingButtons(self.game, Buttons[0], FULLSCREEN_BUTTON_POS, "y", "max", text_input="Fullscreen")
                    self.quit_button = SlidingButtons(self.game, Buttons[0], NEW_QUIT_BUTTON_POS, "y", "max", text_input="Quit")
                    self.buttons = [self.resume_button, self.fps_slider, self.brightness_slider, self.fullscreen_button, self.quit_button]

          def update_buttons(self):
                    for button in self.buttons:
                              button.active = self.game.changing_settings
                              button.update()
                              button.changeColor()
                    if self.game.mouse_state[0]:
                              if self.resume_button.check_for_input(): self.game.changing_settings = False
                              elif self.fps_slider.update_value: self.game.fps = self.fps_slider.value
                              elif self.brightness_slider.update_value: self.game.ui.brightness = self.brightness_slider.value
                              elif self.fullscreen_button.check_for_input(): self.game.event_manager.update_size(True)
                              elif self.quit_button.check_for_input(): self.game.immidiate_quit = True

          def draw_buttons(self):
                    for button in self.buttons:
                              button.draw()



