import math
import pygame
from Code.Variables.Variables import *

pygame.init()

class main:
          def set_attributes(self, attributes):
                    for key, value in attributes.items():
                              setattr(self, key, value)

class Spark(main):
          def __init__(self, game, pos, angle, speed, color, scale=1):
                    self.game = game
                    self.pos = v2(pos)
                    self.angle = angle
                    self.speed = speed
                    self.scale = scale
                    self.color = color
                    self.alive = True

                    self.set_attributes(General_Spark_Settings)

          def calculate_movement(self):
                    return [math.cos(self.angle) * self.speed * self.game.dt,
                            math.sin(self.angle) * self.speed * self.game.dt]

          def move(self):
                    movement = self.calculate_movement()
                    self.pos.x += movement[0]
                    self.pos.y += movement[1]

                    deceleration_factor = 1 - (self.friction * self.game.dt)

                    deceleration_factor = max(0, min(1, deceleration_factor))

                    self.speed *= deceleration_factor

                    if self.speed <= self.min_vel:
                              self.alive = False

          def draw(self):

                    offset = self.game.window.offset_rect.topleft
                    front_point = self.calculate_point(self.angle, self.speed * self.scale, offset)
                    back_point = self.calculate_point(self.angle + math.pi, self.speed * self.scale * self.height, offset)
                    left_point = self.calculate_point(self.angle + math.pi / 2, self.speed * self.scale * self.width, offset)
                    right_point = self.calculate_point(self.angle - math.pi / 2, self.speed * self.scale * self.width, offset)

                    points = [front_point, left_point, back_point, right_point]
                    pygame.draw.polygon(self.game.display_screen, self.color, points)

          def calculate_point(self, angle, distance, offset):
                    return (
                              self.pos.x + math.cos(angle) * distance - offset[0],
                              self.pos.y + math.sin(angle) * distance - offset[1]
                    )

          def reset(self, pos, angle, speed, color, scale=1):
                    self.pos = v2(pos)
                    self.angle = angle
                    self.speed = speed
                    self.scale = scale
                    self.color = color
                    self.alive = True
