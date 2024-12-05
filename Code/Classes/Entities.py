import math

from Code.Utilities.Particles import Spark
from Code.Variables.Initialize import *
from pygame.math import Vector2 as v2


class RectEntity:
          def __init__(self, game, coordinates, res, vel, name, angle=None):
                    self.game = game
                    self.pos = v2(coordinates)
                    self.name = name
                    self.res = res
                    self.rect = pygame.Rect(self.pos.x, self.pos.y, res[0], res[1])
                    self.vel = vel
                    if angle is not None:
                              self.vel_vector = v2(self.vel * math.sin(math.radians(angle)),
                                                   self.vel * math.cos(math.radians(angle)))
                              self.angle = angle

          def calc_angle(self):
                    return v2(self.game.player.pos.x + 0.5 * self.game.player.res[0] - self.pos.x - 0.5 * self.res[0],
                              self.game.player.pos.y + 0.5 * self.game.player.res[1] - self.pos.y - 0.5 * self.res[
                                        1]).angle_to((0, 1))


class AnimatedEntity:
          def __init__(self, game, images, animation=general_settings["animation_speed"]):
                    self.game = game
                    self.images = images
                    self.animation = animation
                    self.frame = 0
                    self.facing = "right"

          def update_frame(self):
                    self.frame += self.animation * self.game.dt


class AnimalEntity:
          def __init__(self, game, health, damage):
                    self.game = game
                    self.health = health
                    self.damage = damage
                    self.dead = False


class Player(RectEntity, AnimatedEntity, AnimalEntity):
          def __init__(self, game, health, res, vel, damage, coordinates, name=player_attributes['name'], images=Player_Running,
                       angle=None, animation=player_attributes['animation_speed'], acceleration=player_attributes['acceleration'], gun=None):
                    RectEntity.__init__(self, game, coordinates, res, vel, name, angle)
                    AnimalEntity.__init__(self, game, health, damage)
                    self.acceleration = acceleration
                    self.current_vel = 0
                    self.max_health = health
                    if gun is None:
                              self.gun = Gun(game, AK_47, PLAYER_GUN_RES, Bullets, PLAYER_GUN_DISTANCE, PLAYER_BULLET_SPEED,
                                   PLAYER_BULLET_LIFETIME, PLAYER_BULLET_RATE, PLAYER_BULLET_FRICTION,
                                   PLAYER_BULLET_DAMAGE)
                    AnimatedEntity.__init__(self, game, images, animation)
                    self.pos.x -= self.res[0] / 2
                    self.pos.y -= self.res[1] / 2
                    self.stamina = player_attributes['stamina']

          def update(self):
                    dx, dy = 0, 0
                    if self.game.keys[pygame.K_a]: dx -= 1
                    if self.game.keys[pygame.K_d]: dx += 1
                    if self.game.keys[pygame.K_s]: dy += 1
                    if self.game.keys[pygame.K_w]: dy -= 1

                    magnitude = math.sqrt(dx ** 2 + dy ** 2)
                    if magnitude != 0:
                              dx /= magnitude
                              dy /= magnitude

                    if (dy != 0 or dx != 0) and not self.game.changing_settings: self.update_frame()
                    self.update_velocity(dy, dx)
                    self.update_facing()

                    new_x = self.pos.x + dx * self.current_vel * self.game.dt
                    new_y = self.pos.y + dy * self.current_vel * self.game.dt

                    move_hor, move_vert = False, False
                    if not self.game.changing_settings:
                              if player_attributes['offset_x1'] < new_x < self.game.big_window[0] - self.res[0] + player_attributes['offset_x2']:
                                        self.pos.x = new_x
                                        self.rect.x = self.pos.x
                                        move_hor = True
                              if player_attributes['offset_y1'] < new_y < self.game.big_window[1] - self.res[
                                        1] + player_attributes['offset_y2'] + 23:
                                        self.pos.y = new_y
                                        self.rect.y = self.pos.y
                                        move_vert = True

                    self.game.window.move(dx, dy, move_hor, move_vert)

          def draw(self):
                    if self.facing == "left":
                              image = pygame.transform.flip(self.images[int(self.frame) % len(self.images) - 1], True,
                                                            False)
                    else:
                              image = self.images[int(self.frame) % len(self.images) - 1]
                    self.game.display_screen.blit(image, (self.rect.x - self.game.window.offset_rect.x,
                                                          self.rect.y - self.game.window.offset_rect.y))

          def update_facing(self):
                    if self.game.correct_mouse_pos[0] < self.game.player.rect.centerx - self.game.window.offset_rect.x:
                              self.facing = "left"
                    else:
                              self.facing = "right"

          def update_velocity(self, dy, dx):
                    if dy != 0 or dx != 0:
                              if self.current_vel + self.acceleration * self.game.dt < player_attributes['vel']:
                                        self.current_vel += self.acceleration * self.game.dt
                              else:
                                        self.current_vel = player_attributes['vel']
                    else:
                              if self.current_vel - self.acceleration * self.game.dt > 0:
                                        self.current_vel -= self.acceleration * self.game.dt
                              else:
                                        self.current_vel = 0

          def update_frame(self):
                    self.frame += self.animation * self.game.dt


