from Code.DataStructures.HashMap import *
from Code.Individuals.Spark import *


class SparkManager:
          def __init__(self, game):
                    self.game = game
                    # Initialize spatial hash grid for efficient spark management
                    self.grid = HashMap(game, GENERAL["hash_maps"][5])
                    # Create a pool of spark objects for reuse
                    self.spark_pool = set()

          def update(self):
                    if not self.game.changing_settings:
                              # Update position of all active sparks
                              for spark in self.grid.items:
                                        spark.move()
                              # Remove dead sparks and return them to the pool
                              self.check_if_remove()
                              # Rebuild the spatial hash grid after updates
                              self.grid.rebuild()

          def create_spark(self, angle, pos, dictionary):
                    # Create multiple sparks based on the specified amount
                    for _ in range(dictionary['amount']):
                              # Calculate a random angle within the spread range
                              spark_angle = math.radians(random.randint(
                                        int(angle) - dictionary['spread'],
                                        int(angle) + dictionary['spread']
                              ))
                              # Generate a random velocity for the spark
                              spark_velocity = random.randint(dictionary["min_vel"], dictionary["max_vel"])

                              if len(self.spark_pool) == 0:
                                        # If no sparks are available in the pool, create a new one
                                        self.grid.insert(
                                                  Spark(self.game, pos, spark_angle, spark_velocity,
                                                        dictionary['colour'], dictionary['scale'])
                                        )
                              else:
                                        # Reuse a spark from the pool
                                        spark = self.spark_pool.pop()
                                        spark.reset(pos, spark_angle, spark_velocity, dictionary["colour"],
                                                    dictionary['scale'])
                                        self.grid.insert(spark)

          def check_if_remove(self):
                    # Check for dead sparks, remove them from the grid, and add to the pool
                    for spark in self.grid.items.copy():
                              if not spark.alive:
                                        self.grid.items.remove(spark)
                                        self.spark_pool.add(spark)
