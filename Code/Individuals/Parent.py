from Code.Variables.SettingsVariables import *

class main:
          def set_attributes(self, attributes):
                    for key, value in attributes.items():
                              setattr(self, key, value)

                    self.facing = "right"
                    self.dead = False
                    self.creation_time = self.game.game_time

                    if hasattr(self, 'vel'):
                              self.max_vel = self.vel
                              self.current_vel = 0
                    if hasattr(self, 'health'):
                              self.max_health = self.health
                    if hasattr(self, 'stamina'):
                              self.max_stamina = self.stamina
                    if hasattr(self, 'animation_speed'):
                              self.frame = 0
                    if hasattr(self, 'hit_cooldown'):
                              self.last_hit = - self.hit_cooldown

          def update_frame(self):
                    self.frame += self.animation_speed * self.game.dt

          def set_rect(self):
                    self.rect = pygame.Rect(self.pos.x - self.res[0] / 2, self.pos.y - self.res[1] / 2, self.res[0],
                                            self.res[1])

          def get_position(self):
                    return self.rect.x - self.game.camera.offset_rect.x, self.rect.y - self.game.camera.offset_rect.y

          def get_mid_position(self):
                    return self.rect.centerx - self.game.camera.offset_rect.x, self.rect.centery - self.game.camera.offset_rect.y

          def deal_damage(self, damage):
                    if self.game.game_time - self.last_hit > self.hit_cooldown:
                              self.health -= damage
                              self.check_if_alive()
                              self.last_hit = self.game.game_time

          def check_if_alive(self):
                    if self.health <= 0:
                              self.dead = True
                              self.health = 0