class Enemy(RectEntity, AnimatedEntity, AnimalEntity):
          def __init__(self, game, coordinates, res, max_vel, name, health, damage, images, angle=None,
                       animation=enemy_attributes["animation_speed"]):
                    super().__init__(game, coordinates, res, max_vel, name, angle)
                    AnimatedEntity.__init__(self, game, images, animation)
                    AnimalEntity.__init__(self, game, health, damage)
                    self.max_vel = max_vel
                    self.acceleration = v2(0, 0)
                    self.vel_vector = v2(0, 0)
                    self.friction = enemy_attributes["friction"]
                    self.facing = "right"

          def apply_force(self, force):
                    self.vel_vector += force
                    if self.vel_vector.length() > self.vel:
                              self.vel_vector = self.vel_vector.normalize() * self.vel

          def update(self):
                    if self.should_move():
                              self.move()
                    self.update_frame()
                    self.update_facing()
                    self.update_position()

          def should_move(self):
                    distance = self.distance_to_player()
                    return distance > enemy_attributes["stopping_distance"]

          def move(self):
                    direction = self.game.player.rect.center - self.pos
                    if direction.length() > 0:
                              direction = direction.normalize()

                    desired_velocity = direction * self.max_vel
                    steering = (desired_velocity - self.vel_vector) * enemy_attributes["steering_strength"]
                    self.apply_force(steering)

                    self.vel_vector += self.acceleration * self.game.dt
                    if self.vel_vector.length() > self.max_vel:
                              self.vel_vector = self.vel_vector.normalize() * self.max_vel

                    self.vel_vector *= (1 - self.friction)

                    self.acceleration = v2(0, 0)

          def update_position(self):
                    self.pos += self.vel_vector * self.game.dt
                    self.rect.center = self.pos

          def update_facing(self):
                    self.facing = "right" if self.game.player.rect.centerx > self.pos.x else "left"

          def distance_to_player(self):
                    return (self.game.player.rect.center - self.pos).length()

          def blit(self):
                    sprite = self.get_current_sprite()
                    draw_pos = (self.rect.x - self.game.window.offset_rect.x,
                                self.rect.y - self.game.window.offset_rect.y)
                    self.game.display_screen.blit(sprite, draw_pos)

          def get_current_sprite(self):
                    sprite = self.images[int(self.frame) % len(self.images)]
                    if self.facing == "left":
                              sprite = pygame.transform.flip(sprite, True, False)
                    return sprite


