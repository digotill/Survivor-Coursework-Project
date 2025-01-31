from Code.Variables.SettingVariables import *

from Code.Variables.SettingVariables import *


class Spark():
          def __init__(self, game, pos, angle, speed, color, scale=1):
                    self.game = game  # Reference to the main game object
                    self.pos = v2(pos)  # Position of the spark
                    self.angle = angle  # Direction of the spark's movement
                    self.speed = speed  # Speed of the spark
                    self.scale = scale  # Size scale of the spark
                    self.color = color  # Color of the spark
                    self.alive = True  # Flag to determine if the spark is still active

                    self.update_rect()  # Initialize the spark's rectangle

          def calculate_movement(self):
                    # Calculate the movement vector based on angle and speed
                    return [math.cos(self.angle) * self.speed * self.game.dt,
                            math.sin(self.angle) * self.speed * self.game.dt]

          def move(self):
                    # Update the spark's position
                    movement = self.calculate_movement()
                    self.pos.x += movement[0]
                    self.pos.y += movement[1]

                    # Apply deceleration
                    deceleration_factor = 1 - (GENERAL["sparks"][0] * self.game.dt)
                    deceleration_factor = max(0, min(1, deceleration_factor))
                    self.speed *= deceleration_factor

                    # Check if the spark should die
                    if self.speed <= GENERAL["sparks"][3]:
                              self.alive = False

                    self.update_rect()  # Update the spark's rectangle

          def draw(self):
                    # Draw the spark on the game's display surface
                    offset = self.game.camera.offset_rect.topleft
                    points = self.calculate_points(offset)
                    pygame.draw.polygon(self.game.display_surface, self.color, points)

          def update_rect(self):
                    # Update the spark's bounding rectangle
                    points = self.calculate_points(offset=(0, 0))
                    min_x = min(point[0] for point in points)
                    max_x = max(point[0] for point in points)
                    min_y = min(point[1] for point in points)
                    max_y = max(point[1] for point in points)

                    width = max_x - min_x
                    height = max_y - min_y
                    self.rect = pygame.Rect(min_x, min_y, width, height)

          def calculate_points(self, offset):
                    # Calculate the four points of the spark's polygon
                    height = GENERAL["sparks"][2]
                    width = GENERAL["sparks"][1]
                    front_point = self.calculate_point(self.angle, self.speed * self.scale, offset)
                    back_point = self.calculate_point(self.angle + math.pi, self.speed * self.scale * height, offset)
                    left_point = self.calculate_point(self.angle + math.pi / 2, self.speed * self.scale * width, offset)
                    right_point = self.calculate_point(self.angle - math.pi / 2, self.speed * self.scale * width, offset)
                    return [front_point, left_point, back_point, right_point]

          def calculate_point(self, angle, distance, offset):
                    # Calculate a point based on an angle and distance from the spark's position
                    return (
                              self.pos.x + math.cos(angle) * distance - offset[0],
                              self.pos.y + math.sin(angle) * distance - offset[1]
                    )

          def reset(self, pos, angle, speed, color, scale=1):
                    # Reset the spark with new parameters
                    self.pos = v2(pos)
                    self.angle = angle
                    self.speed = speed
                    self.scale = scale
                    self.color = color
                    self.alive = True
