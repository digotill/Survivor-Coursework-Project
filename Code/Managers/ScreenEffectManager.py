from Code.Variables.SettingsVariables import *
from Code.Individuals.ScreenEffect import *

class ScreenEffectManager:
          def __init__(self, game):
                    self.game = game
                    self.transition_screeneffect = ScreenEffect(self.game, self.game.assets["transition_screeneffect"], General_Settings['animation_speeds'][1])

          def draw(self):
                    if self.game.playing_transition:
                              if self.transition_screeneffect.draw():
                                        self.game.in_menu = False