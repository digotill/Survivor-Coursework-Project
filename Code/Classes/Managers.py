from Code.Classes.Buttons import *
from Code.Classes.Entities import *
from Code.Utilities.Grid import *
from Code.Utilities.Particles import Spark
import pygame, math, random


class EnemyManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    self.enemy_pool = set()
                    self.spawn_cooldown = 1
                    self.last_spawn = 0
                    self.enemy_multiplier = 1
                    self.separation_radius = General_Settings["enemy_separation_radius"]
                    self.separation_strength = General_Settings["enemy_separation_strength"]

          def update_enemies(self):
                    for enemy in self.grid.items:
                              separation_force = self.calculate_separation(enemy)
                              enemy.apply_force(separation_force)
                              enemy.update()
                    self.remove_dead_enemies()
                    self.add_enemies(Enemies["enemy1"])
                    self.grid.rebuild()

          def draw_enemies(self):
                    for enemy in self.grid.window_query():
                              enemy.blit()

          def add_enemies(self, enemy_dict):
                    if (self.last_spawn + self.spawn_cooldown < self.game.game_time and
                            len(self.grid.items) < General_Settings["max_enemies"] and not PEACEFUL_MODE):
                              self.last_spawn = self.game.game_time
                              coordinates = random_xy(
                                        pygame.Rect(0, 0, GAME_SIZE[0], GAME_SIZE[1]),
                                        self.game.window.rect, enemy_dict["res"][0], enemy_dict["res"][1]
                              )
                              if self.enemy_pool:
                                        enemy = self.enemy_pool.pop()
                                        enemy.reset(coordinates, enemy_dict)
                              else:
                                        enemy = Enemy(self.game, coordinates, enemy_dict)
                              self.grid.insert(enemy)

          def remove_dead_enemies(self):
                    for enemy in self.grid.items.copy():
                              if enemy.health <= 0:
                                        enemy.dead = True
                              if enemy.dead:
                                        self.grid.items.remove(enemy)
                                        self.game.window.add_screen_shake(
                                                  duration=Screen_Shake["bullet_impact_shake_duration"],
                                                  magnitude=Screen_Shake['bullet_impact_shake_magnitude']
                                        )
                                        self.enemy_pool.add(enemy)

          def calculate_separation(self, enemy):
                    steering = v2(0, 0)
                    total = 0
                    nearby_enemies = self.grid.query(
                              enemy.rect.inflate(self.separation_radius * 2, self.separation_radius * 2))

                    for other in nearby_enemies:
                              if other != enemy:
                                        distance = enemy.pos.distance_to(other.pos)
                                        if distance < self.separation_radius:
                                                  diff = (enemy.pos - other.pos).normalize() / distance
                                                  steering += diff
                                                  total += 1

                    if total > 0:
                              steering = (steering / total).normalize() * enemy.vel - enemy.vel_vector
                              if steering.length() > enemy.vel:
                                        steering = steering.normalize() * enemy.vel

                    return steering * self.separation_strength


class BulletManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    self.bullet_pool = set()

          def update(self):
                    current_time = self.game.game_time
                    for bullet in list(self.grid.items):
                              bullet.update()
                              if current_time - bullet.creation_time > bullet.lifetime:
                                        bullet.dead = True
                    self.check_for_collisions()
                    self.check_dead_bullets()
                    self.grid.rebuild()

          def draw(self):
                    offset_x, offset_y = self.game.window.offset_rect.topleft
                    for bullet in self.grid.window_query():
                              self.game.display_screen.blit(bullet.image,
                                                            (bullet.rect.x - offset_x, bullet.rect.y - offset_y))

          def add_bullet(self, start_x, start_y, angle, name, spread):
                    if self.bullet_pool:
                              bullet = self.bullet_pool.pop()
                              bullet.reset(start_x, start_y, angle, spread)
                    else:
                              bullet = Bullet(self.game, self.game.player.gun, (start_x, start_y), angle, name, spread)
                    self.grid.insert(bullet)

          def check_dead_bullets(self):
                    for bullet in self.grid.items.copy():
                              if bullet.dead:
                                        self.grid.items.remove(bullet)
                                        self.bullet_pool.add(bullet)

          def check_for_collisions(self):
                    for bullet in self.grid.items:
                              for enemy in self.game.enemy_manager.grid.query(bullet.rect):
                                        if bullet.check_collision(enemy):
                                                  self.create_bullet_sparks(bullet)
                                                  break

          def create_bullet_sparks(self, bullet):
                    spark_angle = math.radians(random.randint(
                              int(270 - bullet.angle) - Sparks_Settings['bullet']['spread'],
                              int(270 - bullet.angle) + Sparks_Settings['bullet']['spread']
                    ))
                    for _ in range(Sparks_Settings['bullet']['amount']):
                              self.game.particle_manager.sparks.add(
                                        Spark(self.game, bullet.pos, spark_angle,
                                              random.randint(3, 6), Sparks_Settings['bullet']['colour'],
                                              Sparks_Settings['bullet']['size'])
                              )


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
                    self.objects = set()
                    self.object_pool = set()
                    self.game = game
                    self.grid = SpatialHash(game)

          def update(self):
                    pass

          def draw(self):
                    pass


class SoundManager:
          def __init__(self, game):
                    self.game = game
                    self.sounds = {}


class ButtonManager:
          def __init__(self, game):
                    self.game = game
                    self.buttons = {}
                    self.sliders = {}
                    self._create_buttons()
                    self._create_sliders()

          def _create_buttons(self):
                    for name, config in All_Buttons["In_Game"].items():
                              self.buttons[name] = Button(
                                        self.game,
                                        **config
                              )

          def _create_sliders(self):
                    for name, config in All_Buttons["Sliders"].items():
                              self.sliders[name] = Slider(
                                        self.game,
                                        **config
                              )

          def update_buttons(self):
                    all_elements = list(self.buttons.values()) + list(self.sliders.values())
                    for buttons in all_elements:
                              buttons.active = self.game.changing_settings
                              buttons.update()
                              buttons.changeColor()

                    if self.game.mouse_state[0]:
                              if self.buttons['resume'].check_for_input():
                                        self.game.changing_settings = False
                              elif self.sliders['fps'].update_value:
                                        self.game.fps = self.sliders['fps'].value
                              elif self.sliders['brightness'].update_value:
                                        self.game.ui.brightness = self.sliders['brightness'].value
                              elif self.buttons['fullscreen'].check_for_input():
                                        self.game.event_manager.update_size(True)
                              elif self.buttons['quit'].check_for_input():
                                        self.game.immidiate_quit = True
                              elif self.buttons['return'].check_for_input():
                                        self.game.restart = True

          def draw_buttons(self):
                    for button in list(self.buttons.values()) + list(self.sliders.values()):
                              button.draw()
