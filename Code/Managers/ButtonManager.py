from Code.Individuals.Buttons import *
from Code.DataStructures.Grid import *

class ButtonManager:
          def __init__(self, game):
                    self.game = game

                    self.game_buttons = {}
                    self.menu_buttons = {}
                    self.sliders = {}

                    self._create_ingame_buttons()
                    self._create_sliders()

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

          def update(self):
                    all_elements = list(self.game_buttons.values()) + list(self.sliders.values())
                    for buttons in all_elements:
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

          def draw(self):
                    all_elements = list(self.game_buttons.values()) + list(self.sliders.values())

                    # Sort all elements by their y position
                    sorted_elements = sorted(all_elements, key=lambda element: element.pos.y)
                    for button in sorted_elements:
                              button.draw()