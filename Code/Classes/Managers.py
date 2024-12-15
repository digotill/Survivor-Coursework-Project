from Code.Classes.Buttons import *
from Code.Classes.Entities import *
from Code.Utilities.Grid import *
from Code.Utilities.Particles import Spark
import pygame, math, random


class EnemyManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game)
                    self.enemy_pool = set()
                    self.spawn_cooldown = General_Settings["enemy_spawn_rate"]
                    self.last_spawn = - General_Settings["enemy_spawn_rate"]
                    self.enemy_multiplier = 1

          def update(self):
                    for enemy in self.grid.items:
                              enemy.update()
                              separation_force = self.calculate_separation(enemy)
                              enemy.apply_force(separation_force)
                    self.remove_dead_enemies()
                    self.add_enemies(Enemies["enemy1"])
                    self.grid.rebuild()

          def draw(self):
                    for enemy in self.grid.window_query():
                              enemy.blit()

          def add_enemies(self, enemy_dict):
                    if (self.last_spawn + self.spawn_cooldown < self.game.game_time and
                            len(self.grid.items) < General_Settings["max_enemies"] and not General_Settings["peaceful_mode"]):
                              self.last_spawn = self.game.game_time
                              coordinates = random_xy(
                                        pygame.Rect(0, 0, GAME_SIZE[0], GAME_SIZE[1]),
                                        self.game.camera.rect, enemy_dict["res"][0], enemy_dict["res"][1]
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
                                        self.game.camera.add_screen_shake(
                                                  duration=Screen_Shake["bullet_impact_shake_duration"],
                                                  magnitude=Screen_Shake['bullet_impact_shake_magnitude']
                                        )
                                        self.enemy_pool.add(enemy)

          def calculate_separation(self, enemy):
                    steering = v2(0, 0)
                    total = 0
                    nearby_enemies = self.grid.query(
                              enemy.rect.inflate(enemy.separation_radius * 2, enemy.separation_radius * 2))

                    for other in nearby_enemies:
                              if other != enemy:
                                        distance = enemy.pos.distance_to(other.pos)
                                        if distance < enemy.separation_radius:
                                                  diff = (enemy.pos - other.pos).normalize() / distance
                                                  steering += diff
                                                  total += 1

                    if total > 0:
                              steering = (steering / total).normalize() * enemy.vel - enemy.vel_vector
                              if steering.length() > enemy.vel:
                                        steering = steering.normalize() * enemy.vel

                    return steering * enemy.separation_strength


class BulletManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game)
                    self.bullet_pool = set()

          def update(self):
                    current_time = self.game.game_time
                    for bullet in self.grid.items:
                              bullet.update()
                              if current_time - bullet.creation_time > bullet.lifetime:
                                        bullet.dead = True
                    self.check_for_collisions()
                    self.check_dead_bullets()
                    self.grid.rebuild()

          def draw(self):
                    offset_x, offset_y = self.game.camera.offset_rect.topleft
                    for bullet in self.grid.window_query():
                              self.game.display_screen.blit(bullet.image,
                                                            (bullet.rect.x - offset_x, bullet.rect.y - offset_y))

          def add_bullet(self, pos, angle, name, spread):
                    if self.bullet_pool:
                              bullet = self.bullet_pool.pop()
                              bullet.reset(pos, angle, spread)
                    else:
                              bullet = Bullet(self.game, self.game.player.gun, pos, angle, name, spread)
                    self.grid.insert(bullet)

          def check_dead_bullets(self):
                    for bullet in self.grid.items.copy():
                              if bullet.dead:
                                        self.grid.items.remove(bullet)
                                        self.bullet_pool.add(bullet)

          def check_for_collisions(self):
                    for bullet in self.grid.items:
                              for enemy in self.game.enemy_manager.grid.query(bullet.rect):
                                        if bullet.rect.colliderect(enemy.rect) and not bullet.dead:
                                                  enemy.deal_damage(bullet.damage)
                                                  bullet.check_if_alive()
                                                  self.game.particle_manager.create_spark(270 - bullet.angle,
                                                                                          bullet.pos,
                                                                                          Sparks_Settings[
                                                                                                    'bullet'])


class ParticleManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game)
                    self.spark_pool = set()

          def update(self):
                    for spark in self.grid.items:
                              spark.move()
                    self.check_if_remove()
                    self.grid.rebuild()

          def draw(self):
                    for spark in self.grid.window_query():
                              spark.draw()

          def create_spark(self, angle, pos, dictionary):
                    for _ in range(dictionary['amount']):
                              spark_angle = math.radians(random.randint(
                                        int(angle) - dictionary['spread'],
                                        int(angle) + dictionary['spread']
                              ))
                              spark_velocity = random.randint(dictionary["min_vel"], dictionary["max_vel"])
                              if len(self.spark_pool) == 0:
                                        self.grid.insert(
                                                  Spark(self.game, pos, spark_angle, spark_velocity,
                                                        dictionary['colour'], dictionary['scale']))
                              else:
                                        spark = self.spark_pool.pop()
                                        spark.reset(pos, spark_angle, spark_velocity, dictionary["colour"],
                                                    dictionary['scale'])
                                        self.grid.insert(spark)

          def check_if_remove(self):
                    for spark in self.grid.items.copy():
                              if not spark.alive:
                                        self.grid.items.remove(spark)
                                        self.spark_pool.add(spark)


class ObjectManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game)

                    self.object_pool = set()

          def update(self):
                    pass

          def draw(self):
                    pass

          def add_object(self, obj):
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

                    self.cooldown = Cooldowns['buttons']
                    self.last_pressed_time = - Cooldowns['buttons']

                    self.value_cooldown = 0.1
                    self.last_value_set = 0

          def _create_buttons(self):
                    button_configs = AllButtons
                    for name, config in button_configs["In_Game"].items():
                              self.buttons[name] = Button(
                                        self.game,
                                        copy.deepcopy(config)
                              )

          def _create_sliders(self):
                    button_configs = AllButtons
                    for name, config in button_configs["Sliders"].items():
                              self.sliders[name] = Slider(
                                        self.game,
                                        copy.deepcopy(config)
                              )

          def update(self):
                    all_elements = list(self.buttons.values()) + list(self.sliders.values())
                    for buttons in all_elements:
                              buttons.active = self.game.changing_settings
                              buttons.update()
                              buttons.changeColor()

                    if self.game.changing_settings and self.game.mouse_state[0] and pygame.time.get_ticks() / 1000 - self.last_pressed_time > self.cooldown:
                              temp_time = self.last_pressed_time
                              self.last_pressed_time = pygame.time.get_ticks() / 1000
                              if self.buttons['resume'].check_for_input():
                                        self.game.changing_settings = False
                              elif self.sliders['fps'].update_value:
                                        self.game.fps = self.sliders['fps'].value
                              elif self.sliders['brightness'].update_value:
                                        self.game.ui_manager.brightness = self.sliders['brightness'].value
                              elif self.buttons['fullscreen'].check_for_input():
                                        self.game.event_manager.update_size(True)
                              elif self.buttons['quit'].check_for_input():
                                        self.game.immidiate_quit = True
                              elif self.buttons['return'].check_for_input():
                                        self.game.restart = True
                              else: self.last_pressed_time = temp_time

                    if self.game.changing_settings and pygame.time.get_ticks() / 1000 - self.last_value_set > self.value_cooldown:
                              self.game.fps = self.sliders['fps'].value
                              self.game.ui_manager.brightness = self.sliders['brightness'].value
                              self.last_value_set = pygame.time.get_ticks() / 1000

          def draw(self):
                    for button in list(self.buttons.values()) + list(self.sliders.values()):
                              button.draw()

class RainManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game)
                    self.cooldown = Cooldowns['rain']
                    self.last_spawn = - Cooldowns['rain']

                    self.grid.rebuild()

          def update(self):
                    for rain_droplet in self.grid.items:
                              rain_droplet.update()
                              if rain_droplet.hit_ground: rain_droplet.update_frame()
                    self.create()
                    self.check_dead()
                    self.grid.rebuild()

          def draw(self):
                    for rain_droplet in self.grid.window_query():
                              pos = rain_droplet.rect.x - self.game.camera.offset_rect.x, rain_droplet.rect.y - self.game.camera.offset_rect.y
                              if not rain_droplet.hit_ground:
                                        self.game.display_screen.blit(rain_droplet.animation[0], pos)
                              else:
                                        self.game.display_screen.blit(
                                                  rain_droplet.animation[int(rain_droplet.frame % len(rain_droplet.animation))], pos)

          def create(self):
                    if self.game.game_time - self.last_spawn > self.cooldown:
                              self.grid.insert(Rain(self.game, Rain_Config))
                              self.last_spawn = self.game.game_time

          def check_dead(self):
                    for rain_droplet in self.grid.items.copy():
                              if rain_droplet.frame >= len(rain_droplet.animation):
                                        self.grid.items.remove(rain_droplet)


