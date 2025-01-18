from Code.Variables.Variables import *


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

                    self.update_rect()

          def calculate_movement(self):
                    return [math.cos(self.angle) * self.speed * self.game.dt,
                            math.sin(self.angle) * self.speed * self.game.dt]

          def move(self):
                    movement = self.calculate_movement()
                    self.pos.x += movement[0]
                    self.pos.y += movement[1]

                    deceleration_factor = 1 - (General_Settings["sparks"][0] * self.game.dt)

                    deceleration_factor = max(0, min(1, deceleration_factor))

                    self.speed *= deceleration_factor

                    if self.speed <= General_Settings["sparks"][3]:
                              self.alive = False

                    self.update_rect()

          def draw(self):
                    offset = self.game.camera.offset_rect.topleft
                    points = self.calculate_points(offset)
                    pygame.draw.polygon(self.game.display_screen, self.color, points)

          def update_rect(self):
                    points = self.calculate_points(offset=(0, 0))
                    min_x = min(point[0] for point in points)
                    max_x = max(point[0] for point in points)
                    min_y = min(point[1] for point in points)
                    max_y = max(point[1] for point in points)

                    width = max_x - min_x
                    height = max_y - min_y
                    self.rect = pygame.Rect(min_x, min_y, width, height)

          def calculate_points(self, offset):
                    height = General_Settings["sparks"][2]
                    width = General_Settings["sparks"][1]
                    front_point = self.calculate_point(self.angle, self.speed * self.scale, offset)
                    back_point = self.calculate_point(self.angle + math.pi, self.speed * self.scale * height,
                                                      offset)
                    left_point = self.calculate_point(self.angle + math.pi / 2, self.speed * self.scale * width,
                                                      offset)
                    right_point = self.calculate_point(self.angle - math.pi / 2, self.speed * self.scale * width,
                                                       offset)
                    return [front_point, left_point, back_point, right_point]

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
