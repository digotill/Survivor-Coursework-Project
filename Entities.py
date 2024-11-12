import pygame, math, random
from Variables import *
from Initialize import *
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
                              self.vel_vector = v2(self.vel * math.sin(math.radians(angle)), self.vel * math.cos(math.radians(angle)))
                              self.angle = angle
                    if name == "Player":
                              self.stamina = PLAYER_STAMINA

          def calc_angle(self):
                    return v2(self.game.player.pos.x + 0.5 * self.game.player.res[0] - self.pos.x - 0.5 * self.res[0], self.game.player.pos.y + 0.5 * self.game.player.res[1] - self.pos.y - 0.5 * self.res[1]).angle_to((0, 1))

class AnimatedEntity:
          def __init__(self, game,  images, animation=ANIMATION_SPEED):
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
          def __init__(self, game, health, res, vel, damage, coordinates, name, images, angle=None, animation=ANIMATION_SPEED):
                    RectEntity.__init__(self, game, coordinates, res, vel, name, angle)
                    AnimatedEntity.__init__(self, game, images, animation)
                    AnimalEntity.__init__(self, game, health, damage)

          def update(self):
                    a = self.game.keys[pygame.K_a]
                    d = self.game.keys[pygame.K_d]
                    w = self.game.keys[pygame.K_w]
                    s = self.game.keys[pygame.K_s]

                    self.update_facing(a, d)

                    dx, dy = 0, 0
                    if a: dx -= 1
                    if d: dx += 1
                    if s: dy += 1
                    if w: dy -= 1

                    if dy != 0 or dx != 0: self.update_frame()

                    magnitude = math.sqrt(dx ** 2 + dy ** 2)
                    if magnitude != 0:
                              dx /= magnitude
                              dy /= magnitude

                    new_x = self.pos.x + dx * PLAYER_VEL * self.game.dt
                    new_y = self.pos.y + dy * PLAYER_VEL * self.game.dt

                    if 0 < new_x < self.game.big_window[0] - self.res[0]:
                              self.pos.x = new_x
                              self.rect.x = self.pos.x
                    if -10 < new_y < self.game.big_window[1] - self.res[1]:
                              self.pos.y = new_y
                              self.rect.y = self.pos.y

          def blit(self):
                    if self.facing == "left": sprite = pygame.transform.flip(self.images[int(self.frame) % len(self.images) - 1], True, False)
                    else: sprite = self.images[int(self.frame) % len(self.images) - 1]
                    self.game.display_screen.blit(sprite, (self.pos.x - self.game.small_window.pos.x, self.pos.y - self.game.small_window.pos.y))

          def update_facing(self, a, d):
                    if a and d: pass
                    elif a: self.facing = "left"
                    elif d: self.facing = "right"

class BG_entities(RectEntity):
          def __init__(self, game, coordinates, res, vel, name):
                    RectEntity.__init__(self, game, coordinates, res, vel, name)
                    self.image = BG_entities_gif[random.randint(0, len(BG_entities_gif) - 1)]
                    self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.width, self.image.height)
                    self.name = name

          def blit(self):
                    self.game.display_screen.blit(self.image, (self.pos.x - self.game.small_window.pos.x, self.pos.y - self.game.small_window.pos.y))

class Enemy(RectEntity, AnimatedEntity, AnimalEntity):
          def __init__(self, game, coordinates, res, vel, name, health, damage, images, angle=None, animation=ANIMATION_SPEED):
                    RectEntity.__init__(self, game, coordinates, res, vel, name, angle)
                    AnimatedEntity.__init__(self, game, images, animation)
                    AnimalEntity.__init__(self, game, health, damage)

          def blit(self):
                    if self.facing == "left": sprite = pygame.transform.flip(self.images[int(self.frame) % len(self.images) - 1], True, False)
                    else: sprite = self.images[int(self.frame) % len(self.images) - 1]
                    self.game.display_screen.blit(sprite, (self.pos.x - self.game.small_window.pos.x, self.pos.y - self.game.small_window.pos.y))

          def update_facing(self):
                    if self.game.player.pos.x - self.pos.x > 0:
                              self.facing = "right"
                    elif self.game.player.pos.x - self.pos.x < 0:
                              self.facing = "left"

          def update(self):
                    if (abs(self.game.player.pos.x + 0.5 * self.game.player.res[
                              0] - self.pos.x - 0.5 * self.rect.width) +
                            abs(self.game.player.pos.y + 0.5 * self.game.player.res[
                                      1] - self.pos.y - 0.5 * self.rect.height) > 25):
                              new_angle = self.calc_angle()
                              rotate = self.angle - new_angle
                              self.vel_vector.rotate_ip(rotate)
                              self.angle = new_angle
                              self.pos.x += self.vel_vector.x * self.game.dt
                              self.pos.y += self.vel_vector.y * self.game.dt
                              self.rect.x = self.pos.x
                              self.rect.y = self.pos.y

class Gun:
          def __init__(self, game, gunImage, gun_res, distance):
                    self.game = game
                    self.res = gun_res
                    self.gunImage = gunImage
                    self.distance = distance
                    self.rect = pygame.Rect(0, 0, self.res[0], self.res[1])
                    self.facing = "right"
                    self.angle = 0

          def draw(self):
                    self.update_facing()
                    self.calc_angle()
                    pos_x = self.game.player.rect.centerx + math.sin(math.radians(self.angle + 180)) * PLAYER_GUN_DISTANCE - self.game.small_window.pos.x + int(self.res[0] / 2) - 0.5 * self.res[0] - 5
                    pos_y = self.game.player.rect.centery + math.cos(math.radians(self.angle + 180)) * PLAYER_GUN_DISTANCE - self.game.small_window.pos.y + int(self.res[1] / 2) - 0.5 * self.res[1] - 5
                    if self.facing == "right":
                              new_image = pygame.transform.rotate(self.gunImage, self.angle + 90)
                              self.rect = new_image.get_rect(center=(pos_x, pos_y))
                              self.game.display_screen.blit(new_image, self.rect)
                    else:
                              new_image = pygame.transform.rotate(self.gunImage, -self.angle + 90)
                              self.rect = new_image.get_rect(center=(pos_x, pos_y))
                              self.game.display_screen.blit(pygame.transform.flip(new_image, True, False), self.rect)

          def update_facing(self):
                    if int(self.game.mouse_pos[0] * REN_RES[0] / self.game.display.width) < self.game.player.rect.centerx - self.game.small_window.pos.x: self.facing = "left"
                    else: self.facing = "right"

          def calc_angle(self):
                    change_in_x = self.game.player.rect.centerx - self.game.small_window.pos.x - int(self.game.mouse_pos[0] * REN_RES[0] / self.game.display.width) - 5
                    change_in_y = self.game.player.rect.centery - self.game.small_window.pos.y - int(self.game.mouse_pos[1] * REN_RES[1] / self.game.display.height) - 5
                    angle = self.angle = v2(change_in_x, change_in_y).angle_to((0, 1))
                    if angle < 0: self.angle = angle + 360
                    else: self.angle = angle
