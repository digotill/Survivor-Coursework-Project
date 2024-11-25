import pygame, sys, math, random

pygame.init()

class Spark:
          def __init__(self, game, loc, angle, speed, color, scale=1):
                    self.game = game
                    self.loc = loc
                    self.angle = angle
                    self.speed = speed
                    self.scale = scale
                    self.color = color
                    self.alive = True

          def calculate_movement(self):
                    return [math.cos(self.angle) * self.speed * self.game.dt, math.sin(self.angle) * self.speed * self.game.dt]

          def move(self):
                    movement = self.calculate_movement()
                    self.loc[0] += movement[0]
                    self.loc[1] += movement[1]

                    if self.speed * 0.95 * self.game.dt * 235 < self.speed: self.speed *= 0.95 * self.game.dt * 235
                    elif self.speed * 0.95 * self.game.dt < self.speed: self.speed *= 0.95 * self.game.dt

                    if self.speed <= 0.1:
                              self.alive = False

          def draw(self):
                    if self.alive:
                              points = [
                                        [self.loc[0] + math.cos(self.angle) * self.speed * self.scale - self.game.window.offset_rect.x,
                                                  self.loc[1] + math.sin(self.angle) * self.speed * self.scale - self.game.window.offset_rect.y],
                                        [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3 - self.game.window.offset_rect.x,
                                                  self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3 - self.game.window.offset_rect.y],
                                        [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5 - self.game.window.offset_rect.x,
                                                  self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5 - self.game.window.offset_rect.y],
                                        [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3 - self.game.window.offset_rect.x,
                                                  self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3 - self.game.window.offset_rect.y],
                              ]
                              pygame.draw.polygon(self.game.display_screen, self.color, points)
