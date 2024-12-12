import math

from Code.Utilities.Particles import Spark
from Code.Variables.Variables import *
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


class AnimatedEntity:
          def __init__(self, game, images, animation=General_Settings["animation_speed"]):
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


class main:
          def set_attributes(self, attributes):
                    for key, value in attributes.items():
                              setattr(self, key, value)

                    self.frame = 0
                    self.facing = "right"
                    self.dead = False

                    if hasattr(self, 'vel'):
                              self.max_vel = self.vel
                              self.current_vel = 0
                    if hasattr(self, 'health'):
                              self.max_health = self.health

          def update_frame(self):
                    self.frame += self.animation_speed * self.game.dt

          def set_rect(self):
                    self.rect = pygame.Rect(self.pos.x - self.res[0] / 2, self.pos.y - self.res[1] / 2, self.res[0],
                                            self.res[1])

          def get_position(self):
                    return self.rect.x - self.game.window.offset_rect.x, self.rect.y - self.game.window.offset_rect.y

          def get_mid_position(self):
                    return self.rect.centerx - self.game.window.offset_rect.x, self.rect.centery - self.game.window.offset_rect.y


class Player(main):
          def __init__(self, game, position, gun, dictionary):
                    self.game = game

                    self.set_attributes(dictionary)
                    self.pos = v2(position)
                    self.set_rect()
                    self.current_vel = 0
                    self.gun = gun

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
                              if self.offset_x1 + self.res[0] / 2 < new_x < GAME_SIZE[0] - self.res[0] / 2 + self.offset_x2:
                                        self.pos.x = new_x
                                        self.rect.centerx = self.pos.x
                                        move_hor = True
                              if self.offset_y1 + self.res[1] / 2 < new_y < GAME_SIZE[1] - self.res[1] / 2 + self.offset_y2:
                                        self.pos.y = new_y
                                        self.rect.centery = self.pos.y
                                        move_vert = True

                    self.game.window.move(dx, dy, move_hor, move_vert)

          def draw(self):
                    if self.facing == "left":
                              image = pygame.transform.flip(self.images[int(self.frame) % len(self.images) - 1], True,
                                                            False)
                    else:
                              image = self.images[int(self.frame) % len(self.images) - 1]
                    self.game.display_screen.blit(image, self.get_position())

          def update_facing(self):
                    if self.game.correct_mouse_pos[0] < self.get_mid_position()[0]:
                              self.facing = "left"
                    else:
                              self.facing = "right"

          def update_velocity(self, dy, dx):
                    if dy != 0 or dx != 0:
                              if self.current_vel + self.acceleration * self.game.dt < self.max_vel:
                                        self.current_vel += self.acceleration * self.game.dt
                              else:
                                        self.current_vel = self.max_vel
                    else:
                              if self.current_vel - self.acceleration * self.game.dt > 0:
                                        self.current_vel -= self.acceleration * self.game.dt
                              else:
                                        self.current_vel = 0


class Enemy(main):
          def __init__(self, game, coordinates, dictionary):
                    self.game = game

                    self.set_attributes(dictionary)

                    self.pos = v2(coordinates)
                    self.set_rect()

                    self.acceleration = v2(0, 0)
                    self.vel_vector = v2(0, 0)

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
                    return distance > self.stopping_distance

          def move(self):
                    direction = self.game.player.rect.center - self.pos
                    if direction.length() > 0:
                              direction = direction.normalize()

                    desired_velocity = direction * self.max_vel
                    steering = (desired_velocity - self.vel_vector) * self.steering_strength
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
                    self.game.display_screen.blit(self.get_current_sprite(), self.get_position())

          def get_current_sprite(self):
                    sprite = self.images[int(self.frame) % len(self.images)]
                    if self.facing == "left":
                              sprite = pygame.transform.flip(sprite, True, False)
                    return sprite

          def reset(self, coordinates, new_dictionary):
                    self.__init__(self.game, coordinates, new_dictionary)


class Gun(main):
          def __init__(self, game, dictionary):
                    self.game = game

                    self.set_attributes(dictionary)

                    self.pos = v2(0, 0)
                    self.rect = pygame.Rect(0, 0, self.res[0], self.res[1])

                    self.last_shot_time = 0
                    self.initial_vel = self.vel
                    self.continuous_fire_start = 0

          def update(self):
                    self.calc_angle()
                    self.update_shooting()

          def draw(self):
                    if self.game.player.facing == "right":
                              self.rotated_image = pygame.transform.rotate(self.gun_image, self.angle + 90)
                    else:
                              self.rotated_image = pygame.transform.flip(
                                        pygame.transform.rotate(self.gun_image, -self.angle + 90), True, False)

                    pos_x = (self.game.player.rect.centerx + math.sin(
                              math.radians(self.angle)) * self.distance_perpendicular -
                             self.game.window.offset_rect.x)
                    pos_y = (self.game.player.rect.centery + math.cos(
                              math.radians(self.angle)) * self.distance_perpendicular -
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
                    max_spread_time = self.spread_time
                    spread_factor = min(firing_duration / max_spread_time, 1.0)

                    self.last_shot_time = current_time

                    start_coordinates = self.calculate_bullet_start_position()
                    for _ in range(self.shots):
                              self.game.particle_manager.create_spark(270 - self.angle, start_coordinates, Sparks_Settings['gun'])
                              if self.shots == 1:
                                        self.game.bullet_manager.add_bullet(start_coordinates, self.angle,
                                                                            "Player Bullet", spread_factor)
                              else:
                                        self.game.bullet_manager.add_bullet(start_coordinates,
                                                                            change_random(self.angle, self.spread),
                                                                            "Player Bullet", spread_factor)

          def calculate_bullet_start_position(self):
                    start_x = self.game.player.rect.centerx + math.sin(math.radians(self.angle)) * int(
                              self.distance_perpendicular - self.res[0] / 1.4)
                    start_y = self.game.player.rect.centery + math.cos(math.radians(self.angle)) * int(
                              self.distance_perpendicular - self.res[0] / 1.4)
                    return start_x, start_y


class Bullet(main):
          def __init__(self, game, gun, pos, angle, name, spread_factor):
                    self.game = game
                    self.gun = gun
                    self.name = name

                    noise_value = Perlin_Noise["perlin"]([game.game_time * 0.1, 0])
                    spread_angle = noise_value * gun.spread * spread_factor
                    self.angle = angle + spread_angle
                    self.image = pygame.transform.rotate(gun.bullet_image, self.angle + 90)
                    self.original_image = gun.bullet_image

                    self.pos = v2(pos)
                    self.vel_vector = v2(0, -gun.vel).rotate(-self.angle)
                    self.rect = self.image.get_rect(center=self.pos)
                    self.res = self.rect.size

                    self.lifetime = change_random(self.gun.lifetime, self.gun.lifetime_randomness)
                    self.dead = False
                    self.creation_time = game.game_time
                    self.friction = self.gun.friction
                    self.damage = self.gun.damage
                    self.pierce = self.gun.pierce
                    self.health = self.pierce

          def update(self):
                    if self.friction > 0:
                              self.vel_vector *= (1 - self.friction * self.game.dt)

                    self.pos += self.vel_vector * self.game.dt
                    self.rect.center = self.pos

          def check_collision(self, target):
                    if self.rect.colliderect(target.rect):
                              target.health -= self.damage
                              self.pierce -= 1
                              if self.pierce <= 0:
                                        self.dead = True
                              return True
                    return False

          def reset(self, pos, angle, spread):
                    self.__init__(self.game, self.gun, pos, angle, self.name, spread)
