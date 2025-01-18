from Code.Individuals.Parent import *

class Enemy(main):
          def __init__(self, game, coordinates, dictionary):
                    self.game = game

                    self.set_attributes(dictionary)

                    self.images = AM.assets[self.name]
                    self.res = AM.assets[self.name][0].size

                    self.pos = v2(coordinates)
                    self.set_rect()

                    self.acceleration = v2(0, 0)
                    self.vel_vector = v2(0, 0)

          def apply_force(self, force):
                    self.vel_vector += force
                    if self.vel_vector.length() > self.vel:
                              self.vel_vector = self.vel_vector.normalize() * self.vel

          def update(self):
                    if self.should_move():
                              self.move()
                    self.update_frame()
                    self.update_facing()
                    self.update_position()

          def should_move(self):
                    distance = self.distance_to_player()
                    return distance > self.stopping_distance

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

          def draw(self):
                    current_sprite = self.get_current_sprite()
                    shadow_image = self.generate_shadow_image(current_sprite)
                    self.game.display_screen.blit(shadow_image, (
                              self.get_position()[0],
                              self.get_position()[1] + self.res[1] - shadow_image.height / 2))
                    self.game.display_screen.blit(current_sprite, self.get_position())

          def get_current_sprite(self):
                    sprite = self.images[int(self.frame) % len(self.images)]
                    if self.facing == "left":
                              sprite = pygame.transform.flip(sprite, True, False)
                    return sprite

          def reset(self, coordinates, new_dictionary):
                    self.__init__(self.game, coordinates, new_dictionary)