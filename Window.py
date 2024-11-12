import pygame, math
from Variables import *
from pygame.math import Vector2 as v2

class Window:
          def __init__(self, game, res, big_res):
                    self.game = game
                    self.width = res[0]
                    self.height = res[1]
                    self.pos = v2(big_res[0] / 2 - self.width / 2, big_res[1] / 2 - self.height / 2)
                    self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
                    self.vel = PLAYER_VEL
                    self.offset_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

          def move(self):
                    a = self.game.keys[pygame.K_a]
                    d = self.game.keys[pygame.K_d]
                    w = self.game.keys[pygame.K_w]
                    s = self.game.keys[pygame.K_s]

                    dx, dy = 0, 0
                    if a: dx -= 1
                    if d: dx += 1
                    if s: dy += 1
                    if w: dy -= 1

                    magnitude = math.sqrt(dx ** 2 + dy ** 2)
                    if magnitude != 0:
                              dx /= magnitude
                              dy /= magnitude

                    new_x = self.pos.x + dx * self.game.player.current_vel * self.game.dt
                    new_y = self.pos.y + dy * self.game.player.current_vel * self.game.dt

                    if self.width / 2 < self.game.player.pos.x < self.game.big_window[0] - self.width / 2:
                              self.pos.x = new_x
                              self.rect.x = self.pos.x
                              x_diff = int(int(self.game.mouse_pos[0] * REN_RES[0] / self.game.display.width) - 0.5 * REN_RES[0])
                              self.offset_rect.x = self.rect.x + 0.3 * x_diff
                    if self.height / 2 < self.game.player.pos.y < self.game.big_window[1] - self.height / 2:
                              self.pos.y = new_y
                              self.rect.y = self.pos.y
                              y_diff = int(int(self.game.mouse_pos[1] * REN_RES[1] / self.game.display.height) - 0.5 * REN_RES[1])
                              self.offset_rect.y = self.rect.y + 0.3 * y_diff

# + int(self.game.mouse_pos[0] * REN_RES[0] / self.game.display.width) - 0.5 * REN_RES[0]
