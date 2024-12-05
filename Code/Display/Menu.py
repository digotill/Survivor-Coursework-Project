import pandas as pd

from Code.Classes.Buttons import *
from Code.Classes.Entities import *
from Code.Utilities.Utils import *


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.play_button = Button(self.game, Buttons[0], FULLSCREEN_BUTTON_POS, PLAY_BUTTON_AXIS,
                                        PLAY_BUTTON_AXISL, text_input=PLAY_BUTTON_NAME)
                    self.quit_button = Button(self.game, Buttons[0], QUIT_BUTTON_POS, QUIT_BUTTON_AXIS,
                                        QUIT_BUTTON_AXISL, text_input=QUIT_BUTTON_NAME)
                    self.easy_button = StoreButton(self.game, Buttons[0], HARD_BUTTON_POS, EASY_BUTTON_AXIS,
                                        EASY_BUTTON_AXISL, text_input=EASY_BUTTON_NAME)
                    self.medium_button = StoreButton(self.game, Buttons[0], MEDIUM_BUTTON_POS, MEDIUM_BUTTON_AXIS,
                                                  MEDIUM_BUTTON_AXISL, text_input=MEDIUM_BUTTON_NAME, on=True)
                    self.hard_button = StoreButton(self.game, Buttons[0], EASY_BUTTON_POS, HARD_BUTTON_AXIS,
                                        HARD_BUTTON_AXISL, text_input=HARD_BUTTON_NAME)
                    self.ak_47_button = StoreButton(self.game, perfect_outline_2(AK_47), (140, 240), "x", "min")
                    self.buttons = [self.play_button, self.quit_button, self.easy_button, self.medium_button, self.hard_button, self.ak_47_button]
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
