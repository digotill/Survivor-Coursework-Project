import pygame, math, random
from _internal.Variables.Variables import *
from _internal.Variables.Initialize import *
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
                    if name == "Player":
                              self.stamina = PLAYER_STAMINA

          def calc_angle(self):
                    return v2(self.game.player.pos.x + 0.5 * self.game.player.res[0] - self.pos.x - 0.5 * self.res[0],
                              self.game.player.pos.y + 0.5 * self.game.player.res[1] - self.pos.y - 0.5 * self.res[
                                        1]).angle_to((0, 1))


class AnimatedEntity:
          def __init__(self, game, images, animation=ANIMATION_SPEED):
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
          def __init__(self, game, health, res, vel, damage, coordinates, name, images, angle=None,
                       animation=ANIMATION_SPEED, acceleration=PLAYER_ACCELERATION):
                    RectEntity.__init__(self, game, coordinates, res, vel, name, angle)
                    AnimalEntity.__init__(self, game, health, damage)
                    self.acceleration = acceleration
                    self.current_vel = 0
                    self.gun = Gun(game, Rifle, PLAYER_GUN_RES, PLAYER_GUN_DISTANCE, PLAYER_BULLET_SPEED, PLAYER_BULLET_LIFETIME, PLAYER_BULLET_RATE)
                    AnimatedEntity.__init__(self, game, images, animation)

          def update(self):
                    a = self.game.keys[pygame.K_a]
                    d = self.game.keys[pygame.K_d]
                    w = self.game.keys[pygame.K_w]
                    s = self.game.keys[pygame.K_s]

                    self.update_facing()

                    dx, dy = 0, 0
                    if a: dx -= 1
                    if d: dx += 1
                    if s: dy += 1
                    if w: dy -= 1

                    magnitude = math.sqrt(dx ** 2 + dy ** 2)
                    if magnitude != 0:
                              dx /= magnitude
                              dy /= magnitude

                    if dy != 0 or dx != 0: self.update_frame()
                    self.update_velocity(dy, dx)

                    new_x = self.pos.x + dx * self.current_vel * self.game.dt
                    new_y = self.pos.y + dy * self.current_vel * self.game.dt

                    if 0 < new_x < self.game.big_window[0] - self.res[0]:
                              self.pos.x = new_x
                              self.rect.x = self.pos.x
                    if -10 < new_y < self.game.big_window[1] - self.res[1]:
                              self.pos.y = new_y
                              self.rect.y = self.pos.y

          def blit(self):
                    if self.facing == "left":
                              image = pygame.transform.flip(self.images[int(self.frame) % len(self.images) - 1], True,
                                                            False)
                    else:
                              image = self.images[int(self.frame) % len(self.images) - 1]
                    self.game.display_screen.blit(image, (self.pos.x - self.game.small_window.offset_rect.x - 10,
                                                          self.pos.y - self.game.small_window.offset_rect.y))

          def update_facing(self):
                    if int(self.game.mouse_pos[0] * REN_RES[
                              0] / self.game.display.width) < self.game.player.rect.centerx - self.game.small_window.pos.x:
                              self.facing = "left"
                    else:
                              self.facing = "right"

          def update_velocity(self, dy, dx):
                    if dy != 0 or dx != 0:
                              if self.current_vel + self.acceleration * self.game.dt < PLAYER_VEL:
                                        self.current_vel += self.acceleration * self.game.dt
                              else:
                                        self.current_vel = PLAYER_VEL
                    else:
                              if self.current_vel - self.acceleration * self.game.dt > 0:
                                        self.current_vel -= self.acceleration * self.game.dt
                              else:
                                        self.current_vel = 0

          def update_frame(self):
                    self.frame += self.animation * self.game.dt


class BG_entities(RectEntity):
          def __init__(self, game, coordinates, res, vel=None, name=None):
                    RectEntity.__init__(self, game, coordinates, res, vel, name)
                    self.image = BG_entities_gif[random.randint(0, len(BG_entities_gif) - 1)]
                    self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.width, self.image.height)
                    self.name = name

          def blit(self):
                    self.game.display_screen.blit(self.image, (self.pos.x - self.game.small_window.offset_rect.x,
                                                               self.pos.y - self.game.small_window.offset_rect.y))


