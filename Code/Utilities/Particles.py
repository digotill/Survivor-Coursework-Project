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

          def point_towards(self, angle, rate):
                    global rotate_sign
                    rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
                    try:
                              rotate_sign = abs(rotate_direction) / rotate_direction
                    except ZeroDivisionError:
                              rotate_sign = 1
                    if abs(rotate_direction) < rate:
                              self.angle = angle
                    else:
                              self.angle += rate * rotate_sign

          def calculate_movement(self):
                    return [math.cos(self.angle) * self.speed * self.game.dt, math.sin(self.angle) * self.speed * self.game.dt]

          # gravity and friction
          def velocity_adjust(self, friction, force, terminal_velocity, dt):
                    movement = self.calculate_movement()
                    movement[1] = min(terminal_velocity, movement[1] + force * dt)
                    movement[0] *= friction
                    self.angle = math.atan2(movement[1], movement[0])
                    # if you want to get more realistic, the speed should be adjusted here

          def move(self):
                    movement = self.calculate_movement()
                    self.loc[0] += movement[0]
                    self.loc[1] += movement[1]

                    # a bunch of options to mess around with relating to angles...
                    #self.point_towards(math.pi / 2, 0.02)
                    #self.velocity_adjust(0.975, 0.2, 8, dt)
                    #self.angle += 0.1

                    self.speed -= 0.1

                    if self.speed <= 0:
                              self.alive = False

          def draw(self, offset=None):
                    if offset is None:
                              offset = [0, 0]
                    if self.alive:
                              points = [
                                        [self.loc[0] + math.cos(self.angle) * self.speed * self.scale,
                                         self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                                        [self.loc[0] + math.cos(
                                                  self.angle + math.pi / 2) * self.speed * self.scale * 0.3,
                                         self.loc[1] + math.sin(
                                                   self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                                        [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5,
                                         self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                                        [self.loc[0] + math.cos(
                                                  self.angle - math.pi / 2) * self.speed * self.scale * 0.3,
                                         self.loc[1] - math.sin(
                                                   self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                              ]
                              pygame.draw.polygon(self.game.display_screen, self.color, points)
