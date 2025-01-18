from Code.Individuals.Parent import *

class Bullet(main):
          def __init__(self, game, gun, pos, angle, name, spread_factor, shake_map):
                    self.game = game
                    self.gun = gun
                    self.name = name
                    noise_value = shake_map([game.game_time * Perlin_Noise["gun_shake_map"][0], 0])
                    spread_angle = noise_value * gun.spread * spread_factor
                    self.angle = angle + spread_angle
                    self.image = pygame.transform.rotate(gun.bullet_image, self.angle + 90)
                    self.original_image = gun.bullet_image

                    self.pos = v2(pos)
                    self.vel_vector = v2(0, -gun.vel).rotate(-self.angle)
                    self.rect = self.image.get_rect(center=self.pos)
                    self.res = self.rect.size

                    self.lifetime = change_by_diff(self.gun.lifetime, self.gun.lifetime_randomness)
                    self.dead = False
                    self.creation_time = game.game_time
                    self.friction = self.gun.friction
                    self.damage = self.gun.damage
                    self.pierce = self.gun.pierce
                    self.health = self.pierce

          def update(self):
                    if self.friction > 0:
                              self.vel_vector *= (1 - self.friction * self.game.dt)

                    self.pos += self.vel_vector * self.game.dt
                    self.rect.center = self.pos

          def check_collision(self, target):
                    if self.rect.colliderect(target.rect):
                              target.health -= self.damage
                              self.health -= 1
                              if self.health <= 0:
                                        self.dead = True
                              return True
                    return False

          def reset(self, pos, angle, spread):
                    self.__init__(self.game, self.gun, pos, angle, self.name, spread, self.game.player.gun.noise_map)