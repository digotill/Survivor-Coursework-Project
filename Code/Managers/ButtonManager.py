from Code.Individuals.Buttons import *
from Code.DataStructures.Grid import *
from Code.Individuals.Gun import *

class ButtonManager:
          def __init__(self, game):
                    self.game = game

                    self.game_buttons = {}
                    self.menu_buttons = {}
                    self.sliders = {}

                    self._create_ingame_buttons()
                    self._create_sliders()
                    self.create_buttons()
                    self.create_weapons()

                    self.cooldown = General_Settings['cooldowns'][0]
                    self.last_pressed_time = - General_Settings['cooldowns'][0]

                    self.value_cooldown = General_Settings['cooldowns'][1]
                    self.last_value_set = -General_Settings['cooldowns'][1]

          def _create_ingame_buttons(self):
                    for name, config in AllButtons["In_Game"].items():
                              self.game_buttons[name] = Button(
                                        self.game,
                                        copy.deepcopy(config)
                              )

          def _create_sliders(self):
                    for name, config in AllButtons["Sliders"].items():
                              self.sliders[name] = Slider(
                                        self.game,
                                        copy.deepcopy(config)
                              )

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

          def update(self):
                    if not self.game.in_menu:
                              for buttons in list(self.game_buttons.values()) + list(self.sliders.values()):
                                        buttons.active = self.game.changing_settings
                                        buttons.update()
                                        buttons.changeColor()

                              if self.game.changing_settings and self.game.mouse_state[
                                        0] and pygame.time.get_ticks() / 1000 - self.last_pressed_time > self.cooldown:
                                        temp_time = self.last_pressed_time
                                        self.last_pressed_time = pygame.time.get_ticks() / 1000
                                        if self.game_buttons['resume'].check_for_input():
                                                  self.game.changing_settings = False
                                        elif self.sliders['fps'].update_value:
                                                  self.game.fps = self.sliders['fps'].value
                                        elif self.sliders['brightness'].update_value:
                                                  self.game.ui_manager.brightness = self.sliders['brightness'].value
                                        elif self.game_buttons['fullscreen'].check_for_input():
                                                  pygame.display.toggle_fullscreen()
                                        elif self.game_buttons['quit'].check_for_input():
                                                  self.game.immidiate_quit = True
                                        elif self.game_buttons['return'].check_for_input():
                                                  self.game.restart = True
                                        else:
                                                  self.last_pressed_time = temp_time

                              if self.game.changing_settings and pygame.time.get_ticks() / 1000 - self.last_value_set > self.value_cooldown:
                                        self.game.fps = self.sliders['fps'].value
                                        self.game.ui_manager.brightness = self.sliders['brightness'].value
                                        self.last_value_set = pygame.time.get_ticks() / 1000
                    elif self.game.in_menu:
                              for button in sorted(self.menu_buttons.values(), key=lambda b: b.pos.y):
                                        button.update()
                                        button.changeColor()

                              if self.game.mouse_state[0]:
                                        if self.menu_buttons['play'].check_for_input():
                                                  self.game.playing_transition = True
                                        elif self.menu_buttons['quit'].check_for_input():
                                                  self.game.running = False
                                                  self.game.immidiate_quit = True
                                        else:
                                                  for button in self.difficulty_switches:
                                                            if button.can_change():
                                                                      self.difficulty = button.text_input
                                                                      button.change_on()
                                                                      for other_button in self.difficulty_switches:
                                                                                if other_button != button:
                                                                                          other_button.on = False
                                                  for button_name, button in self.menu_buttons.items():
                                                            if button in self.weapons_switches and button.can_change():
                                                                      self.game.player.gun = self.weapons[button_name]
                                                                      button.change_on()
                                                                      for other_button in self.weapons_switches:
                                                                                if other_button != button:
                                                                                          other_button.on = False

          def draw(self):
                    # Sort all elements by their y position
                    if not self.game.in_menu:
                              for button in sorted(list(self.game_buttons.values()) + list(self.sliders.values()), key=lambda element: element.pos.y):
                                        button.draw()
                    elif self.game.in_menu:
                              for button in sorted(self.menu_buttons.values(), key=lambda b: b.pos.y):
                                        button.draw()