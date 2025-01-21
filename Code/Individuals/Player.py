from Code.Individuals.Parent import *
from Code.Individuals.Gun import *

class Player(main):
          def __init__(self, game):
                    self.game = game

                    self.set_attributes(Player_Attributes)
                    self.res = AM.assets["player_idle"][0].size
                    self.pos = self.find_spawn_position()
                    self.set_rect()
                    self.current_vel = 0
                    self.gun = Gun(self.game, Weapons["ak47"])
                    self.base_max_vel = self.max_vel
                    self.current_animation = 'idle'
                    self.is_sprinting = False

          def find_spawn_position(self):
                    center_x, center_y = GAME_SIZE[0] // 2, GAME_SIZE[1] // 2
                    max_distance = max(GAME_SIZE[0], GAME_SIZE[1])

                    for distance in range(0, max_distance, 16):
                              for angle in range(0, 360, 10):
                                        x = center_x + int(distance * math.cos(math.radians(angle)))
                                        y = center_y + int(distance * math.sin(math.radians(angle)))

                                        if 0 <= x < GAME_SIZE[0] and 0 <= y < GAME_SIZE[1]:
                                                  test_rect = pygame.Rect(x, y, self.res[0], self.res[1])
                                                  if not self.game.tilemap_manager.tile_collision(test_rect, "water_tile"):
                                                            return v2(x, y)

          def change_animation(self, animation_name):
                    if self.current_animation != animation_name:
                              self.current_animation = animation_name
                              self.frame = 0

          def update_animation(self):
                    new_animation = 'running' if (self.game.keys[pygame.K_a] or self.game.keys[pygame.K_d] or
                                                  self.game.keys[pygame.K_s] or self.game.keys[pygame.K_w]) else 'idle'
                    self.change_animation(new_animation)

          def update(self):
                    dx, dy = 0, 0
                    if self.game.keys[pygame.K_a]: dx -= 1
                    if self.game.keys[pygame.K_d]: dx += 1
                    if self.game.keys[pygame.K_s]: dy += 1
                    if self.game.keys[pygame.K_w]: dy -= 1

                    magnitude = math.sqrt(dx ** 2 + dy ** 2)
                    if magnitude != 0:
                              dx /= magnitude
                              dy /= magnitude

                    self.is_sprinting = self.game.keys[Keys['sprint']] and (dx != 0 or dy != 0)
                    if not self.game.changing_settings: self.handle_stamina()
                    self.max_vel = self.sprint_vel if self.is_sprinting else self.base_max_vel
                    x_water_collision = self.game.tilemap_manager.tile_collision(pygame.Rect(self.pos.x, self.pos.y + self.res[1] / 2, 0, 0), "water_tile")
                    y_water_collision = self.game.tilemap_manager.tile_collision(pygame.Rect(self.pos.x, self.pos.y + self.res[1] / 2, 0, 0), "water_tile")
                    if x_water_collision or y_water_collision:
                              self.max_vel = self.slowed_vel
                              self.health -= Damages["acid"] * self.game.dt

                    if not self.game.changing_settings: self.update_frame()
                    self.update_velocity(dy, dx)
                    self.update_facing()

                    new_x = self.pos.x + dx * self.current_vel * self.game.dt
                    new_y = self.pos.y + dy * self.current_vel * self.game.dt

                    move_hor, move_vert = False, False
                    if not self.game.changing_settings:

                              if self.offset[0] + self.res[0] / 2 < new_x < GAME_SIZE[0] - self.res[0] / 2 + \
                                      self.offset[2]:
                                        self.pos.x = new_x
                                        self.rect.centerx = self.pos.x
                                        move_hor = True
                              if self.offset[1] + self.res[1] / 2 < new_y < GAME_SIZE[1] - self.res[1] / 2 + \
                                      self.offset[3]:
                                        self.pos.y = new_y
                                        self.rect.centery = self.pos.y
                                        move_vert = True

                    self.game.grass_manager.apply_force(self.rect.midbottom, self.rect.width, self.grass_force)
                    self.game.camera.move(dx, dy, move_hor, move_vert)
                    self.update_animation()

          def draw(self):
                    current_animation = self.game.assets["player_" + self.current_animation + "_" + self.facing]
                    frame_index = int(self.frame) % len(current_animation)
                    image = current_animation[frame_index]

                    shadow_image = self.generate_shadow_image(image)
                    self.game.display_surface.blit(shadow_image, (self.get_position()[0], self.get_position()[1] + self.res[1] - shadow_image.height / 2))
                    self.game.display_surface.blit(image, self.get_position())

                    self.gun.draw()

          def handle_stamina(self):
                    if self.is_sprinting and self.current_vel > 0:
                              self.stamina -= self.stamina_consumption * self.game.dt
                              self.stamina = max(0,
                                                 self.stamina)
                    else:
                              self.stamina += self.stamina_recharge_rate * self.game.dt
                              self.stamina = min(self.max_stamina,
                                                 self.stamina)

                    if self.stamina <= 0:
                              self.is_sprinting = False

          def update_frame(self):
                    factor = self.max_vel / self.base_max_vel
                    self.frame += self.animation_speed * factor * self.game.dt

          def update_facing(self):
                    if self.game.correct_mouse_pos[0] < self.get_mid_position()[0]:
                              self.facing = "left"
                    else:
                              self.facing = "right"

          def update_velocity(self, dy, dx):
                    if dy != 0 or dx != 0:
                              self.current_vel = min(self.current_vel + self.acceleration * self.game.dt, self.max_vel)
                    else:
                              self.current_vel = max(self.current_vel - self.acceleration * self.game.dt, 0)