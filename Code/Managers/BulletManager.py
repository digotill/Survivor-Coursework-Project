from Code.Individuals.Bullet import *
from Code.DataStructures.HashMap import *


class BulletManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, General_Settings["hash_maps"][1])
                    self.bullet_pool = set()

          def update(self):
                    if not self.game.changing_settings:
                              current_time = self.game.game_time
                              for bullet in self.grid.items:
                                        bullet.update()
                                        if current_time - bullet.creation_time > bullet.lifetime:
                                                  bullet.dead = True
                              self.check_for_collisions()
                              self.check_dead_bullets()
                              self.grid.rebuild()

          def draw(self):
                    offset_x, offset_y = self.game.camera.offset_rect.topleft
                    for bullet in self.grid.window_query():
                              self.game.display_surface.blit(bullet.image,
                                                             (bullet.rect.x - offset_x, bullet.rect.y - offset_y))

          def add_bullet(self, pos, angle, name, spread):
                    if self.bullet_pool:
                              bullet = self.bullet_pool.pop()
                              bullet.reset(pos, angle, spread)
                    else:
                              bullet = Bullet(self.game, self.game.player.gun, pos, angle, name, spread, self.game.player.gun.noise_map)
                    self.grid.insert(bullet)
                    array = SCREENSHAKE[self.game.player.gun.name]
                    self.game.camera.add_screen_shake(array[1], array[0])

          def check_dead_bullets(self):
                    for bullet in self.grid.items.copy():
                              if bullet.dead:
                                        self.grid.items.remove(bullet)
                                        self.bullet_pool.add(bullet)

          def check_for_collisions(self):
                    for bullet in self.grid.items:
                              for enemy in self.game.enemy_manager.grid.query(bullet.rect):
                                        if bullet.rect.colliderect(enemy.rect) and not bullet.dead:
                                                  enemy.deal_damage(bullet.damage)
                                                  bullet.check_if_alive()
                                                  angle = bullet.angle if bullet.angle > 0 else 360 + bullet.angle
                                                  self.game.effect_manager.add_effect(bullet.pos, angle, EFFECTS["blood"])
