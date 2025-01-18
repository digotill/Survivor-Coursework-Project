import pygame


class DrawingManager:
          def __init__(self, game):
                    self.game = game
                    self.drawables = []

          def transparent_objects(self):
                    for thing in self.game.object_manager.grid.query(self.game.player.rect):
                              if thing.rect.colliderect(self.game.player.rect):
                                        dx = thing.rect.bottom - self.game.player.rect.bottom
                                        dy = thing.rect.bottom - self.game.player.rect.bottom
                                        squared_distance = dx * dx + dy * dy
                                        greatest_side = thing.image.get_height()
                                        alpha = max(100,
                                                    min(squared_distance / (greatest_side * greatest_side) * 255, 255))
                                        if self.game.player.rect.bottom > thing.rect.bottom: alpha = 255
                                        thing.image = thing.original_image.copy()
                                        thing.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
                              else:
                                        thing.image = thing.original_image.copy()

          def draw(self):
                    self.transparent_objects()
                    for obg in self.game.object_manager.grid.window_query():
                              self.game.drawing_manager.drawables.append(obg)

                    for enemy in self.game.enemy_manager.grid.window_query():
                              self.game.drawing_manager.drawables.append(enemy)

                    self.game.drawing_manager.drawables.append(self.game.player)

                    self.drawables.sort(key=lambda obj: obj.rect.bottom)
                    for drawable in self.drawables:
                              drawable.draw()
                    self.drawables = []