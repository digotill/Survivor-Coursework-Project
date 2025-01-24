from Code.Individuals.Buttons import *
from Code.DataStructures.Grid import *
from Code.Individuals.Gun import *

class ButtonManager:
          def __init__(self, game):
                    self.game = game

                    self.game_buttons = {}
                    self.menu_buttons = {}
                    self.end_buttons = {}
                    self.sliders = {}

                    self._create_ingame_buttons()
                    self._create_sliders()
                    self.create_buttons()
                    self.create_weapons()
                    self.create_end_buttons()

                    self.button_cooldown_timer = Timer(General_Settings['cooldowns'][0], self.game.ticks)
                    self.value_cooldown_timer = Timer(General_Settings['cooldowns'][1], self.game.ticks)

          def _create_ingame_buttons(self):
                    for name, config in AllButtons["In_Game_Buttons"].items():
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
                    button_configs = AllButtons["Weapon_Buttons"] | AllButtons["Menu_Buttons"]
                    for name, config in button_configs.items():
                              button_class = Switch if name in ['easy', 'medium', 'hard', 'ak47', 'shotgun', 'minigun'] else Button
                              self.menu_buttons[name] = button_class(self.game, copy.deepcopy(config))

                    self.difficulty_switches = [self.menu_buttons[d] for d in ['easy', 'medium', 'hard']]
                    self.weapons_switches = [self.menu_buttons[w] for w in ['ak47', 'shotgun', 'minigun']]

          def create_end_buttons(self):
                    button_configs = AllButtons["End_Screen_Buttons"]
                    for name, config in button_configs.items():
                              self.end_buttons[name] = Button(self.game, copy.deepcopy(config))

          def create_weapons(self):
                    button_configs = AllButtons["Weapon_Buttons"]
                    self.weapons = {weapon_type: Gun(self.game, Weapons[weapon_type]) for weapon_type in button_configs.keys()}

          def update(self):
                    if not self.game.in_menu and not self.game.died:
                              for buttons in list(self.game_buttons.values()) + list(self.sliders.values()):
                                        buttons.active = self.game.changing_settings
                                        buttons.update()
                                        buttons.changeColor()

                              if self.game.mouse_state[0] and self.button_cooldown_timer.check(self.game.ticks):
                                        if self.game.changing_settings:
                                                  if self.game_buttons['resume'].check_for_input():
                                                            self.game.changing_settings = False
                                                  elif self.sliders['fps'].update_value:
                                                            self.game.fps = self.sliders['fps'].value
                                                  elif self.sliders['brightness'].update_value:
                                                            self.game.ui_manager.brightness = self.sliders['brightness'].value
                                                  elif self.game_buttons['fullscreen'].check_for_input():
                                                            pygame.display.toggle_fullscreen()
                                                  elif self.game_buttons['quit'].check_for_input():
                                                            self.game.running = False
                                                  elif self.game_buttons['return'].check_for_input():
                                                            self.game.restart = True

                                        # Reset the cooldown timer after any button press
                                        self.button_cooldown_timer.reactivate(self.game.ticks)

                              if self.game.changing_settings and self.value_cooldown_timer.check(self.game.ticks):
                                        self.game.fps = self.sliders['fps'].value
                                        self.game.ui_manager.brightness = self.sliders['brightness'].value
                                        self.value_cooldown_timer.reactivate(self.game.ticks)

                    elif self.game.in_menu and not self.game.died:
                              for button in sorted(self.menu_buttons.values(), key=lambda b: b.pos.y):
                                        button.update()
                                        button.changeColor()

                              if self.game.mouse_state[0] and self.button_cooldown_timer.check(self.game.ticks):
                                        if self.menu_buttons['play'].check_for_input():
                                                  self.game.playing_transition = True
                                        elif self.menu_buttons['quit'].check_for_input():
                                                  self.game.running = False
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

                                        # Reset the cooldown timer after any button press in the menu
                                        self.button_cooldown_timer.reactivate(self.game.ticks)

                    if self.game.died:
                              for button in sorted(self.end_buttons.values(), key=lambda b: b.pos.y):
                                        button.active = True
                                        button.update()
                                        button.changeColor()
                              if self.game.mouse_state[0] and self.button_cooldown_timer.check(self.game.ticks):
                                        if self.end_buttons['restart'].check_for_input():
                                                  self.game.restart = True
                                        elif self.end_buttons['quit'].check_for_input():
                                                  self.game.running = False

                                        self.button_cooldown_timer.reactivate(self.game.ticks)

          def draw(self):
                    # Sort all elements by their y position
                    if not self.game.in_menu and not self.game.died:
                              for button in sorted(list(self.game_buttons.values()) + list(self.sliders.values()), key=lambda element: element.pos.y):
                                        button.draw()
                    elif self.game.in_menu and not self.game.died:
                              for button in sorted(self.menu_buttons.values(), key=lambda b: b.pos.y):
                                        button.draw()
                    if self.game.died:
                              for button in sorted(self.end_buttons.values(), key=lambda b: b.pos.y):
                                        button.draw()