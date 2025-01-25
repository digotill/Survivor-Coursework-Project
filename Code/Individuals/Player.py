from Code.Individuals.Gun import *

class Player:
          def __init__(self, game):
                    self.game = game

                    self.game.methods.set_attributes(self, PLAYER)

                    self.pos = self.find_spawn_position()
                    self.game.methods.set_rect(self)

                    self.current_vel = 0
                    self.gun = Gun(self.game, WEAPONS["ak47"])
                    self.max_vel = self.vel
                    self.base_max_vel = self.max_vel
                    self.current_animation = 'idle'
                    self.facing = "right"
                    self.is_sprinting = False
                    self.dead = False
                    self.frame = 0
                    self.max_health = self.health
                    self.max_stamina = self.stamina
                    self.last_hit = - self.hit_cooldown
                    self.slow_timer = Timer(self.slow_cooldown, 0)
                    self.is_slowed = False
                    self.dx = self.dy = 0
                    self.cached_water_collision = False
                    self.water_check_timer = Timer(0.2, 0)
                    self.hit_count = None

          def update_position(self):
                    new_x = self.pos.x + self.dx * self.current_vel * self.game.dt
                    new_y = self.pos.y + self.dy * self.current_vel * self.game.dt

                    self.move_hor = self.move_vert = False
                    if self.offset[0] + self.res[0] / 2 < new_x < GAME_SIZE[0] - self.res[0] / 2 + self.offset[2]:
                              self.pos.x = new_x
                              self.rect.centerx = self.pos.x
                              self.move_hor = True
                    if self.offset[1] + self.res[1] / 2 < new_y < GAME_SIZE[1] - self.res[1] / 2 + self.offset[3]:
                              self.pos.y = new_y
                              self.rect.centery = self.pos.y
                              self.move_vert = True

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
                    self.dx = self.dy = 0
                    if self.game.keys[pygame.K_a]: self.dx -= 1
                    if self.game.keys[pygame.K_d]: self.dx += 1
                    if self.game.keys[pygame.K_s]: self.dy += 1
                    if self.game.keys[pygame.K_w]: self.dy -= 1

                    magnitude = math.hypot(self.dx, self.dy)
                    if magnitude != 0:
                              self.dx /= magnitude
                              self.dy /= magnitude

                    self.is_sprinting = self.game.keys[KEYS['sprint']] and (self.dx != 0 or self.dy != 0)
                    self.move_hor = self.move_vert = False
                    if not self.game.changing_settings or not self.game.died:
                              self.handle_stamina()
                              self.handle_slowdown()
                              self.update_frame()

                    self.update_velocity()
                    self.update_facing()

                    if not self.game.changing_settings and not self.game.died:
                              self.update_position()
                              self.game.grass_manager.apply_force(self.rect.midbottom, self.rect.width, self.grass_force)

                    self.game.camera.move(self.dx, self.dy, self.move_hor, self.move_vert)
                    self.update_animation()

                    self.gun.update()

          def draw(self, surface=None):
                    if surface is None:
                              surface = self.game.display_surface
                    current_animation = self.game.assets["player_" + self.current_animation + "_" + self.facing]
                    frame_index = int(self.frame) % len(current_animation)
                    image = current_animation[frame_index]

                    shadow_image = self.game.methods.get_shadow_image(self, image)
                    surface.blit(shadow_image, (self.get_position()[0], self.get_position()[1] + self.res[1] - shadow_image.height / 2))
                    if self.hit_count is not None:
                              image = self.game.methods.get_image_mask(image)
                              self.hit_count += MISC["hit_effect"][1] * self.game.dt
                              if self.hit_count >= MISC["hit_effect"][0]:
                                        self.hit_count = None
                    surface.blit(image, self.get_position())

                    self.gun.draw(surface)

          def get_position(self):
                    return self.rect.x - self.game.camera.offset_rect.x, self.rect.y - self.game.camera.offset_rect.y

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
                    if not self.game.died:
                              factor = self.max_vel / self.base_max_vel
                              self.frame += self.animation_speed * factor * self.game.dt

          def get_mid_position(self):
                    return self.rect.centerx - self.game.camera.offset_rect.x, self.rect.centery - self.game.camera.offset_rect.y

          def update_facing(self):
                    if not self.game.died:
                              if self.game.correct_mouse_pos[0] < self.get_mid_position()[0]:
                                        self.facing = "left"
                              else:
                                        self.facing = "right"

          def deal_damage(self, damage):
                    if self.game.game_time - self.last_hit > self.hit_cooldown:
                              self.health -= damage
                              self.check_if_alive()
                              self.last_hit = self.game.game_time
                              self.hit_count = 0

          def check_if_alive(self):
                    if self.health <= 0:
                              self.dead = True
                              self.health = 0

          def update_velocity(self):
                    if self.dx != 0 or self.dy != 0:
                              self.current_vel = min(self.current_vel + self.acceleration * self.game.dt, self.max_vel)
                    else:
                              self.current_vel = max(self.current_vel - self.acceleration * self.game.dt, 0)

          def should_be_slowed(self):
                    if self.water_check_timer.update(self.game.game_time):
                              self.cached_water_collision = self.game.tilemap_manager.tile_collision(
                                        pygame.Rect(self.pos.x, self.pos.y + self.res[1] / 2, 0, 0), "water_tile")
                              self.water_check_timer.reactivate(self.game.game_time)
                    return self.cached_water_collision

          def handle_slowdown(self):
                    if self.should_be_slowed():
                              if not self.is_slowed:
                                        self.is_slowed = True
                                        self.slow_timer.reactivate(self.game.game_time)
                              elif self.slow_timer.update(self.game.game_time):
                                        # Player has been slowed for more than the cooldown period
                                        self.max_vel = self.slowed_vel
                                        self.health -= GENERAL["damages"][0] * self.game.dt
                    else:
                              self.is_slowed = False
                              self.max_vel = self.sprint_vel if self.is_sprinting else self.vel
