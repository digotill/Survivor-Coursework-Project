from Code.Individuals.Parent import *

class Rain(main):
          def __init__(self, game, dictionary):
                    self.game = game
                    self.animation = AM.assets["rain"]
                    self.res = AM.assets["rain"][0].size
                    self.set_attributes(dictionary)
                    self.pos = v2(change_by_diff(self.game.camera.offset_rect.x, self.game.camera.offset_rect.width),
                                  self.game.camera.offset_rect.y - self.game.camera.offset_rect.height / 2)

                    self.spawn_time = self.game.game_time
                    self.initial_vel = self.vel
                    self.hit_ground = False
                    self.lifetime = change_by_diff(self.lifetime, self.lifetime_randomness)
                    self.vel = change_by_diff(self.vel, self.vel_randomness)
                    self.vel_vector = self.calculate_vel_vector()
                    self.set_rect()
                    self.frame = 0

          def calculate_vel_vector(self):
                    angle_rad = math.radians(self.angle)

                    vel_x = self.vel * math.sin(angle_rad)
                    vel_y = self.vel * math.cos(angle_rad)

                    return v2(vel_x, vel_y)

          def update(self):
                    self.lifetime -= self.game.dt

                    if self.lifetime <= 0:
                              self.hit_ground = True

                    if not self.hit_ground:
                              self.pos += self.vel_vector * self.game.dt
                              self.rect.center = self.pos

          def draw(self, surface=None):
                    if surface is None:
                              surface = self.game.display_surface
                    pos = self.rect.x - self.game.camera.offset_rect.x, self.rect.y - self.game.camera.offset_rect.y
                    if not self.hit_ground:
                              surface.blit(self.animation[0], pos)
                    else:
                              surface.blit(
                                        self.animation[
                                                  int(self.frame % len(self.animation))], pos)