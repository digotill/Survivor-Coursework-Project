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

class BG_entities(RectEntity):
          def __init__(self, game, coordinates, res, vel, name):
                    RectEntity.__init__(self, game, coordinates, res, vel, name)
                    self.image = pygame.transform.scale(BG_entities_gif[random.randint(0, len(BG_entities_gif) - 1)], res)
                    self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.width, self.image.height)
                    self.name = name
                    self.image = BG_sprites[random.randint(0, len(BG_sprites) - 1)]

          def blit(self):
                    self.game.screen.blit(self.image, (self.pos.x - self.game.small_window.pos.x, self.pos.y - self.game.small_window.pos.y))

class Enemy(RectEntity, AnimatedEntity, AnimalEntity):
          def __init__(self, game, coordinates, res, vel, name, health, damage, images, angle=None, animation=ANIMATION_SPEED):
                    RectEntity.__init__(self, game, coordinates, res, vel, name, angle)
                    AnimatedEntity.__init__(self, game, images, animation)
                    AnimalEntity.__init__(self, game, health, damage)

          def blit(self):
                    if self.facing == "left": sprite = pygame.transform.scale(pygame.transform.flip(self.images[int(self.frame) % len(self.images) - 1], True, False), self.res)
                    else: sprite = pygame.transform.scale(self.images[int(self.frame) % len(self.images) - 1], self.res)
                    self.game.screen.blit(sprite, (self.pos.x - self.game.small_window.pos.x, self.pos.y - self.game.small_window.pos.y))


class Gun2:
          def __init__(self, game, gunImage, gun_res, distance):
                    self.game = game
                    self.gun_res = gun_res
                    self.gunImage = pygame.transform.scale(gunImage, gun_res)
                    self.distance = distance
                    self.facing = "right"
                    self.angle = 0

          def draw(self):
                    self.update_facing()
                    self.calc_angle(self.game.mouse_pos)
                    pos_x = self.game.player.rect.centerx + math.sin(math.radians(self.angle))
                    pos_y = self.game.player.rect.centery + math.cos(math.radians(self.angle))
                    self.game.display_screen.blit(pygame.transform.rotate(self.gunImage, self.angle), (pos_x, pos_y))

          def update_facing(self):
                    if self.game.mouse_pos[0] < self.game.player.pos[0] - self.game.small_window.pos.x: self.facing = "left"
                    else: self.facing = "right"

          def calc_angle(self, pos):
                    angle = v2(self.game.player.pos.x + 0.5 * self.game.player.res[0] - pos[0] - 0.5 * self.gun_res[0], self.game.player.pos.y + 0.5 * self.game.player.res[1] - pos[1] - 0.5 * self.gun_res[1]).angle_to((0, 1))
                    if angle < 0: angle += 360
                    self.angle = angle


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


