from Code.Individuals.Enemy import *
from Code.DataStructures.HashMap import *


class EnemyManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, GENERAL["hash_maps"][0])  # Spatial hash grid for efficient enemy management
                    self.enemy_pool = set()  # Pool of inactive enemies for reuse
                    self.spawn_timer = Timer(GENERAL["enemies"][1], self.game.game_time)  # Timer for enemy spawning
                    self.enemy_multiplier = 1  # Multiplier for enemy attributes (e.g., health, damage)

          def update(self):
                    if not self.game.changing_settings:
                              for enemy in self.grid.items:
                                        enemy.update()  # Update each enemy's state
                                        if random.random() < 0.05:  # 5% chance to apply separation force
                                                  separation_force = self.calculate_separation(enemy)
                                                  enemy.apply_force(separation_force)  # Apply separation to avoid crowding

                              self.remove_dead_enemies()  # Clean up dead enemies

                              if self.spawn_timer.update(self.game.game_time):
                                        self.add_enemies("mantis")  # Spawn new enemies if timer is up
                                        self.spawn_timer.reactivate(self.game.game_time)

                              if random.random() < 0.1:  # 10% chance to rebuild grid
                                        self.grid.rebuild()  # Periodically rebuild spatial hash grid

          def add_enemies(self, enemy_type):
                    if len(self.grid.items) < GENERAL["enemies"][0] and GENERAL["enemies"][2]:  # Check enemy limit and spawn flag
                              if self.enemy_pool:
                                        enemy = self.enemy_pool.pop()  # Reuse enemy from pool if available
                                        enemy.reset(ENEMIES[enemy_type])
                              else:
                                        enemy = Enemy(self.game, ENEMIES[enemy_type])  # Create new enemy if pool is empty

                              self.grid.insert(enemy)  # Add enemy to spatial hash grid

          def remove_dead_enemies(self):
                    for enemy in self.grid.items.copy():
                              if enemy.health <= 0:
                                        enemy.dead = True
                              if enemy.dead:
                                        self.grid.items.remove(enemy)  # Remove dead enemy from grid
                                        self.enemy_pool.add(enemy)  # Add dead enemy back to pool for reuse

          def calculate_separation(self, enemy):
                    steering = v2(0, 0)
                    total = 0
                    nearby_enemies = self.grid.query(
                              enemy.rect.inflate(enemy.separation_radius * 2, enemy.separation_radius * 2))  # Query nearby enemies

                    enemy_pos = enemy.pos
                    separation_radius_sq = enemy.separation_radius ** 2

                    for other in nearby_enemies:
                              if other is not enemy:
                                        dx = enemy_pos.x - other.pos.x
                                        dy = enemy_pos.y - other.pos.y
                                        distance_sq = dx * dx + dy * dy

                                        if distance_sq < separation_radius_sq:
                                                  inv_dist = 1.0 / (distance_sq ** 0.5 + 1e-6)  # Inverse distance (avoid division by zero)
                                                  steering.x += dx * inv_dist
                                                  steering.y += dy * inv_dist
                                                  total += 1

                    if total > 0:
                              steering.x /= total
                              steering.y /= total

                              length = (steering.x ** 2 + steering.y ** 2) ** 0.5
                              if length > 0:
                                        inv_length = 1.0 / length
                                        steering.x *= inv_length * enemy.vel  # Normalize and scale by enemy velocity
                                        steering.y *= inv_length * enemy.vel

                              rel_vel_x = steering.x - enemy.vel_vector.x
                              rel_vel_y = steering.y - enemy.vel_vector.y
                              rel_vel_length_sq = rel_vel_x ** 2 + rel_vel_y ** 2

                              if rel_vel_length_sq > enemy.vel ** 2:
                                        inv_rel_vel_length = enemy.vel / (rel_vel_length_sq ** 0.5)
                                        steering.x = rel_vel_x * inv_rel_vel_length  # Limit steering force
                                        steering.y = rel_vel_y * inv_rel_vel_length

                    return steering * enemy.separation_strength  # Return final separation force
