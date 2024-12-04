import pandas as pd

from Code.Classes.Buttons import *
from Code.Classes.Entities import *


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.play_button = SlidingButtons(self.game, Buttons[0], FULLSCREEN_BUTTON_POS, "y", "max",
                                                      text_input="Play")
                    self.quit_button = SlidingButtons(self.game, Buttons[0], NEW_QUIT_BUTTON_POS, "y", "max",
                                                      text_input="Quit")
                    self.easy_button = SwitchButton(self.game, Buttons[0], HARD_BUTTON_POS, "y", "max",
                                                      text_input="EASY")
                    self.medium_button = SwitchButton(self.game, Buttons[0], MEDIUM_BUTTON_POS, "y", "max",
                                                      text_input="MEDIUM")
                    self.hard_button = SwitchButton(self.game, Buttons[0], EASY_BUTTON_POS, "y", "max",
                                                     text_input="HARD")
                    self.buttons = [self.play_button, self.quit_button, self.easy_button, self.medium_button, self.hard_button]
                    self.difficulty_buttons = [self.easy_button, self.medium_button, self.hard_button]
                    for button in self.buttons:
                              button.active = True
                    self.loading_screen = Green_Waterfall if random.random() < 0.5 else Orange_Pond
                    self.current_frame = 0
                    self.in_menu = True
                    self.difficulty = 'MEDIUM'
                    self.return_value = None
                    self.player_health_multiplier = 1
                    self.player_damage_multiplier = 1
                    self.animation_speed = MAIN_MENU_ANIMATION_SPEED

          def loop(self):
                    while self.in_menu and self.game.running:
                              self.game.clock.tick(self.game.fps)
                              self.draw_and_update_background()

                              self.game.manage_events()
                              self.game.update_game_variables()

                              for button in self.buttons:
                                        button.update()
                                        button.changeColor()
                                        button.draw()

                              if pygame.mouse.get_pressed()[0]:
                                        if self.play_button.check_for_input():
                                                  self.in_menu = False
                                        if self.quit_button.check_for_input():
                                                  self.game.running = False
                                        for button1 in self.difficulty_buttons:
                                                  if button1.can_change():
                                                            self.difficulty = button1.text_input
                                                            button1.change_on()
                                                            for button2 in self.difficulty_buttons:
                                                                      if button2 != button1:
                                                                                button2.on = False

                              self.game.update_display()

                    self.update_difficulty()
                    return self.return_value

          def update_difficulty(self):
                    new_stat = pd.DataFrame({'Coins': [0], 'Score': [0], 'Enemies Killed': [0], 'Difficulty': [self.difficulty]})
                    self.game.stats = pd.concat([self.game.stats, new_stat], ignore_index=True)

                    self.game.enemy_manager.enemy_multiplier = eval(str(self.difficulty) + "_ENEMY_MULTIPLYER")
                    self.player_health_multiplier = eval(str(self.difficulty) + "_PLAYER_HEALTH_MULTIPLYER")
                    self.player_damage_multiplier = eval(str(self.difficulty) + "_PLAYER_DAMAGE_MULTIPLYER")

                    self.game.player = Player(self.game, PLAYER_HEALTH * self.player_health_multiplier, PLAYER_RES, PLAYER_VEL,
                                              PLAYER_DAMAGE * self.player_damage_multiplier, self.game.window.rect.center)
                    self.game.enemy_manager.enemy_multiplier = eval(str(self.difficulty) + "_ENEMY_MULTIPLYER")

          def draw_and_update_background(self):
                    self.game.display_screen.blit(pygame.transform.scale(
                              self.loading_screen[int(self.current_frame) % len(self.loading_screen)],
                              self.game.display_screen.size))
                    self.current_frame -= self.game.dt * self.animation_speed

class GameOver:
          def __init__(self, game):
                    self.game = game

          def update(self):
                    if self.game.player.health < 0: self.running = False

          def loop(self):
                    pass
