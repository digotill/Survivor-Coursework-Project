from Code.Variables.SettingsVariables import *


class EffectManager:
          def __init__(self, game):
                    self.game = game
                    self.effects = []
                    self.effect_types = {}
                    self.spawn_timers = {}

          def update(self):
                    for effect in self.effects:
                              effect.update()
