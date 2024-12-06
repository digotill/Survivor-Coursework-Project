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

                    self.loading_screen = Green_Waterfall if random.random() < 0.5 else Orange_Pond
                    self.current_frame = 0
                    self.in_menu = True
                    self.difficulty = general_settings['difficulty']
                    self.return_value = None
                    self.animation_speed = general_settings["main_menu_animation_speed"]
                    self.create_weapons()

          def create_weapons(self):
                    self.weapons = {}
                    weapon_types = ["AK47", "Shotgun", "Minigun"]
                    weapon_images = {"AK47": AK47, "Shotgun": Shotgun, "Minigun": Minigun}

                    for weapon_type in weapon_types:
                              weapon_settings = weapons[weapon_type]
                              self.weapons[weapon_type] = Gun(
                                        self.game,
                                        weapon_images[weapon_type],
                                        weapon_settings["res"],
                                        Bullets,
                                        weapon_settings["vel"],
                                        weapon_settings["lifetime"],
                                        weapon_settings["lifetime_randomness"],
                                        weapon_settings["fire_rate"],
                                        weapon_settings["friction"],
                                        weapon_settings["damage"],
                                        weapon_settings["spread"],
                                        weapon_settings["distance_perpendicular"],
                                        weapon_settings["distance_parrallel"],
                                        weapon_settings["animation_speed"],
                                        weapon_settings["shake_mag"],
                                        weapon_settings["shake_duration"],
                                        weapon_settings["spread_time"],
                                        weapon_settings["clip_size"],
                                        weapon_settings["reload_time"],
                                        weapon_settings["pierce"],
                              )

                    self.gun = self.weapons["AK47"]

          def _create_buttons(self):
                    button_configs = {
                              'play': buttons['play'],
                              'quit': buttons['quit'],
                              'easy': buttons['easy'],
                              'medium': buttons['medium'],
                              'hard': buttons['hard'],
                              'AK47': buttons['AK47'],
                              "Shotgun": buttons['Shotgun'],
                              "Minigun": buttons['Minigun']
                              }
                    button_configs["AK47"]["image"] = perfect_outline(AK47)
                    button_configs["Shotgun"]["image"] = perfect_outline(Shotgun)
                    button_configs["Minigun"]["image"] = perfect_outline(Minigun)

                    for name, config in button_configs.items():
                              button_class = Switch if name in ['easy', 'medium', 'hard', 'AK47', 'Shotgun', 'Minigun'] else Button
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
                    self.buttons['AK47'].on = True

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
                    return self.return_value

          def update_difficulty(self):
                    new_stat = pd.DataFrame({'Coins': [0], 'Score': [0], 'Enemies Killed': [0], 'Difficulty': [self.difficulty]})
                    self.game.stats = pd.concat([self.game.stats, new_stat], ignore_index=True)



                    self.game.player = Player(self.game, player_attributes['health'] * general_settings[self.difficulty + "_difficulty"], player_attributes['res'], player_attributes['vel'],
                                              player_attributes['damage'] * general_settings[self.difficulty + "_difficulty"], self.gun, self.game.window.rect.center)


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
