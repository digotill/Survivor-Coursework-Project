from Code.Variables.SettingsVariables import *
from Code.Individuals.ScreenEffect import *

class ScreenEffectManager:
          def __init__(self, game):
                    self.game = game
                    self.transition_screeneffect = ScreenEffect(self.game, self.game.assets["transition_screeneffect"], General_Settings['animation_speeds'][1])
                    self.youdied_screeneffect = ScreenEffect(self.game, self.game.assets["youdied_screeneffect"], General_Settings['animation_speeds'][2])
                    self.inverted_transition = False
                    self.youdied_start_time = None
                    self.youdied_duration = 3

          def draw(self):
                    if self.game.playing_transition and self.game.in_menu:
                              if self.transition_screeneffect.draw():
                                        self.game.in_menu = False
                    elif not self.game.in_menu and self.game.game_time < General_Settings["screen_effect"][0]:
                              self.transition_screeneffect.draw()
                    elif not self.game.in_menu and self.game.game_time >= General_Settings["screen_effect"][0]:
                              if not self.inverted_transition:
                                        self.transition_screeneffect.frame = self.transition_screeneffect.length
                                        self.inverted_transition = True
                              self.transition_screeneffect.draw(-1)

                    if self.game.died:
                              if self.youdied_start_time is None:
                                        self.youdied_start_time = self.game.game_time
                              self.youdied_screeneffect.alpha = (max(min(0.8, (self.game.game_time - self.youdied_start_time) / self.youdied_duration), 0.2)) * 255
                              self.youdied_screeneffect.draw()

