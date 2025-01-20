from Code.Individuals.Parent import *

class Gun(main):
          def __init__(self, game, dictionary):
                    self.game = game

                    self.set_attributes(dictionary)

                    self.gun_image = AM.assets[self.name]
                    self.res = AM.assets[self.name].size
                    self.bullet_image = AM.assets[self.name + "_bullet"]

                    self.pos = v2(0, 0)
                    self.rect = pygame.Rect(0, 0, self.res[0], self.res[1])
                    self.noise_map = PerlinNoise(Map_Config["gun_shake_map"][1], random.randint(0, 100000))

                    self.last_shot = - self.fire_rate
                    self.initial_vel = self.vel
                    self.continuous_fire_start = 0

          def update(self):
                    self.calc_angle()
                    self.update_shooting()

          def draw(self):
                    if self.game.player.facing == "right":
                              self.rotated_image = pygame.transform.rotate(self.gun_image, self.angle + 90)
                    else:
                              self.rotated_image = pygame.transform.flip(
                                        pygame.transform.rotate(self.gun_image, -self.angle + 90), True, False)

                    pos_x = (self.game.player.rect.centerx + math.sin(
                              math.radians(self.angle)) * self.distance -
                             self.game.camera.offset_rect.x)
                    pos_y = (self.game.player.rect.centery + math.cos(
                              math.radians(self.angle)) * self.distance -
                             self.game.camera.offset_rect.y)
                    self.rect = self.rotated_image.get_rect(center=(pos_x, pos_y))
                    self.game.display_surface.blit(self.rotated_image, self.rect)

          def calc_angle(self):
                    change_in_x = self.game.player.rect.centerx - self.game.camera.offset_rect.x - \
                                  self.game.correct_mouse_pos[0]
                    change_in_y = self.game.player.rect.centery - self.game.camera.offset_rect.y - \
                                  self.game.correct_mouse_pos[1]
                    self.angle = v2(change_in_x, change_in_y).angle_to((0, 1))

          def update_shooting(self):
                    current_time = self.game.game_time
                    if self.can_shoot(current_time):
                              self.shoot(current_time)
                    elif not self.game.mouse_state[0]:
                              self.continuous_fire_start = None

          def can_shoot(self, current_time):
                    return (self.fire_rate + self.last_shot < current_time and
                            self.game.mouse_state[0] and
                            not self.game.changing_settings)

          def shoot(self, current_time):
                    if self.continuous_fire_start is None:
                              self.continuous_fire_start = current_time

                    firing_duration = current_time - self.continuous_fire_start
                    max_spread_time = self.spread_time
                    spread_factor = min(firing_duration / max_spread_time, 1.0)

                    self.last_shot = current_time

                    start_coordinates = self.calculate_bullet_start_position()
                    for _ in range(self.shots):
                              self.game.spark_manager.create_spark(270 - self.angle, start_coordinates,
                                                                   Sparks_Settings['muzzle_flash'])
                              if self.shots == 1:
                                        self.game.bullet_manager.add_bullet(start_coordinates, self.angle,
                                                                            "Player Bullet", spread_factor)
                              else:
                                        self.game.bullet_manager.add_bullet(start_coordinates,
                                                                            change_by_diff(self.angle, self.spread),
                                                                            "Player Bullet", spread_factor)

          def calculate_bullet_start_position(self):
                    start_x = self.game.player.rect.centerx + math.sin(math.radians(self.angle)) * int(
                              self.distance - self.res[0])
                    start_y = self.game.player.rect.centery + math.cos(math.radians(self.angle)) * int(
                              self.distance - self.res[0])
                    return start_x, start_y