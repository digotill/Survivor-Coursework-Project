import pygame, math, random
from Variables import *
from Initialize import *
from pygame.math import Vector2 as v2


class RectEntity:
          def __init__(self, game, coordinates, res, vel, name, angle):
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
          def __init__(self, game,  images, animation):
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

                    if a or d or w or s: self.frame += self.animation * self.game.dt

                    if a and d: pass
                    elif a: self.facing = "left"
                    elif d: self.facing = "right"

                    dx, dy = 0, 0
                    if a: dx -= 1
                    if d: dx += 1
                    if s: dy += 1
                    if w: dy -= 1

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
                    if self.facing == "left": sprite = pygame.transform.scale(pygame.transform.flip(self.images[int(self.frame) % len(self.images) - 1], True, False), self.res)
                    else: sprite = pygame.transform.scale(self.images[int(self.frame) % len(self.images) - 1], self.res)
                    self.game.screen.blit(sprite, (self.pos.x - self.game.small_window.pos.x, self.pos.y - self.game.small_window.pos.y))


class Entity:
          def __init__(self, game, health, res, vel, damage, coordinates, name, angle=0, idle=None, run=None, hit=None, animation=ANIMATION_SPEED):
                    self.game = game
                    if idle is not None: self.idle = idle
                    if run is not None: self.run = run
                    if hit is not None: self.hit = hit
                    self.health = health
                    self.res = res
                    self.vel = vel
                    self.pos = v2(coordinates)
                    self.rect = pygame.Rect(self.pos.x, self.pos.y, res[0], res[1])
                    self.damage = damage
                    self.name = name
                    self.facing = "right"
                    self.frame = 0
                    self.animation = animation
                    self.dead = False
                    if angle != 0:
                              self.vel_vector = v2(self.vel * math.sin(math.radians(angle)), self.vel * math.cos(math.radians(angle)))
                              self.angle = angle
                    if name == "Player":
                              self.stamina = PLAYER_STAMINA

          def blit(self):
                    if self.facing == "left": sprite = pygame.transform.scale(pygame.transform.flip(self.idle[int(self.frame) % len(self.idle) - 1], True, False), self.res)
                    else: sprite = pygame.transform.scale(self.idle[int(self.frame) % len(self.idle) - 1], self.res)
                    self.game.screen.blit(sprite, (self.pos.x - self.game.small_window.pos.x, self.pos.y - self.game.small_window.pos.y))

          def calc_angle(self):
                    return v2(self.game.player.pos.x + 0.5 * self.game.player.res[0] - self.pos.x - 0.5 * self.res[0], self.game.player.pos.y + 0.5 * self.game.player.res[1] - self.pos.y - 0.5 * self.res[1]).angle_to((0, 1))

          def update(self):
                    a = self.game.keys[pygame.K_a]
                    d = self.game.keys[pygame.K_d]
                    w = self.game.keys[pygame.K_w]
                    s = self.game.keys[pygame.K_s]

                    if a or d or w or s: self.frame += self.animation * self.game.dt

                    if a and d: pass
                    elif a: self.facing = "left"
                    elif d: self.facing = "right"

                    dx, dy = 0, 0
                    if a: dx -= 1
                    if d: dx += 1
                    if s: dy += 1
                    if w: dy -= 1

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

class Gun:
          def __init__(self, game, gunImages, Bullet, gun_res, bullet_res, bullet_speed, bullet_damage, bullet_range, bullet_frequency, animation=ANIMATION_SPEED):
                    self.game = game
                    self.gunImages = []
                    for i in range(len(gunImages)):
                              self.gunImages.append(pygame.transform.scale(gunImages[i], gun_res))
                    self.gun_res = gun_res
                    self.bullet_res = bullet_res
                    self.bulletImage = Bullet
                    self.bullet_speed = bullet_speed
                    self.bullet_damage = bullet_damage
                    self.bullet_range = bullet_range
                    self.bullet_frequency = bullet_frequency
                    self.last_shot_time = 0
                    self.facing = "right"
                    self.frame = 0
                    self.animation = animation


          def draw(self):
                    if self.game.mouse_pos[0] < self.game.player.pos[0] - self.game.small_window.pos.x: self.facing = "left"
                    else: self.facing = "right"

                    player_x = int(self.game.player.pos.x + 0.5 * self.game.player.res[0] - self.game.small_window.pos.x) / 1920
                    player_y = int(self.game.player.pos.y + 0.5 * self.game.player.res[1] - self.game.small_window.pos.y) / 1080

                    angle = v2(player_x * pygame.display.get_window_size()[0] - self.game.mouse_pos[0], player_y * pygame.display.get_window_size()[1] - self.game.mouse_pos[1]).angle_to((0, 1))
                    if angle < 0: angle += 360
                    if self.facing == "left": sprite = pygame.transform.scale(pygame.transform.flip(self.gunImages[int(self.frame) % len(self.gunImages) - 1], True, False), self.gun_res)
                    else: sprite = pygame.transform.scale(self.gunImages[int(self.frame) % len(self.gunImages) - 1], self.gun_res)
                    if 180 > angle: sprite = pygame.transform.rotate(sprite, angle - 90)
                    else: sprite = pygame.transform.rotate(sprite, angle + 90)

                    self.frame += self.animation * self.game.dt
                    self.game.screen.blit(sprite, (self.game.player.pos[0] - self.game.small_window.pos.x - int(sprite.get_width()/2), self.game.player.pos[1] - int(sprite.get_height()/2) - self.game.small_window.pos.y))

class BG_entities:
          def __init__(self, coordinates):
                    self.x = coordinates[0]
                    self.y = coordinates[1]
                    self.image = BG_entities_gif[random.randint(0, len(BG_entities_gif) - 1)]
                    self.rect = pygame.Rect(self.x, self.y, self.image.width, self.image.height)

