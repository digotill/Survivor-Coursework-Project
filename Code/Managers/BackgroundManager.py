from Code.Individuals.Background import *

class BackgroundManager:
          def __init__(self, game):
                    self.game = game
                    self.main_background = Background(self.game, AM.assets['main_menu'], General_Settings['animation_speeds'][0])

          def draw(self):
                    if self.game.in_menu:
                              self.main_background.draw()