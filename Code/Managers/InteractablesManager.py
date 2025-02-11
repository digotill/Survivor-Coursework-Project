from Code.Individuals.Interactable import *
from Code.DataStructures.HashMap import *
from Code.Individuals.Gun import *


class InteractablesManager:
          def __init__(self, game):
                    self.game = game

                    self.grabbing_slider = False

                    # Dictionaries to store different types of buttons and sliders
                    self.game_buttons = {}  # Buttons used during gameplay
                    self.menu_buttons = {}  # Buttons used in the main menu
                    self.end_buttons = {}  # Buttons used in the end screen
                    self.sliders = {}  # Sliders for adjusting settings
                    self.xp_bar = Button(self.game, BUTTONS["XP_bar"])

                    # Initialize all buttons and sliders
                    self._create_ingame_buttons()
                    self._create_sliders()
                    self.create_buttons()
                    self.create_weapons()
                    self.create_end_buttons()

                    # Timer to prevent rapid button presses
                    self.button_cooldown_timer = Timer(GENERAL['cooldowns'][0], self.game.ticks)
                    # Timer for updating values (e.g., FPS, brightness) at regular intervals
                    self.value_cooldown_timer = Timer(GENERAL['cooldowns'][1], self.game.ticks)

          def _create_ingame_buttons(self):
                    # Create buttons used during gameplay
                    for name, config in BUTTONS["In_Game_Buttons"].items():
                              self.game_buttons[name] = Button(
                                        self.game,
                                        copy.deepcopy(config)
                              )

          def _create_sliders(self):
                    # Create sliders for adjusting settings
                    for name, config in BUTTONS["Sliders"].items():
                              self.sliders[name] = Slider(
                                        self.game,
                                        copy.deepcopy(config)
                              )

          def create_buttons(self):
                    # Create buttons for the main menu, including weapon selection and difficulty
                    button_configs = BUTTONS["Weapon_Buttons"] | BUTTONS["Menu_Buttons"]
                    for name, config in button_configs.items():
                              # Use Switch class for specific buttons, Button class for others
                              button_class = Switch if name in ['easy', 'medium', 'hard', 'ak47', 'shotgun', 'minigun'] else Button
                              self.menu_buttons[name] = button_class(self.game, copy.deepcopy(config))

                    # Group difficulty and weapon switches for easier management
                    self.difficulty_switches = [self.menu_buttons[d] for d in ['easy', 'medium', 'hard']]
                    self.weapons_switches = [self.menu_buttons[w] for w in ['ak47', 'shotgun', 'minigun']]

          def create_end_buttons(self):
                    # Create buttons for the end screen
                    button_configs = BUTTONS["End_Screen_Buttons"]
                    for name, config in button_configs.items():
                              self.end_buttons[name] = Button(self.game, copy.deepcopy(config))

          def create_weapons(self):
                    # Create weapon objects for each weapon type
                    button_configs = BUTTONS["Weapon_Buttons"]
                    self.weapons = {weapon_type: Gun(self.game, WEAPONS[weapon_type]) for weapon_type in button_configs.keys()}

          def update(self):
                    # Update method handles button interactions based on game state
                    if not self.game.in_menu and not self.game.died:
                              # Update in-game buttons and sliders
                              self._update_ingame_buttons()
                    elif self.game.in_menu and not self.game.died:
                              # Update menu buttons
                              self._update_menu_buttons()
                    if self.game.died:
                              # Update end screen buttons
                              self._update_end_buttons()

          def _update_ingame_buttons(self):
                    # Update and handle interactions for in-game buttons and sliders
                    for buttons in list(self.game_buttons.values()) + list(self.sliders.values()):
                              buttons.active = self.game.changing_settings
                              buttons.update()
                              buttons.change_colour()

                    self.xp_bar.update()
                    self.xp_bar.text_input = "level: " + str(self.game.player.level)

                    if self.game.mouse_state[0] and self.button_cooldown_timer.check(self.game.ticks) and not self.grabbing_slider and self.game.changing_settings:
                              # Handle various button interactions in the settings menu
                              self._handle_settings_interactions()

                              # Reset the cooldown timer after any button press
                              self.button_cooldown_timer.reactivate(self.game.ticks)

                    # Update game settings based on slider values
                    if self.value_cooldown_timer.check(self.game.ticks):
                              self.game.fps = self.sliders['fps'].value
                              self.game.uiM.brightness = self.sliders['brightness'].value
                              self.game.reduced_screen_shake = self.sliders['shake'].value / 100
                              self.game.colour_mode = self.sliders['colour'].value
                              self.game.volume = self.sliders['volume'].value / 100
                              self.game.text_size = self.sliders['text_size'].value / 100

                              self.value_cooldown_timer.reactivate(self.game.ticks)

          def _handle_settings_interactions(self):
                    # Handle button interactions in the settings menu
                    if self.game_buttons['resume'].check_for_input():
                              self.game.changing_settings = False
                    elif self.game_buttons['fullscreen'].check_for_input():
                              pygame.display.toggle_fullscreen()
                    elif self.game_buttons['quit'].check_for_input():
                              self.game.running = False
                    elif self.game_buttons['return'].check_for_input():
                              self.game.screeneffectM.draw_restart_transition = True

          def _update_menu_buttons(self):
                    # Update and handle interactions for menu buttons
                    for button in sorted(self.menu_buttons.values(), key=lambda b: b.pos.y):
                              button.update()
                              button.change_colour()

                    if self.game.mouse_state[0] and self.button_cooldown_timer.check(self.game.ticks) and not self.grabbing_slider:
                              self._handle_menu_interactions()
                              self.button_cooldown_timer.reactivate(self.game.ticks)

          def _handle_menu_interactions(self):
                    # Handle button interactions in the main menu
                    if self.menu_buttons['play'].check_for_input():
                              self.game.playing_transition = True
                    elif self.menu_buttons['quit'].check_for_input():
                              self.game.running = False
                    else:
                              self._handle_difficulty_selection()
                              self._handle_weapon_selection()

          def _handle_difficulty_selection(self):
                    # Handle difficulty selection in the main menu
                    for button in self.difficulty_switches:
                              if button.can_change():
                                        self.game.difficulty = button.text_input
                                        button.change_on()
                                        for other_button in self.difficulty_switches:
                                                  if other_button != button:
                                                            other_button.on = False

          def _handle_weapon_selection(self):
                    # Handle weapon selection in the main menu
                    for button_name, button in self.menu_buttons.items():
                              if button in self.weapons_switches and button.can_change():
                                        self.game.player.gun = self.weapons[button_name]
                                        button.change_on()
                                        for other_button in self.weapons_switches:
                                                  if other_button != button:
                                                            other_button.on = False

          def _update_end_buttons(self):
                    # Update and handle interactions for end screen buttons
                    for button in sorted(self.end_buttons.values(), key=lambda b: b.pos.y):
                              button.active = True
                              button.update()
                              button.change_colour()
                    if self.game.mouse_state[0] and self.button_cooldown_timer.check(self.game.ticks):
                              if self.end_buttons['restart'].check_for_input():
                                        self.game.screeneffectM.draw_restart_transition = True
                              elif self.end_buttons['quit'].check_for_input():
                                        self.game.running = False
                              self.button_cooldown_timer.reactivate(self.game.ticks)

          def draw(self):
                    # Draw all relevant buttons based on the current game state
                    if not self.game.in_menu and not self.game.died:
                              # Draw in-game buttons and sliders
                              for button in sorted(list(self.game_buttons.values()) + list(self.sliders.values()), key=lambda element: element.pos.y):
                                        button.draw()
                              self.xp_bar.draw()
                    elif self.game.in_menu and not self.game.died:
                              # Draw menu buttons
                              for button in sorted(self.menu_buttons.values(), key=lambda b: b.pos.y):
                                        button.draw()
                    if self.game.died:
                              # Draw end screen buttons
                              for button in sorted(self.end_buttons.values(), key=lambda b: b.pos.y):
                                        button.draw()
