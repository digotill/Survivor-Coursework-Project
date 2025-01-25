from Code.Variables.SettingsVariables import *

class Enemy:
          def __init__(self, game, dictionary):
                    self.game = game

                    self.game.methods.set_attributes(self, dictionary)

                    self.set_coordinates()
                    self.game.methods.set_rect(self)

                    self.acceleration = v2(0, 0)
                    self.vel_vector = v2(0, 0)
                    self.max_vel = self.vel
                    self.current_animation = 'moving'
                    self.is_attacking = False
                    self.hit_count = None
                    self.dead = False
                    self.creation_time = self.game.game_time
                    self.last_hit = - self.hit_cooldown
                    self.facing = "right"
                    self.frame = 0

          def apply_force(self, force):
                    self.vel_vector += force
                    if self.vel_vector.length() > self.vel: self.vel_vector = self.vel_vector.normalize() * self.vel

          def set_coordinates(self):
                    s = MISC["enemy_spawns"]
                    rect2 = self.game.camera.offset_rect
                    rect1 = pygame.Rect(rect2.left - s, rect2.top - s, rect2.width + 2 * s, rect2.height + 2 * s )
                    while True:
                              x = random.randint(rect1.left, rect1.right - self.res[0])
                              y = random.randint(rect1.top, rect1.bottom - self.res[1])
                              if not self.game.camera.offset_rect.collidepoint(x, y):
                                        self.pos = v2(x, y)
                                        break

          def update(self):
                    if random.random() < General_Settings["update_fraction"][1]: self.full_update()
                    else: self.partial_update()

          def full_update(self):
                    if self.should_move(): self.move()
                    self.update_is_attacking()
                    self.update_frame()
                    self.update_facing()
                    self.update_position()
                    self.attack_player()

          def partial_update(self):
                    if self.should_move(): self.update_position()
                    self.update_frame()

          def update_frame(self):
                    self.frame += self.animation_speed * self.game.dt

          def should_move(self):
                    return (self.game.player.rect.center - self.pos).length_squared() > self.stopping_range

          def attack_player(self):
                    if self.is_attacking and self.rect.colliderect(self.game.player.rect): self.game.player.deal_damage(self.damage)

          def move(self):
                    direction = self.game.player.rect.center - self.pos
                    if direction.length_squared() > 0: direction = direction.normalize()

                    desired_velocity = direction * self.max_vel
                    steering = (desired_velocity - self.vel_vector) * self.steering_strength
                    self.apply_force(steering)

                    self.vel_vector += self.acceleration * self.game.dt
                    if self.vel_vector.length_squared() > self.max_vel ** 2: self.vel_vector = self.vel_vector.normalize() * self.max_vel

                    self.vel_vector *= (1 - self.friction)
                    self.acceleration.update(0, 0)

          def update_position(self):
                    self.pos += self.vel_vector * self.game.dt
                    self.rect.center = (int(self.pos.x), int(self.pos.y))

          def update_facing(self):
                    self.facing = "right" if self.game.player.rect.centerx > self.pos.x else "left"

          def distance_to_player(self):
                    return (self.game.player.rect.center - self.pos).length()

          def update_is_attacking(self):
                    distance_squared = (self.game.player.rect.center - self.pos).length_squared()
                    if distance_squared <= self.attack_range ** 2: self.is_attacking = True
                    elif self.is_attacking and self.frame > len(self.game.assets[f"{self.name}_{self.current_animation}_{self.facing}"]): self.is_attacking = False
                    self.update_animation()

          def get_position(self):
                    return self.rect.x - self.game.camera.offset_rect.x, self.rect.y - self.game.camera.offset_rect.y

          def draw(self, surface=None):
                    if surface is None: surface = self.game.display_surface
                    pos = self.get_position()
                    current_sprite = self.get_current_sprite()
                    shadow_image = self.game.methods.get_shadow_image(self, current_sprite)
                    self.game.display_surface.blit(shadow_image, (pos[0], pos[1] + self.res[1] - shadow_image.height / 2))
                    if self.hit_count is not None:
                              current_sprite = self.game.methods.get_image_mask(current_sprite)
                              self.hit_count += MISC["hit_effect"][1] * self.game.dt
                              if self.hit_count >= MISC["hit_effect"][0]:  self.hit_count = None
                    surface.blit(current_sprite, pos)

          def get_current_sprite(self):
                    current_animation = self.game.assets[self.name + "_" + self.current_animation + "_" + self.facing]
                    frame_index = int(self.frame) % len(current_animation)
                    sprite = current_animation[frame_index]
                    return sprite

          def reset(self, new_dictionary):
                    self.__init__(self.game, new_dictionary)

          def change_animation(self, animation_name):
                    if self.current_animation != animation_name:
                              self.current_animation = animation_name
                              self.frame = 0

          def update_animation(self):
                    new_animation = 'attacking' if self.is_attacking else 'moving'
                    if self.current_animation != new_animation:
                              self.current_animation = new_animation
                              self.frame = 0