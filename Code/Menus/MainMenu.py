from Code.Individuals.Player import *
from Code.Individuals.Buttons import *
from Code.Individuals.Gun import *


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.buttons = {}
                    self._create_buttons()
                    self.difficulty_switchs = [self.buttons['easy'], self.buttons['medium'], self.buttons['hard']]
                    self.weapons_switches = [self.buttons['ak47'], self.buttons['shotgun'], self.buttons['minigun']]

                    for button in self.buttons.values():
                              button.active = True

                    self.background_frame = 0
                    self.transition_frame = 0
                    self.playing_transition = False
                    self.difficulty = "medium"
                    self.create_weapons()
                    self.loop()

          def create_weapons(self):
                    self.weapons = {}

                    for weapon_type in ["ak47", "shotgun", "minigun"]:
                              weapon_settings = Weapons[weapon_type]
                              self.weapons[weapon_type] = Gun(
                                        self.game, weapon_settings
                              )

                    self.gun = self.weapons["ak47"]

          def _create_buttons(self):
                    button_configs = AllButtons
                    for name, config in (button_configs["Weapons"] | button_configs["Menu_Buttons"]).items():
                              button_class = Switch if name in ['easy', 'medium', 'hard', 'ak47', 'shotgun',
                                                                'minigun'] else Button
                              self.buttons[name] = button_class(self.game,
                                                                copy.deepcopy(config)
                                                                )

                    self.buttons['medium'].on = True
                    self.buttons['ak47'].on = True

          def loop(self):
                    while self.game.in_menu and self.game.running:
                              self.game.clock.tick(self.game.fps)
                              self.draw_background()

                              self.game.manage_events()
                              self.game.update_variables()

                              sorted_buttons = sorted(self.buttons.values(), key=lambda b: b.pos.y)
                              for button in sorted_buttons:
                                        button.update()
                                        button.changeColor()
                                        button.draw()

                              self.draw_transition()

                              if pygame.mouse.get_pressed()[0]:
                                        if self.buttons['play'].check_for_input():
                                                  self.playing_transition = True
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

                    self.update()

          def update(self):
                    new_stat = pd.DataFrame(
                              {'Coins': [0], 'Score': [0], 'Enemies Killed': [0], 'Difficulty': [self.difficulty]})
                    self.game.stats = pd.concat([self.game.stats, new_stat], ignore_index=True)

                    self.game.player = Player(self.game, self.gun, Player_Attributes)

          def draw_background(self):
                    self.game.display_screen.blit(self.game.assets["main_menu"][int(self.background_frame) % len(self.game.assets["main_menu"])])
                    self.background_frame += self.game.dt * General_Settings['animation_speeds'][0]

          def draw_transition(self):
                    if self.playing_transition:
                              self.game.ui_surface.blit(self.game.assets["transition_screeneffect"][int(self.transition_frame) % len(self.game.assets["transition_screeneffect"])])
                              self.transition_frame += self.game.dt * General_Settings['animation_speeds'][1]
                              if self.transition_frame > len(self.game.assets["transition_screeneffect"]) - 1:
                                        self.game.in_menu = False