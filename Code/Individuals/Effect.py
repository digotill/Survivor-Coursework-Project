from Code.Variables.SettingsVariables import *


class Effect:
          def __init__(self, game, pos, angle, dictionary):
                    self.game = game

                    self.game.methods.set_attributes(self, dictionary)

                    self.pos = v2(pos)
                    self.set_rect()
                    self.images = self.game.assets[self.name + "_" + str(random.randint(2, 11))]
                    self.frame = 0
                    self.length = len(self.images) - 1
                    self.alpha = 255
                    self.end_frame = random.randint(0, self.length)

                    self.speed = self.speed[0] + random.uniform(-self.speed[0], self.speed[0])  # Add randomness to speed
                    self.vel_vector = v2(0, -self.speed).rotate(-angle)

                    self.grounded = False
                    self.grounded_time = 0
                    self.time_when_grounded = None

          def update(self):
                    if not self.grounded:
                              if self.frame >= self.end_frame:
                                        self.grounded = True
                              else:
                                        self.pos += self.vel_vector * self.game.dt
                                        self.rect.center = self.pos
                                        self.frame += self.animation_speed * self.game.dt
                    elif self.grounded:
                              if self.time_when_grounded is None:
                                        self.time_when_grounded = self.game.game_time
                              self.grounded_time = self.game.game_time - self.time_when_grounded
                              if self.grounded_time > self.vanish_time[0]:
                                        fade_duration = self.vanish_time[1]
                                        fade_progress = min((self.grounded_time - self.vanish_time[0]) / fade_duration, 1)
                                        self.alpha = int(255 * (1 - fade_progress))

          def draw(self, surface=None):
                    if surface is None:
                              surface = self.game.display_surface
                    if not self.grounded: frame = int(self.frame) % len(self.images)
                    else: frame = self.end_frame
                    image = self.images[frame]

                    # Apply transparency
                    image = self.game.methods.get_transparent_image(image, self.alpha)

                    surface.blit(image, (self.rect.x - self.game.camera.offset_rect.x, self.rect.y - self.game.camera.offset_rect.y))

          def set_rect(self):
                    self.rect = pygame.Rect(self.pos.x - self.res[0] / 2, self.pos.y - self.res[1] / 2, self.res[0],
                                            self.res[1])