class Gun:
          def __init__(self, game, gunImage, gun_res, bullet_image, distance, velocity, lifetime, fire_rate, friction=0,
                       damage=30):
                    self.game = game
                    self.res = gun_res
                    self.gunImage = gunImage
                    self.distance = distance
                    self.damage = damage
                    self.rect = pygame.Rect(0, 0, self.res[0], self.res[1])
                    self.angle = 0
                    self.initial_vel = velocity
                    self.bullet_image = bullet_image
                    self.bullet_velocity = velocity
                    self.bullet_lifetime = lifetime
                    self.bullet_friction = friction
                    self.last_shot_time = 0
                    self.fire_rate = fire_rate
                    self.continuous_fire_start = None

          def update(self):
                    self.calc_angle()
                    self.update_shooting()

          def draw(self):
                    if self.game.player.facing == "right":
                              self.rotated_image = pygame.transform.rotate(self.gunImage, self.angle + 90)
                    else:
                              self.rotated_image = pygame.transform.flip(
                                        pygame.transform.rotate(self.gunImage, -self.angle + 90), True, False)

                    pos_x = (self.game.player.rect.centerx + math.sin(math.radians(self.angle)) * self.distance -
                             self.game.window.offset_rect.x)
                    pos_y = (self.game.player.rect.centery + math.cos(math.radians(self.angle)) * self.distance -
                             self.game.window.offset_rect.y)
                    self.rect = self.rotated_image.get_rect(center=(pos_x, pos_y))
                    self.game.display_screen.blit(self.rotated_image, self.rect)

          def calc_angle(self):
                    change_in_x = self.game.player.rect.centerx - self.game.window.offset_rect.x - \
                                  self.game.correct_mouse_pos[0]
                    change_in_y = self.game.player.rect.centery - self.game.window.offset_rect.y - \
                                  self.game.correct_mouse_pos[1]
                    self.angle = v2(change_in_x, change_in_y).angle_to((0, 1))

          def update_shooting(self):
                    current_time = self.game.game_time
                    if self.can_shoot(current_time):
                              self.shoot(current_time)
                    elif not self.game.mouse_state[0]:
                              self.continuous_fire_start = None

          def can_shoot(self, current_time):
                    return (self.fire_rate + self.last_shot_time < current_time and
                            self.game.mouse_state[0] and
                            not self.game.changing_settings)

          def shoot(self, current_time):
                    if self.continuous_fire_start is None:
                              self.continuous_fire_start = current_time

                    firing_duration = current_time - self.continuous_fire_start
                    max_spread_time = PLAYER_GUN_SPREAD_TIME
                    spread_factor = min(firing_duration / max_spread_time, 1.0)

                    self.last_shot_time = current_time

                    start_x, start_y = self.calculate_bullet_start_position()
                    self.create_gun_sparks(start_x, start_y)
                    self.create_bullet(start_x, start_y, spread_factor)

          def calculate_bullet_start_position(self):
                    start_x = self.game.player.rect.centerx + math.sin(math.radians(self.angle)) * int(
                              self.distance - self.res[0] / 1.4)
                    start_y = self.game.player.rect.centery + math.cos(math.radians(self.angle)) * int(
                              self.distance - self.res[0] / 1.4)
                    return start_x, start_y

          def create_gun_sparks(self, start_x, start_y):
                    for _ in range(sparks['gun']['amount']):
                              spark_angle = math.radians(random.randint(
                                        int(270 - self.angle) - sparks['gun']['spread'],
                                        int(270 - self.angle) + sparks['gun']['spread']
                              ))
                              self.game.particle_manager.sparks.add(Spark(
                                        self.game, [start_x, start_y], spark_angle,
                                        random.randint(3, 6), sparks['gun']['colour'], sparks['gun']['size']
                              ))

          def create_bullet(self, start_x, start_y, spread_factor):
                    self.game.bullet_manager.add_bullet(
                              start_x, start_y, self.angle, self.initial_vel,
                              self.bullet_image, self.bullet_lifetime,
                              self.bullet_friction, "Player Bullet", self.damage,
                              spread_factor, 1  # Assuming bullet health is 1
                    )


class Bullet(RectEntity):
          def __init__(self, game, pos, angle, velocity, image, lifetime, friction, name="dunno", damage=10,
                       health=1, spread_factor=0):
                    noise_value = perlin_noise["perlin"]([game.game_time * 0.1, 0])
                    spread_angle = noise_value * PLAYER_GUN_SPREAD * spread_factor
                    final_angle = angle + spread_angle
                    self.image = pygame.transform.rotate(image, final_angle + 90)
                    RectEntity.__init__(self, game, pos, self.image.get_rect().size, velocity, name, final_angle + 180)
                    self.original_image = image
                    self.lifetime = change_random(lifetime, BULLET_LIFETIME_RANDOMNESS)
                    self.dead = False
                    self.creation_time = game.game_time
                    self.friction = friction
                    self.damage = damage
                    self.health = health
                    self.rect.center = self.pos

          def update(self):
                    if self.friction > 0:
                              self.vel_vector *= (1 - self.friction * self.game.dt)

                    self.pos += self.vel_vector * self.game.dt
                    self.rect.center = self.pos

          def check_collision(self, target):
                    if self.rect.colliderect(target.rect):
                              target.health -= self.damage
                              self.health -= 1
                              if self.health <= 0:
                                        self.dead = True
                              return True
                    return False

          def reset(self, start_x, start_y, angle, vel, life, friction, name, damage, spread, health):
                    self.pos = v2(start_x, start_y)
                    self.rect.center = (start_x, start_y)
                    noise_value = perlin_noise["perlin"]([self.game.game_time * 0.1, 0])
                    spread_angle = noise_value * PLAYER_GUN_SPREAD * spread
                    final_angle = angle + spread_angle + 180
                    self.vel_vector = v2(vel * math.sin(math.radians(final_angle)),
                                         vel * math.cos(math.radians(final_angle)))
                    self.creation_time = self.game.game_time
                    self.image = pygame.transform.rotate(self.original_image, final_angle + 90)
                    self.lifetime = life
                    self.friction = friction
                    self.name = name
                    self.damage = damage
                    self.health = health
                    self.spread_factor = spread
                    self.dead = False
                    self.angle = angle
