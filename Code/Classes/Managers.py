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
                    self.spawn_cooldown = enemy_attributes["spawn_rate"]
                    self.last_spawn = 0
                    self.enemy_multiplier = 1
                    self.separation_radius = 15
                    self.separation_strength = 0.4

          def update_enemies(self):
                    for enemy in self.grid.items:
                              separation_force = self.calculate_separation(enemy)
                              enemy.apply_force(separation_force)
                              enemy.update()
                    self.remove_dead_enemies()
                    self.add_enemies()
                    self.grid.rebuild()

          def draw_enemies(self):
                    for enemy in self.grid.window_query():
                              enemy.blit()

          def add_enemies(self):
                    if (self.last_spawn + self.spawn_cooldown < self.game.game_time and
                            len(self.grid.items) < enemy_attributes["max_enemies"] and not PEACEFUL_MODE):
                              self.last_spawn = self.game.game_time
                              coordinates = random_xy(
                                        pygame.Rect(0, 0, self.game.big_window[0], self.game.big_window[1]),
                                        self.game.window.rect, enemy_attributes["res"][0], enemy_attributes["res"][1]
                              )

                              if self.enemy_pool:
                                        enemy = self.enemy_pool.pop()
                                        self.reset_enemy(enemy, coordinates)
                              else:
                                        enemy = self.create_new_enemy(coordinates)

                              self.grid.insert(enemy)

          def remove_dead_enemies(self):
                    for enemy in self.grid.items.copy():
                              if enemy.pierce <= 0:
                                        enemy.dead = True
                              if enemy.dead:
                                        self.grid.items.remove(enemy)
                                        self.game.window.add_screen_shake(
                                                  duration=screen_shake["bullet_impact_shake_duration"],
                                                  magnitude=screen_shake['bullet_impact_shake_magnitude']
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

          def reset_enemy(self, enemy, coordinates):
                    enemy.pos = v2(coordinates)
                    enemy.rect.center = coordinates
                    enemy.vel_vector = v2(0, 0)
                    enemy.acceleration = v2(0, 0)
                    enemy.pierce = enemy_attributes["health"] * self.enemy_multiplier
                    enemy.dead = False

          def create_new_enemy(self, coordinates):
                    return Enemy(self.game, coordinates, enemy_attributes["res"], enemy_attributes["vel"], enemy_attributes["name"],
                                 enemy_attributes["health"] * self.enemy_multiplier,
                                 enemy_attributes["damage"] * self.enemy_multiplier, Enemy_idle)


class BulletManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    self.player_bullets = set()
                    self.enemy_bullets = set()
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
                    bullet_set = self.player_bullets if name == "Player Bullet" else self.enemy_bullets
                    bullet_set.add(bullet)

          def check_dead_bullets(self):
                    for bullet in self.grid.items.copy():
                              if bullet.dead:
                                        self.grid.items.remove(bullet)
                                        bullet_set = self.player_bullets if bullet.name == "Player Bullet" else self.enemy_bullets
                                        bullet_set.remove(bullet)
                                        self.bullet_pool.add(bullet)

          def check_for_collisions(self):
                    for bullet in self.player_bullets:
                              for enemy in self.game.enemy_manager.grid.query(bullet.rect):
                                        if bullet.check_collision(enemy):
                                                  self.create_bullet_sparks(bullet)
                                                  break

          def create_bullet_sparks(self, bullet):
                    spark_angle = math.radians(random.randint(
                              int(270 - bullet.angle) - sparks['bullet']['spread'],
                              int(270 - bullet.angle) + sparks['bullet']['spread']
                    ))
                    for _ in range(sparks['bullet']['amount']):
                              self.game.particle_manager.sparks.add(
                                        Spark(self.game, bullet.pos, spark_angle,
                                              random.randint(3, 6), sparks['bullet']['colour'],
                                              sparks['bullet']['size'])
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


class ButtonManager:
          def __init__(self, game):
                    self.game = game
                    self.buttons = {}
                    self.sliders = {}
                    self._create_buttons()
                    self._create_sliders()

          def _create_buttons(self):
                    button_configs = {
                              'resume': buttons['resume'],
                              'fullscreen': buttons['fullscreen'],
                              'quit': buttons['quit']
                    }
                    for name, config in button_configs.items():
                              self.buttons[name] = Button(
                                        self.game,
                                        Buttons[0],
                                        config['pos'],
                                        config['axis'],
                                        config['axisl'],
                                        text_input=config['name']
                              )

          def _create_sliders(self):
                    slider_configs = {
                              'fps': {
                                        **sliders['fps'],
                                        'max_value': 240,
                                        'min_value': 60,
                                        'initial_value': pygame.display.get_current_refresh_rate()
                              },
                              'brightness': {
                                        **sliders['brightness'],
                                        'max_value': 100,
                                        'min_value': 0,
                                        'initial_value': window_attributes['brightness'],
                              }
                    }
                    for name, config in slider_configs.items():
                              self.sliders[name] = Slider(
                                        self.game,
                                        Buttons[1],
                                        config['pos'],
                                        config['axis'],
                                        config['axisl'],
                                        text_input=config['text'],
                                        text_pos=config['text_pos'],
                                        max_value=config['max_value'],
                                        min_value=config['min_value'],
                                        initial_value=config['initial_value']
                              )

          def update_buttons(self):
                    all_elements = list(self.buttons.values()) + list(self.sliders.values())
                    for element in all_elements:
                              element.active = self.game.changing_settings
                              element.update()
                              element.changeColor()

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

          def draw_buttons(self):
                    for element in list(self.buttons.values()) + list(self.sliders.values()):
                              element.draw()
