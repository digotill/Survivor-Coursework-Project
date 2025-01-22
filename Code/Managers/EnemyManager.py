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
                                        separation_force = self.calculate_separation(enemy)
                                        enemy.apply_force(separation_force)

                              self.remove_dead_enemies()  # Remove enemies with no health

                              if self.spawn_timer.update(self.game.game_time):
                                        self.add_enemies("enemy1")  # Spawn new enemies if conditions are met
                                        self.spawn_timer.reactivate(self.game.game_time)

                              self.grid.rebuild()  # Rebuild the spatial hash grid

          def add_enemies(self, enemy_type):
                    # Check if it's time to spawn a new enemy and if the max enemy limit hasn't been reached
                    if len(self.grid.items) < General_Settings["enemies"][0] and not General_Settings["peaceful_mode"]:

                              # Generate random coordinates for the new enemy
                              coordinates = random_xy(
                                        pygame.Rect(0, 0, GAME_SIZE[0], GAME_SIZE[1]),
                                        self.game.camera.rect, AM.assets[enemy_type][0].width, AM.assets[enemy_type][0].height
                              )

                              # Reuse an enemy from the pool if available, otherwise create a new one
                              if self.enemy_pool:
                                        enemy = self.enemy_pool.pop()
                                        enemy.reset(coordinates, Enemies[enemy_type])
                              else:
                                        enemy = Enemy(self.game, coordinates, Enemies[enemy_type])

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
                    # Calculate separation force to prevent enemies from clustering too closely
                    steering = v2(0, 0)
                    total = 0
                    nearby_enemies = self.grid.query(
                              enemy.rect.inflate(enemy.separation_radius * 2, enemy.separation_radius * 2))

                    for other in nearby_enemies:
                              if other != enemy:
                                        distance = enemy.pos.distance_to(other.pos)
                                        if distance < enemy.separation_radius:
                                                  diff = (enemy.pos - other.pos).normalize() / distance
                                                  steering += diff
                                                  total += 1

                    if total > 0:
                              steering = (steering / total).normalize() * enemy.vel - enemy.vel_vector
                              if steering.length() > enemy.vel:
                                        steering = steering.normalize() * enemy.vel

                    return steering * enemy.separation_strength
