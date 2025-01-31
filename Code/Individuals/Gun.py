from Code.Variables.SettingVariables import *


class Gun:
          def __init__(self, game, dictionary):
                    self.game = game  # Reference to the main game object

                    self.game.methods.set_attributes(self, dictionary)  # Set gun attributes from dictionary

                    self.gun_image = self.game.assets[self.name]  # Load gun image
                    self.res = self.game.assets[self.name].size  # Get gun image resolution
                    self.bullet_image = self.game.assets[self.name + "_bullet"]  # Load bullet image

                    self.pos = v2(0, 0)  # Initialize gun position
                    self.rect = pygame.Rect(0, 0, self.res[0], self.res[1])  # Create gun rectangle
                    self.noise_map = PerlinNoise(MAP["gun_shake_map"][1],  # Create Perlin noise for gun shake
                                                 random.randint(0, 100000))

                    self.last_shot = - self.fire_rate  # Initialize last shot time
                    self.initial_vel = self.vel  # Store initial velocity
                    self.continuous_fire_start = 0  # Track continuous fire start time

          def update(self):
                    self.calc_angle()  # Calculate gun angle
                    self.update_shooting()  # Update shooting mechanics

          def draw(self, surface):
                    if not self.game.died:  # Only draw if player is alive
                              if self.game.player.facing == "right":
                                        self.rotated_image = pygame.transform.rotate(  # Rotate gun image for right-facing
                                                  self.gun_image, self.angle + 90)
                              else:
                                        self.rotated_image = pygame.transform.flip(  # Flip and rotate for left-facing
                                                  pygame.transform.rotate(self.gun_image, -self.angle + 90), True, False)

                              pos_x = (self.game.player.rect.centerx +  # Calculate gun x position
                                       math.sin(math.radians(self.angle)) * self.distance -
                                       self.game.cameraM.offset_rect.x)
                              pos_y = (self.game.player.rect.centery +  # Calculate gun y position
                                       math.cos(math.radians(self.angle)) * self.distance -
                                       self.game.cameraM.offset_rect.y)
                              self.rect = self.rotated_image.get_rect(center=(pos_x, pos_y))  # Update gun rectangle
                              surface.blit(self.rotated_image, self.rect)  # Draw gun on surface

          def calc_angle(self):
                    # Calculate x difference to mouse
                    change_in_x = self.game.player.rect.centerx - self.game.cameraM.offset_rect.x - self.game.correct_mouse_pos[0]
                    # Calculate y difference to mouse
                    change_in_y = self.game.player.rect.centery - self.game.cameraM.offset_rect.y - self.game.correct_mouse_pos[1]
                    self.angle = v2(change_in_x, change_in_y).angle_to((0, 1))  # Calculate angle to mouse

          def update_shooting(self):
                    current_time = self.game.game_time  # Get current game time
                    if self.can_shoot(current_time):  # Check if gun can shoot
                              self.shoot(current_time)  # Perform shooting
                    elif not self.game.mouse_state[0]:  # If mouse button released
                              self.continuous_fire_start = None  # Reset continuous fire

          def can_shoot(self, current_time):
                    return (self.fire_rate + self.last_shot < current_time and  # Check cooldown
                            self.game.mouse_state[0] and  # Check mouse pressed
                            not self.game.changing_settings and  # Check not in settings
                            not self.game.died)  # Check player alive

          def shoot(self, current_time):
                    if self.continuous_fire_start is None:  # If starting to fire
                              self.continuous_fire_start = current_time  # Set continuous fire start time

                    firing_duration = current_time - self.continuous_fire_start  # Calculate firing duration
                    max_spread_time = self.spread_time  # Get max spread time
                    spread_factor = min(firing_duration / max_spread_time, 1.0)  # Calculate spread factor

                    self.last_shot = current_time  # Update last shot time

                    start_coordinates = self.calculate_bullet_start_position()  # Get bullet start position
                    for _ in range(self.shots):  # For each shot
                              self.game.sparkM.create_spark(  # Create muzzle flash
                                        270 - self.angle, start_coordinates,
                                        SPARKS['muzzle_flash'])
                              if self.shots == 1:  # If single shot
                                        self.game.bulletM.add_bullet(  # Add bullet without spread
                                                  start_coordinates, self.angle,
                                                  "Player Bullet", spread_factor)
                              else:  # If multiple shots
                                        self.game.bulletM.add_bullet(  # Add bullet with spread
                                                  start_coordinates,
                                                  self.game.methods.change(self.angle, self.spread),
                                                  "Player Bullet", spread_factor)

          def calculate_bullet_start_position(self):
                    start_x = self.game.player.rect.centerx + math.sin(math.radians(self.angle)) * int(
                              self.distance - self.res[0])  # Calculate bullet start x
                    start_y = self.game.player.rect.centery + math.cos(math.radians(self.angle)) * int(
                              self.distance - self.res[0])  # Calculate bullet start y
                    return start_x, start_y  # Return start coordinates
