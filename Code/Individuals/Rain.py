from Code.Variables.SettingsVariables import *

class Rain:
          def __init__(self, game, dictionary):
                    self.game = game
                    self.animation = self.game.assets["rain"]
                    self.res = self.game.assets["rain"][0].size
                    self.game.methods.set_attributes(self, dictionary)
                    self.pos = v2(self.game.methods.change(self.game.camera.offset_rect.x * 1.1, self.game.camera.offset_rect.width / 1.1),
                                  self.game.camera.offset_rect.y - self.game.camera.offset_rect.height / 4)

                    self.spawn_time = self.game.game_time
                    self.initial_vel = self.vel
                    self.hit_ground = False
                    self.lifetime = self.game.methods.change(self.lifetime[0], self.lifetime[1])
                    self.vel = self.game.methods.change(self.vel[0], self.vel[1])
                    self.vel_vector = self.calculate_vel_vector()
                    self.game.methods.set_rect(self)
                    self.frame = 0

          def update_frame(self):
                    self.frame += self.animation_speed * self.game.dt

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