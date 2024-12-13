import pandas as pd

from Code.Classes.Buttons import *
from Code.Classes.Entities import *
from Code.Utilities.Utils import *


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.buttons = {}
                    self._create_buttons()
                    self.difficulty_switchs = [self.buttons['easy'], self.buttons['medium'], self.buttons['hard']]
                    self.weapons_switches = [self.buttons['AK47'], self.buttons['Shotgun'], self.buttons['Minigun']]

                    for button in self.buttons.values():
                              button.active = True

                    self.loading_screen = Loading_Screens["Green_Waterfall"] if random.random() < 0.5 else \
                              Loading_Screens["Orange_Pond"]
                    self.current_frame = 0
                    self.difficulty = "MEDIUM"
                    self.animation_speed = General_Settings["main_menu_animation_speed"]
                    self.create_weapons()

          def create_weapons(self):
                    self.weapons = {}

                    for weapon_type in ["AK47", "Shotgun", "Minigun"]:
                              weapon_settings = Weapons[weapon_type]
                              self.weapons[weapon_type] = Gun(
                                        self.game, weapon_settings
                              )

                    self.gun = self.weapons["AK47"]

          def _create_buttons(self):
                    button_configs = AllButtons
                    for name, config in (button_configs["Weapons"] | button_configs["Menu_Buttons"]).items():
                              button_class = Switch if name in ['easy', 'medium', 'hard', 'AK47', 'Shotgun',
                                                                'Minigun'] else Button
                              self.buttons[name] = button_class(self.game,
                                                                copy.deepcopy(config)
                                                                )

                    self.buttons['medium'].on = True
                    self.buttons['AK47'].on = True

          def loop(self):
                    while self.game.in_menu and self.game.running:
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
                                                  self.game.in_menu = False
                                        if self.buttons['quit'].check_for_input():
                                                  self.game.running = False
                                                  self.game.immidiate_quit = True
                                        for button in self.difficulty_switchs:
                                                  if button.can_change():
                                                            self.difficulty = button.text_input
                                                            button.change_on()
                                                            for other_button in self.difficulty_switchs:
                                                                      if other_button != button:
                                                                                other_button.on = False
                                        for button_name, button in self.buttons.items():
                                                  if button in self.weapons_switches and button.can_change():
                                                            self.gun = self.weapons[button_name]
                                                            button.change_on()
                                                            for other_button in self.weapons_switches:
                                                                      if other_button != button:
                                                                                other_button.on = False

                              self.game.update_display()

                    self.update_difficulty()

          def update_difficulty(self):
                    new_stat = pd.DataFrame(
                              {'Coins': [0], 'Score': [0], 'Enemies Killed': [0], 'Difficulty': [self.difficulty]})
                    self.game.stats = pd.concat([self.game.stats, new_stat], ignore_index=True)

                    self.game.player = Player(self.game, self.game.window.rect.center, self.gun, Player_Attributes)

          def draw_and_update_background(self):
                    self.game.display_screen.blit(pygame.transform.scale(
                              self.loading_screen[int(self.current_frame) % len(self.loading_screen)],
                              self.game.display_screen.size))
                    self.current_frame -= self.game.dt * self.animation_speed


class GameOver:
          def __init__(self, game):
                    self.game = game

          def update(self):
                    if self.game.player.pierce < 0: self.running = False

          def loop(self):
                    pass
