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
                    self.difficulty = general_settings['difficulty']
                    self.return_value = None
                    self.animation_speed = general_settings["main_menu_animation_speed"]

          def _create_buttons(self):
                    button_configs = {
                              'play': buttons['play'],
                              'quit': buttons['quit'],
                              'easy': buttons['easy'],
                              'medium': buttons['medium'],
                              'hard': buttons['hard'],
                              'ak_47': buttons['ak47'],
                              "shotgun": buttons['shotgun'],
                              "minigun": buttons['minigun']
                              }
                    button_configs["ak_47"]["image"] = perfect_outline(AK_47)
                    button_configs["shotgun"]["image"] = perfect_outline(Shotgun)
                    button_configs["minigun"]["image"] = perfect_outline(Minigun)

                    for name, config in button_configs.items():
                              button_class = Switch if name in ['easy', 'medium', 'hard'] else Button
                              self.buttons[name] = button_class(
                                        self.game,
                                        config.get('image', Buttons[0]),
                                        config['pos'],
                                        config['axis'],
                                        config['axisl'],
                                        text_input=config['name'],
                                        text_pos=config['text_pos']
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
                                                  self.game.immidiate_quit = True
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

                    self.game.player = Player(self.game, player_attributes['health'] * general_settings[self.difficulty + "_difficulty"], player_attributes['res'], player_attributes['vel'],
                                              player_attributes['damage'] * general_settings[self.difficulty + "_difficulty"], self.game.window.rect.center)


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
