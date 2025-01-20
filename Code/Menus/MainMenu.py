from Code.Individuals.Player import *
from Code.Individuals.Buttons import *
from Code.Individuals.Gun import *


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.menu_buttons = {}
                    self.create_buttons()
                    self.create_weapons()
                    self.background_frame = 0
                    self.transition_frame = 0
                    self.playing_transition = False
                    self.difficulty = "medium"
                    self.loop()

          def create_buttons(self):
                    button_configs = AllButtons["Weapons"] | AllButtons["Menu_Buttons"]
                    for name, config in button_configs.items():
                              button_class = Switch if name in ['easy', 'medium', 'hard', 'ak47', 'shotgun', 'minigun'] else Button
                              self.menu_buttons[name] = button_class(self.game, copy.deepcopy(config))
                              self.menu_buttons[name].active = True

                    self.menu_buttons['medium'].on = True
                    self.menu_buttons['ak47'].on = True

                    self.difficulty_switches = [self.menu_buttons[d] for d in ['easy', 'medium', 'hard']]
                    self.weapons_switches = [self.menu_buttons[w] for w in ['ak47', 'shotgun', 'minigun']]

          def create_weapons(self):
                    self.weapons = {weapon_type: Gun(self.game, Weapons[weapon_type])
                                    for weapon_type in ["ak47", "shotgun", "minigun"]}
                    self.gun = self.weapons["ak47"]

          def loop(self):
                    while self.game.in_menu and self.game.running:
                              self.game.clock.tick(self.game.fps)
                              self.game.manage_events()
                              self.game.game_variables.update()

                              self.draw_background()
                              self.update_buttons()
                              self.handle_input()
                              self.draw_transition()

                              self.game.update_display()

                    self.update()

          def update_buttons(self):
                    for button in sorted(self.menu_buttons.values(), key=lambda b: b.pos.y):
                              button.update()
                              button.changeColor()
                              button.draw()

          def handle_input(self):
                    if self.game.mouse_state[0]:
                              if self.menu_buttons['play'].check_for_input():
                                        self.playing_transition = True
                              elif self.menu_buttons['quit'].check_for_input():
                                        self.game.running = False
                                        self.game.immidiate_quit = True
                              else:
                                        self.handle_difficulty_selection()
                                        self.handle_weapon_selection()

          def handle_difficulty_selection(self):
                    for button in self.difficulty_switches:
                              if button.can_change():
                                        self.difficulty = button.text_input
                                        button.change_on()
                                        for other_button in self.difficulty_switches:
                                                  if other_button != button:
                                                            other_button.on = False

          def handle_weapon_selection(self):
                    for button_name, button in self.menu_buttons.items():
                              if button in self.weapons_switches and button.can_change():
                                        self.gun = self.weapons[button_name]
                                        button.change_on()
                                        for other_button in self.weapons_switches:
                                                  if other_button != button:
                                                            other_button.on = False

          def update(self):
                    new_stat = pd.DataFrame({'Coins': [0], 'Score': [0], 'Enemies Killed': [0], 'Difficulty': [self.difficulty]})
                    self.game.stats = pd.concat([self.game.stats, new_stat], ignore_index=True)
                    self.game.player = Player(self.game, self.gun, Player_Attributes)

          def draw_background(self):
                    frame = int(self.background_frame) % len(self.game.assets["main_menu"])
                    self.game.display_screen.blit(self.game.assets["main_menu"][frame])
                    self.background_frame += self.game.dt * General_Settings['animation_speeds'][0]

          def draw_transition(self):
                    if self.playing_transition:
                              frame = int(self.transition_frame) % len(self.game.assets["transition_screeneffect"])
                              self.game.ui_surface.blit(self.game.assets["transition_screeneffect"][frame])
                              self.transition_frame += self.game.dt * General_Settings['animation_speeds'][1]
                              if self.transition_frame > len(self.game.assets["transition_screeneffect"]) - 1:
                                        self.game.in_menu = False
