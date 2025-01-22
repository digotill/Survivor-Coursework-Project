from Code.Individuals.Parent import *

class Enemy(main):
          def __init__(self, game, coordinates, dictionary):
                    self.game = game

                    self.set_attributes(dictionary)

                    self.pos = v2(coordinates)
                    self.set_rect()

                    self.acceleration = v2(0, 0)
                    self.vel_vector = v2(0, 0)
                    self.current_animation = 'moving'
                    self.is_attacking = False

          def apply_force(self, force):
                    self.vel_vector += force
                    if self.vel_vector.length() > self.vel:
                              self.vel_vector = self.vel_vector.normalize() * self.vel

          def update(self):
                    if self.should_move():
                              self.move()
                    self.update_is_attacking()
                    self.update_frame()
                    self.update_facing()
                    self.update_position()
                    self.attack_player()

          def should_move(self):
                    distance = self.distance_to_player()
                    return distance > self.stopping_range

          def attack_player(self):
                    if self.is_attacking:
                              if self.rect.colliderect(self.game.player.rect):
                                        self.game.player.deal_damage(self.damage)

          def move(self):
                    direction = self.game.player.rect.center - self.pos
                    if direction.length() > 0:
                              direction = direction.normalize()

                    desired_velocity = direction * self.max_vel
                    steering = (desired_velocity - self.vel_vector) * self.steering_strength
                    self.apply_force(steering)

                    self.vel_vector += self.acceleration * self.game.dt
                    if self.vel_vector.length() > self.max_vel:
                              self.vel_vector = self.vel_vector.normalize() * self.max_vel

                    self.vel_vector *= (1 - self.friction)

                    self.acceleration = v2(0, 0)

          def update_position(self):
                    self.pos += self.vel_vector * self.game.dt
                    self.rect.center = self.pos

          def update_facing(self):
                    self.facing = "right" if self.game.player.rect.centerx > self.pos.x else "left"

          def distance_to_player(self):
                    return (self.game.player.rect.center - self.pos).length()

          def update_is_attacking(self):
                    distance = self.distance_to_player()
                    if distance <= self.attack_range:
                              self.is_attacking = True
                    elif self.is_attacking and self.frame > len(self.game.assets[self.name + "_" + self.current_animation + "_" + self.facing]):
                              self.is_attacking = False
                    self.update_animation()

          def draw(self, surface=None):
                    if surface is None:
                              surface = self.game.display_surface
                    current_sprite = self.get_current_sprite()
                    shadow_image = self.generate_shadow_image(current_sprite)
                    self.game.display_surface.blit(shadow_image, (
                              self.get_position()[0],
                              self.get_position()[1] + self.res[1] - shadow_image.height / 2))
                    surface.blit(current_sprite, self.get_position())

          def get_current_sprite(self):
                    current_animation = self.game.assets[self.name + "_" + self.current_animation + "_" + self.facing]
                    frame_index = int(self.frame) % len(current_animation)
                    sprite = current_animation[frame_index]
                    return sprite

          def reset(self, coordinates, new_dictionary):
                    self.__init__(self.game, coordinates, new_dictionary)

          def change_animation(self, animation_name):
                    if self.current_animation != animation_name:
                              self.current_animation = animation_name
                              self.frame = 0

          def update_animation(self):
                    new_animation = 'moving' if not self.is_attacking else 'attacking'
                    self.change_animation(new_animation)