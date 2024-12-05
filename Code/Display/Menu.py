import pandas as pd

from Code.Classes.Buttons import *
from Code.Classes.Entities import *
from Code.Utilities.Utils import *


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.buttons = {}
                    self._create_buttons()
                    self.difficulty_buttons = [self.buttons['easy'], self.buttons['medium'], self.buttons['hard']]

                    for button in self.buttons.values():
                              button.active = True

                    self.loading_screen = Green_Waterfall if random.random() < 0.5 else Orange_Pond
                    self.current_frame = 0
                    self.in_menu = True
                    self.difficulty = STARTING_DIFFICULTY
                    self.return_value = None
                    self.player_health_multiplier = 1
                    self.player_damage_multiplier = 1
                    self.animation_speed = MAIN_MENU_ANIMATION_SPEED

          def _create_buttons(self):
                    button_configs = {
                              'play': BUTTONS['PLAY'],
                              'quit': BUTTONS['QUIT'],
                              'easy': BUTTONS['EASY'],
                              'medium': BUTTONS['MEDIUM'],
                              'hard': BUTTONS['HARD'],
                              'ak_47': {
                                        'image': perfect_outline_2(AK_47),
                                        'POS': (140, 240),
                                        'AXIS': "x",
                                        'AXISL': "min",
                                        'NAME': ""
                              }
                    }

                    for name, config in button_configs.items():
                              button_class = StoreButton if name in ['easy', 'medium', 'hard'] else Button
                              self.buttons[name] = button_class(
                                        self.game,
                                        config.get('image', Buttons[0]),
                                        config['POS'],
                                        config['AXIS'],
                                        config['AXISL'],
                                        text_input=config['NAME']
                              )

                    # Set medium difficulty as default
                    self.buttons['medium'].on = True

          def loop(self):
                    while self.in_menu and self.game.running:
                              self.game.clock.tick(self.game.fps)
                              self.draw_and_update_background()

                              self.game.manage_events()
                              self.game.update_game_variables()

                              for button in self.buttons.values():
                                        button.update()
                                        button.changeColor()
                                        button.draw()

                              if pygame.mouse.get_pressed()[0]:
                                        if self.buttons['play'].check_for_input():
                                                  self.in_menu = False
                                        if self.buttons['quit'].check_for_input():
                                                  self.game.running = False
                                        for button in self.difficulty_buttons:
                                                  if button.can_change():
                                                            self.difficulty = button.text_input
                                                            button.change_on()
                                                            for other_button in self.difficulty_buttons:
                                                                      if other_button != button:
                                                                                other_button.on = False

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
