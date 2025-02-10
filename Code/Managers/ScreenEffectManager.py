from Code.Variables.SettingVariables import *
from Code.Individuals.ScreenEffect import *


class ScreenEffectManager:
          def __init__(self, game):
                    self.game = game
                    # Create screen effect for transitions
                    self.transition_screeneffect = ScreenEffect(self.game, self.game.assets["transition_screeneffect"], GENERAL['animation_speeds'][1])
                    # Create screen effect for "You Died" message
                    self.youdied_screeneffect = ScreenEffect(self.game, self.game.assets["youdied_screeneffect"], GENERAL['animation_speeds'][2])
                    self.inverted_transition = None  # Flag to track if transition is inverted
                    self.youdied_start_time = None  # Timestamp for when "You Died" effect starts
                    self.youdied_duration = MISC["youdied_duration"]   # Duration of "You Died" effect in seconds

          def draw(self):
                    # Handle transition from menu to game
                    if self.game.playing_transition and self.game.in_menu:
                              if self.transition_screeneffect.draw():
                                        self.game.in_menu = False  # Exit menu when transition completes
                    # Handle transition at the start of the game
                    elif not self.game.in_menu and self.game.game_time < MISC["transition_time"]:
                              self.transition_screeneffect.draw()
                    # Handle transition after game has started
                    elif not self.game.in_menu and self.game.game_time >= MISC["transition_time"]:
                              if self.inverted_transition is None:
                                        # Set the frame to the last frame to start the reverse animation
                                        self.transition_screeneffect.frame = self.transition_screeneffect.length
                                        self.inverted_transition = True  # Set flag to indicate transition is inverted
                              self.transition_screeneffect.draw(-1)  # Draw transition in reverse
                              if self.transition_screeneffect.frame < 0:
                                        self.game.playing_transition = False  # Exit transition when transition completes

                    # Handle "You Died" effect
                    if self.game.died:
                              if self.youdied_start_time is None:
                                        self.youdied_start_time = self.game.game_time  # Set start time when player dies
                              # Calculate alpha value for fade effect
                              self.youdied_screeneffect.alpha = (max(min(1, (self.game.game_time - self.youdied_start_time) / self.youdied_duration), 0)) * 255
                              self.youdied_screeneffect.draw()  # Draw "You Died" effect

