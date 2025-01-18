class GameOver:
          def __init__(self, game):
                    self.game = game

          def update(self):
                    if self.game.player.pierce < 0: self.running = False

          def loop(self):
                    pass