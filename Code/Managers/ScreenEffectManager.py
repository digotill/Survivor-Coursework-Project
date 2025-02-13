from Code.Variables.SettingVariables import *
from Code.Individuals.ScreenEffect import ScreenEffect


class ScreenEffectManager:
          def __init__(self, game):
                    self.game = game
                    self._initialize_screen_effects()
                    self._initialize_flags()

          def _initialize_screen_effects(self):
                    self.transition_effect = ScreenEffect(self.game, self.game.assets["transition_screeneffect"], GENERAL['animation_speeds'][1])
                    self.youdied_effect = ScreenEffect(self.game, self.game.assets["youdied_screeneffect"], GENERAL['animation_speeds'][2])
                    self.blood_effect = ScreenEffect(self.game, self.game.assets["blood_screeneffect"], GENERAL['animation_speeds'][3])

          def _initialize_flags(self):
                    self.inverted_transition = False
                    self.youdied_start_time = None
                    self.youdied_duration = MISC["youdied_duration"]
                    self.draw_restart_transition = False
                    self.drawing_restart_transition = False
                    self.play_start_transition = False
                    self.has_blood_effect = False
                    self.blood_effect_start_time = None

          def set_transition_to_play(self):
                    self.play_start_transition = True
                    self.transition_effect.frame = self.transition_effect.length

          def add_blood_effect(self):
                    if not self.has_blood_effect:
                              self.has_blood_effect = True
                              self.blood_effect_start_time = self.game.game_time

          def draw(self):
                    self.game.uiM.draw_xp_bar()
                    self._handle_you_died_effect()
                    self._draw_blood_effect()
                    self._draw_blood_when_dead()
                    self._draw_start_transition()
                    self._handle_menu_to_game_transition()
                    self._handle_game_start_transition()
                    self._handle_in_game_transition()
                    self._handle_restart_transition()


          def _draw_start_transition(self):
                    if self.play_start_transition:
                              self.transition_effect.draw(-1)
                              if self.transition_effect.frame < 0:
                                        self.play_start_transition = False
                                        self.transition_effect.frame = 0

          def _handle_menu_to_game_transition(self):
                    if self.game.playing_transition and self.game.in_menu:
                              if self.transition_effect.draw():
                                        self.game.in_menu = False

          def _handle_game_start_transition(self):
                    if not self.game.in_menu and self.game.game_time < MISC["transition_time"]:
                              self.transition_effect.draw()

          def _handle_in_game_transition(self):
                    if not self.game.in_menu and self.game.game_time >= MISC["transition_time"] and self.game.playing_transition:
                              if not self.inverted_transition:
                                        self.transition_effect.frame = self.transition_effect.length
                                        self.inverted_transition = True
                              self.transition_effect.draw(-1)
                              if self.transition_effect.frame < 0:
                                        self.game.playing_transition = False

          def _handle_you_died_effect(self):
                    if self.game.died:
                              if self.youdied_start_time is None:
                                        self.youdied_start_time = self.game.game_time
                              elapsed_time = self.game.game_time - self.youdied_start_time
                              self.youdied_effect.alpha = min(max(elapsed_time / self.youdied_duration, 0), 1) * 255
                              self.youdied_effect.draw()

          def _handle_restart_transition(self):
                    if self.draw_restart_transition:
                              self.transition_effect.frame = 0
                              self.drawing_restart_transition = True
                              self.draw_restart_transition = False
                    if self.drawing_restart_transition:
                              self.transition_effect.draw()
                              if self.transition_effect.frame > self.transition_effect.length + 3:
                                        self.game.restart = True

          def _draw_blood_effect(self):
                    if self.has_blood_effect and not self.game.died:
                              elapsed_time = self.game.game_time - self.blood_effect_start_time
                              if elapsed_time < MISC["blood_effect_duration"]:
                                        self.blood_effect.draw()
                                        if self.blood_effect.frame > self.blood_effect.length:
                                                  self.blood_effect.frame = self.blood_effect.length
                              elif elapsed_time > MISC["blood_effect_duration"]:
                                        self.blood_effect.draw(-1)
                                        if self.blood_effect.frame < 0:
                                                  self.has_blood_effect = False

          def _draw_blood_when_dead(self):
                    if self.game.died:
                              self.blood_effect.frame = self.blood_effect.length
                              self.blood_effect.draw()
