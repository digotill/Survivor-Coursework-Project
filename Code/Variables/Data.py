from Code.Utilities.SaveLoadSystem import *
import pygame


class Data:
          def __init__(self, game):
                    self.game = game
                    self.save_load_system = SaveLoadSystem(".save", "DataSave")
                    self.slider_configs = {
                              'fps': {'default': pygame.display.get_current_refresh_rate()},
                              'brightness': {'default': 50},
                              'shake': {'default': 100},
                              'colour': {'default': 50},
                              'volume': {'default': 50},
                              'text_size': {'default': 100}
                    }

          def load_data(self):
                    for slider_name, config in self.slider_configs.items():
                              value = self.save_load_system.load_game_data([slider_name], [config['default']])
                              self.game.interactablesM.sliders[slider_name].value = value
                    self.game.wins = self.save_load_system.load_game_data(["wins"], [0])

          def save_data(self):
                    for slider_name in self.slider_configs.keys():
                              value = self.game.interactablesM.sliders[slider_name].value
                              self.save_load_system.save_game_data([value], [slider_name])
                    self.save_load_system.save_game_data([self.game.wins], ["wins"])