class Enemy(RectEntity, AnimatedEntity, AnimalEntity):
          def __init__(self, game, coordinates, res, vel, name, health, damage, images, angle=None,
                       animation=ANIMATION_SPEED):
                    RectEntity.__init__(self, game, coordinates, res, vel, name, angle)
                    AnimatedEntity.__init__(self, game, images, animation)
                    AnimalEntity.__init__(self, game, health, damage)
                    self.facing = "right"

          def update(self):
                    if self.should_move():
                              self.move()
                    self.update_facing()
                    self.update_frame()

          def should_move(self):
                    distance = self.distance_to_player()
                    return distance > ENEMY_STOPPING_DISTANCE

          def distance_to_player(self):
                    player_center = self.game.player.pos + v2(self.game.player.res) * 0.5
                    enemy_center = self.pos + v2(self.res) * 0.5
                    return (player_center - enemy_center).length()

          def move(self):
                    new_angle = self.calc_angle()
                    self.rotate_velocity(new_angle)
                    self.update_position()

          def rotate_velocity(self, new_angle):
                    rotate = self.angle - new_angle
                    self.vel_vector.rotate_ip(rotate)
                    self.angle = new_angle

          def update_position(self):
                    self.pos += self.vel_vector * self.game.dt
                    self.rect.topleft = self.pos

          def update_facing(self):
                    self.facing = "right" if self.game.player.pos.x > self.pos.x else "left"

          def blit(self):
                    sprite = self.get_current_sprite()
                    draw_pos = self.pos - (self.game.small_window.offset_rect.x, self.game.small_window.offset_rect.y)
                    self.game.display_screen.blit(sprite, draw_pos)

          def get_current_sprite(self):
                    sprite = self.images[int(self.frame) % len(self.images)]
                    if self.facing == "left":
                              return pygame.transform.flip(sprite, True, False)
                    return sprite


class Gun:
          def __init__(self, game, gunImage, gun_res, distance, velocity, lifetime, fire_rate, friction=0):
                    self.game = game
                    self.res = gun_res
                    self.gunImage = gunImage
                    self.distance = distance
                    self.rect = pygame.Rect(0, 0, self.res[0], self.res[1])
                    self.facing = "right"
                    self.angle = 0
                    self.bullet_velocity = velocity
                    self.bullet_lifetime = lifetime
                    self.bullet_friction = friction
                    self.last_shot_time = 0
                    self.fire_rate = fire_rate

          def update(self):
                    self.update_facing()
                    self.calc_angle()

          def draw(self):
                    pos_x = (self.game.player.rect.centerx + math.sin(
                              math.radians(self.angle + 180)) * self.distance -
                             self.game.small_window.offset_rect.x + int(self.res[0] / 2) - 0.5 * self.res[0] - 5)
                    pos_y = (self.game.player.rect.centery + math.cos(
                              math.radians(self.angle + 180)) * self.distance -
                             self.game.small_window.offset_rect.y + int(self.res[1] / 2) - 0.5 * self.res[1] - 5)
                    if self.facing == "right":
                              new_image = pygame.transform.rotate(self.gunImage, self.angle + 90)
                              self.rect = new_image.get_rect(center=(pos_x, pos_y))
                              self.game.display_screen.blit(new_image, self.rect)
                    else:
                              new_image = pygame.transform.rotate(self.gunImage, -self.angle + 90)
                              self.rect = new_image.get_rect(center=(pos_x, pos_y))
                              self.game.display_screen.blit(pygame.transform.flip(new_image, True, False), self.rect)

          def update_facing(self):
                    if int(self.game.mouse_pos[0] * REN_RES[
                              0] / self.game.display.width) < self.game.player.rect.centerx - self.game.small_window.pos.x:
                              self.facing = "left"
                    else:
                              self.facing = "right"

          def calc_angle(self):
                    change_in_x = (self.game.player.rect.centerx - self.game.small_window.offset_rect.x
                                   - self.game.correct_mouse_pos[0] - 5)
                    change_in_y = (self.game.player.rect.centery - self.game.small_window.offset_rect.y
                                   - self.game.correct_mouse_pos[1] - 5)
                    angle = self.angle = v2(change_in_x, change_in_y).angle_to((0, 1))
                    if angle <= 0:
                              self.angle = angle + 360
                    else:
                              self.angle = angle

          def shoot(self):
                    current_time = pygame.time.get_ticks()
                    if self.fire_rate + self.last_shot_time < current_time:
                              self.last_shot_time = current_time

                              # Calculate bullet start position
                              start_x = self.game.player.rect.centerx + math.sin(
                                        math.radians(self.angle + 180)) * self.distance
                              start_y = self.game.player.rect.centery + math.cos(
                                        math.radians(self.angle + 180)) * self.distance
                              start_pos = v2(start_x, start_y)

                              # Create new bullet
                              new_bullet = Bullet(self.game, start_pos, self.angle, self.bullet_velocity,
                                                  self.bullet_image, self.bullet_lifetime, self.bullet_friction)

                              # Add bullet to game's bullet manager
                              self.game.bullet_manager.add_bullet(new_bullet)


class Bullet(RectEntity):
          def __init__(self, game, pos, angle, velocity, image, lifetime, name=PLAYER_NAME, friction=0,
                       damage=10):
                    self.image = pygame.transform.rotate(image, angle)
                    RectEntity.__init__(game, pos, self.image.get_size(), velocity, name, angle)
                    self.original_image = image
                    self.lifetime = lifetime
                    self.creation_time = pygame.time.get_ticks()
                    self.friction = friction
                    self.damage = damage

          def update(self):
                    if self.friction > 0:
                              self.vel_vector *= (1 - self.friction * self.game.dt)

                    self.pos += self.vel_vector * self.game.dt
                    self.rect.center = self.pos


          def check_collision(self, target):
                    if self.rect.colliderect(target.rect):
                              target.health -= self.damage
                              self.game.bullet_manager.remove_bullet(self)
                              return True
                    return False
