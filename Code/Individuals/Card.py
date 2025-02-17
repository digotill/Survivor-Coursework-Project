from Code.Variables.SettingVariables import *

class Card:
          def __init__(self, game, type):
                    self.game = game
                    images = self.game.assets[type + "_cards"]
                    self.card_number = random.randint(0, len(images) - 1)
                    self.image = images[self.card_number]