from Code.Variables.SettingsVariables import *


class Effect:
          def __init__(self, game, images, pos, speed, direction, lifetime):
                    self.game = game
                    self.images = images
                    self.frame = 0
                    self.transparency = 1.0
                    self.pos = v2(pos)
                    self.speed = speed + random.uniform(-0.5, 0.5)  # Add randomness to speed
                    self.direction = direction + random.uniform(-0.1, 0.1)  # Add randomness to direction
                    self.lifetime = lifetime + random.uniform(-0.2, 0.2) * lifetime  # Random lifetime variation
                    self.time_alive = 0
                    self.grounded = False
                    self.curve_amplitude = random.uniform(5, 15)
                    self.curve_frequency = random.uniform(0.05, 0.1)

          def update(self):
                    dt = self.game.dt
                    if not self.grounded:
                              self.time_alive += dt
                              if self.time_alive >= self.lifetime:
                                        self.grounded = True
                              else:
                                        # Move in a curve
                                        self.pos.x += math.cos(self.direction) * self.speed * dt
                                        self.pos.y += math.sin(self.direction) * self.speed * dt
                                        # Add curved motion
                                        self.pos.x += math.sin(self.time_alive * self.curve_frequency) * self.curve_amplitude * dt

                                        # Update frame for animation
                                        self.frame = (self.frame + 1) % len(self.images)
                    else:
                              # When grounded, don't update the frame
                              pass

          def draw(self, surface):
                    if not self.grounded:
                              image = self.images[self.frame]
                    else:
                              # Use the last frame when grounded
                              image = self.images[-1]

                    # Apply transparency
                    alpha = int(255 * self.transparency)
                    image.set_alpha(alpha)

                    surface.blit(image, self.pos)

          def set_transparency(self, value):
                    self.transparency = max(0, min(1, value))

          def is_alive(self):
                    return self.transparency > 0