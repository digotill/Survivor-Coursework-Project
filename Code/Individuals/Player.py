from Code.Individuals.Gun import *


class Player:
          def __init__(self, game):
                    self.game = game

                    # Set player attributes from PLAYER settings
                    self.game.methods.set_attributes(self, PLAYER)

                    # Find a suitable spawn position and set up the player's rectangle
                    self.pos = self.find_spawn_position()
                    self.game.methods.set_rect(self)

                    # Initialize player state variables
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
                    self.water_collision = False
                    self.water_check_timer = Timer(0.2, 0)
                    self.hit_count = None

                    self.xp = 0
                    self.level = 1
                    self.calculate_max_xp()

          def update_position(self):
                    # Calculate new position based on velocity and delta time
                    new_x = self.pos.x + self.dx * self.current_vel * self.game.dt
                    new_y = self.pos.y + self.dy * self.current_vel * self.game.dt

                    # Check if new position is within game boundaries and update accordingly
                    self.move_hor = self.move_vert = False
                    if self.offset[0] + self.res[0] / 2 < new_x < GAMESIZE[0] - self.res[0] / 2 + self.offset[2]:
                              self.pos.x = new_x
                              self.rect.centerx = self.pos.x
                    if self.offset[1] + self.res[1] / 2 < new_y < GAMESIZE[1] - self.res[1] / 2 + self.offset[3]:
                              self.pos.y = new_y
                              self.rect.centery = self.pos.y

          def calculate_max_xp(self):
                    base_xp = XP["starting_max_xp"]
                    growth_factor = XP["xp_progression_rate"]
                    self.max_xp = int(base_xp * (growth_factor ** (self.level - 1)))

          def find_spawn_position(self):
                    # Find a suitable spawn position that's not on a water tile
                    center_x, center_y = GAMESIZE[0] // 2, GAMESIZE[1] // 2
                    max_distance = max(GAMESIZE[0], GAMESIZE[1])

                    for distance in range(0, max_distance, 16):
                              for angle in range(0, 360, 10):
                                        x = center_x + int(distance * math.cos(math.radians(angle)))
                                        y = center_y + int(distance * math.sin(math.radians(angle)))

                                        if 0 <= x < GAMESIZE[0] and 0 <= y < GAMESIZE[1]:
                                                  test_rect = pygame.Rect(x, y, self.res[0], self.res[1])
                                                  if not self.game.tilemapM.tile_collision(test_rect, "water_tile"):
                                                            return v2(x, y)

          def change_animation(self, animation_name):
                    # Change the current animation if it's different from the new one
                    if self.current_animation != animation_name:
                              self.current_animation = animation_name
                              self.frame = 0

          def update_animation(self):
                    # Update the animation based on player movement
                    new_animation = 'running' if (self.game.inputM.get("move_left") or self.game.inputM.get("move_right") or
                                                  self.game.inputM.get("move_down") or self.game.inputM.get("move_up")) and not self.game.changing_settings else 'idle'
                    self.change_animation(new_animation)

          def update(self):
                    # Reset movement direction
                    self.dx = self.dy = 0

                    # Check for movement input
                    if self.game.inputM.get("move_left"): self.dx -= 1
                    if self.game.inputM.get("move_right"): self.dx += 1
                    if self.game.inputM.get("move_down"): self.dy += 1
                    if self.game.inputM.get("move_up"): self.dy -= 1

                    # Normalize diagonal movement
                    magnitude = math.hypot(self.dx, self.dy)
                    if magnitude != 0:
                              self.dx /= magnitude
                              self.dy /= magnitude

                    # Update player state if game is not paused or player hasn't died
                    if not self.game.changing_settings or not self.game.died:
                              self.handle_slowdown()
                              self.update_frame()
                              self.update_velocity()
                              self.update_facing()
                              self.game.grassM.apply_force(self.rect.midbottom, self.rect.width, self.grass_force)

                    # Update position and apply grass force if game is not paused and player is alive
                    if not self.game.changing_settings and not self.game.died:
                              self.handle_stamina()
                              self.update_position()

                    self.update_animation()
                    self.xp += 0.2

                    # Update gun
                    self.gun.update()
                    self.manage_xp()

          def manage_xp(self):
                    if self.xp >= self.max_xp:
                              self.level += 1
                              self.calculate_max_xp()
                              self.xp = 0
                    else:
                              self.calculate_max_xp()

          def draw(self, surface=None):
                    # Draw the player on the given surface (or game display if none provided)
                    if surface is None:
                              surface = self.game.displayS

                    # Get the current animation frame
                    current_animation = self.game.assets["player_" + self.current_animation + "_" + self.facing]
                    frame_index = int(self.frame) % len(current_animation)
                    image = current_animation[frame_index]

                    # Draw player shadow
                    shadow_image = self.game.methods.get_shadow_image(self, image)
                    surface.blit(shadow_image, (self.get_position()[0], self.get_position()[1] + self.res[1] - shadow_image.height / 2))

                    # Apply hit effect if player was recently hit
                    if self.hit_count is not None:
                              image = self.game.methods.get_image_mask(image)
                              self.hit_count += MISC["hit_effect"][1] * self.game.dt
                              if self.hit_count >= MISC["hit_effect"][0]:
                                        self.hit_count = None

                    # Draw player
                    surface.blit(image, self.get_position())

                    # Draw gun
                    self.gun.draw(surface)

          def handle_stamina(self):
                    self.is_sprinting = self.game.inputM.get("sprint") and (self.dx != 0 or self.dy != 0) and not self.game.changing_settings
                    # Decrease stamina while sprinting, increase while not sprinting
                    if self.is_sprinting and self.current_vel > 0:
                              self.stamina -= self.stamina_consumption * self.game.dt
                              self.stamina = max(0, self.stamina)
                    else:
                              self.stamina += self.stamina_recharge_rate * self.game.dt
                              self.stamina = min(self.max_stamina, self.stamina)

                    # Disable sprinting if stamina is depleted
                    if self.stamina <= 0:
                              self.is_sprinting = False

          def update_frame(self):
                    # Update animation frame based on velocity
                    if not self.game.died:
                              factor = self.max_vel / self.base_max_vel
                              self.frame += self.animation_speed * factor * self.game.dt

          def get_position(self):
                    # Get player's position relative to the camera
                    return self.rect.x - self.game.cameraM.rect.x, self.rect.y - self.game.cameraM.rect.y

          def get_mid_position(self):
                    # Get player's center position relative to the camera
                    return self.rect.centerx - self.game.cameraM.rect.x, self.rect.centery - self.game.cameraM.rect.y

          def update_facing(self):
                    # Update player's facing direction based on mouse position
                    if not self.game.died:
                              if self.game.correct_mouse_pos[0] < self.get_mid_position()[0]:
                                        self.facing = "left"
                              else:
                                        self.facing = "right"

          def deal_damage(self, damage):
                    # Apply damage to player if not in hit cooldown
                    if self.game.game_time - self.last_hit > self.hit_cooldown:
                              self.health -= damage
                              self.check_if_alive()
                              self.last_hit = self.game.game_time
                              self.hit_count = 0

                              self.game.cameraM.add_screen_shake(SHAKE["hit"][1], SHAKE["hit"][0] * self.game.reduced_screen_shake)

          def check_if_alive(self):
                    # Check if player's health has depleted
                    if self.health <= 0:
                              self.dead = True
                              self.health = 0

          def update_velocity(self):
                    # Update player's velocity based on movement and acceleration
                    if self.dx != 0 or self.dy != 0:
                              self.current_vel = min(self.current_vel + self.acceleration * self.game.dt, self.max_vel)
                    else:
                              self.current_vel = max(self.current_vel - self.acceleration * self.game.dt, 0)

          def should_be_slowed(self):
                    # Check if player is in contact with water tiles
                    if self.water_check_timer.update(self.game.game_time):
                              self.water_collision = self.game.tilemapM.tile_collision(
                                        pygame.Rect(self.pos.x, self.pos.y + self.res[1] / 2, 0, 0), "water_tile")
                              self.water_check_timer.reactivate(self.game.game_time)
                    return self.water_collision

          def handle_slowdown(self):
                    # Apply slowdown effect and damage when in water
                    if self.should_be_slowed():
                              if not self.is_slowed:
                                        self.is_slowed = True
                                        self.slow_timer.reactivate(self.game.game_time)
                              elif self.slow_timer.update(self.game.game_time):
                                        # Player has been slowed for more than the cooldown period
                                        self.max_vel = self.slowed_vel
                                        self.health -= MISC["acid_damage"] * self.game.dt
                    else:
                              self.is_slowed = False
                              self.max_vel = self.sprint_vel if self.is_sprinting else self.vel
