from Code.Individuals.Enemy import *
from Code.DataStructures.Grid import *


class EnemyManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, General_Settings["hash_maps"][0])  # Spatial hash grid for efficient enemy management
                    self.enemy_pool = set()  # Pool of inactive enemies for reuse
                    self.spawn_timer = Timer(General_Settings["enemies"][1], self.game.game_time)
                    self.enemy_multiplier = 1  # Multiplier for enemy attributes (e.g., health, damage)

          def update(self):
                    if not self.game.changing_settings:
                              # Update all enemies and apply separation forces
                              for enemy in self.grid.items:
                                        enemy.update()
                                        if random.random() < 0.005:
                                                  separation_force = self.calculate_separation(enemy)
                                                  enemy.apply_force(separation_force)

                              self.remove_dead_enemies()  # Remove enemies with no health

                              if self.spawn_timer.update(self.game.game_time):
                                        self.add_enemies("enemy1")  # Spawn new enemies if conditions are met
                                        self.spawn_timer.reactivate(self.game.game_time)

                              if random.random() > 0.9:
                                        self.grid.rebuild()  # Rebuild the spatial hash grid

          @staticmethod
          def random_xy(rect1, rect2, sprite_width, sprite_height):
                    while True:
                              x = random.randint(rect1.left, rect1.right - sprite_width)
                              y = random.randint(rect1.top, rect1.bottom - sprite_height)
                              if not rect2.collidepoint(x, y): return x, y

          def add_enemies(self, enemy_type):
                    # Check if it's time to spawn a new enemy and if the max enemy limit hasn't been reached
                    if len(self.grid.items) < General_Settings["enemies"][0] and not General_Settings["peaceful_mode"]:

                              # Generate random coordinates for the new enemy
                              coordinates = self.random_xy(
                                        pygame.Rect(0, 0, GAME_SIZE[0], GAME_SIZE[1]),
                                        self.game.camera.rect, AM.assets[enemy_type][0].width, AM.assets[enemy_type][0].height
                              )

                              # Reuse an enemy from the pool if available, otherwise create a new one
                              if self.enemy_pool:
                                        enemy = self.enemy_pool.pop()
                                        enemy.reset(coordinates, ENEMIES[enemy_type])
                              else:
                                        enemy = Enemy(self.game, coordinates, ENEMIES[enemy_type])

                              self.grid.insert(enemy)  # Add the enemy to the spatial hash grid

          def remove_dead_enemies(self):
                    # Remove enemies with no health and add them back to the pool
                    for enemy in self.grid.items.copy():
                              if enemy.health <= 0:
                                        enemy.dead = True
                              if enemy.dead:
                                        self.grid.items.remove(enemy)
                                        self.enemy_pool.add(enemy)

          def calculate_separation(self, enemy):
                    steering = v2(0, 0)
                    total = 0
                    nearby_enemies = self.grid.query(
                              enemy.rect.inflate(enemy.separation_radius * 2, enemy.separation_radius * 2))

                    enemy_pos = enemy.pos
                    separation_radius_sq = enemy.separation_radius ** 2

                    for other in nearby_enemies:
                              if other is not enemy:
                                        dx = enemy_pos.x - other.pos.x
                                        dy = enemy_pos.y - other.pos.y
                                        distance_sq = dx * dx + dy * dy

                                        if distance_sq < separation_radius_sq:
                                                  inv_dist = 1.0 / (distance_sq ** 0.5 + 1e-6)  # Add small epsilon to avoid division by zero
                                                  steering.x += dx * inv_dist
                                                  steering.y += dy * inv_dist
                                                  total += 1

                    if total > 0:
                              steering.x /= total
                              steering.y /= total

                              length = (steering.x ** 2 + steering.y ** 2) ** 0.5
                              if length > 0:
                                        inv_length = 1.0 / length
                                        steering.x *= inv_length * enemy.vel
                                        steering.y *= inv_length * enemy.vel

                              rel_vel_x = steering.x - enemy.vel_vector.x
                              rel_vel_y = steering.y - enemy.vel_vector.y
                              rel_vel_length_sq = rel_vel_x ** 2 + rel_vel_y ** 2

                              if rel_vel_length_sq > enemy.vel ** 2:
                                        inv_rel_vel_length = enemy.vel / (rel_vel_length_sq ** 0.5)
                                        steering.x = rel_vel_x * inv_rel_vel_length
                                        steering.y = rel_vel_y * inv_rel_vel_length

                    return steering * enemy.separation_strength


