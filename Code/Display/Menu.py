import pandas as pd

from Code.Classes.Buttons import *
from Code.Classes.Entities import *


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.PLAY_BUTTON = Button(Buttons[0], PLAY_BUTTON_POS, game, True, PLAY_BUTTON_NAME, FONT,
                                              PLAY_BUTTON_BASE_COLOUR, PLAY_BUTTON_HOVERING_COLOUR)
                    self.QUIT_BUTTON = Button(Buttons[2], QUIT_BUTTON_POS, game, True, QUIT_BUTTON_NAME, FONT,
                                              QUIT_BUTTON_BASE_COLOUR, QUIT_BUTTON_HOVERING_COLOUR)
                    self.EASY_BUTTON = SwitchButton(Buttons[0], EASY_BUTTON_POS, game, True, EASY_BUTTON_NAME, FONT,
                                                    EASY_BUTTON_BASE_COLOUR, EASY_BUTTON_HOVERING_COLOUR)
                    self.MEDIUM_BUTTON = SwitchButton(Buttons[0], MEDIUM_BUTTON_POS, game, True, MEDIUM_BUTTON_NAME,
                                                      FONT,
                                                      MEDIUM_BUTTON_BASE_COLOUR, MEDIUM_BUTTON_HOVERING_COLOUR, on=True)
                    self.HARD_BUTTON = SwitchButton(Buttons[0], HARD_BUTTON_POS, game, True, HARD_BUTTON_NAME, FONT,
                                                    HARD_BUTTON_BASE_COLOUR, HARD_BUTTON_HOVERING_COLOUR)
                    self.fullscreen_button = SlidingButtons(self.game, Buttons[0], FULLSCREEN_BUTTON_POS, "y", "max",
                                                            text_input="Fullscreen")
                    self.buttons = [self.PLAY_BUTTON, self.QUIT_BUTTON, self.EASY_BUTTON, self.MEDIUM_BUTTON,
                                    self.HARD_BUTTON]
                    for button in self.buttons:
                              button.active = True
                    self.loading_screen = Green_Waterfall if random.random() < 0.5 else Orange_Pond
                    self.current_frame = 0
                    self.in_menu = False

          def loop(self):
                    global player_health_multiplier, player_damage_multiplier
                    self.in_menu = True
                    return_value = None
                    difficulty = 'Medium'
                    self.fullscreen_button.active = True
                    while self.in_menu and self.game.running:
                              self.game.clock.tick(self.game.fps)
                              self.game.display.blit(pygame.transform.scale(
                                        self.loading_screen[int(self.current_frame) % len(self.loading_screen)],
                                        self.game.display.size))
                              self.current_frame -= self.game.dt * MAIN_MENU_ANIMATION_SPEED

                              self.game.manage_events()
                              self.game.update_game_variables()

                              for button in self.buttons:
                                        button.update_size_and_position()
                                        button.changeColor(self.game.mouse_pos)
                                        button.draw()
                              self.fullscreen_button.update()
                              self.fullscreen_button.changeColor()
                              self.fullscreen_button.draw()

                              if pygame.mouse.get_pressed()[0]:
                                        if self.PLAY_BUTTON.check_for_input(self.game.mouse_pos):
                                                  return_value = False
                                                  self.in_menu = False
                                        elif self.QUIT_BUTTON.check_for_input(self.game.mouse_pos):
                                                  return_value = True
                                                  self.in_menu = False
                                        elif self.EASY_BUTTON.check_for_input(self.game.mouse_pos):
                                                  self.HARD_BUTTON.on = False
                                                  self.MEDIUM_BUTTON.on = False
                                                  difficulty = 'Easy'
                                        elif self.HARD_BUTTON.check_for_input(self.game.mouse_pos):
                                                  self.MEDIUM_BUTTON.on = False
                                                  self.EASY_BUTTON.on = False
                                                  difficulty = 'Hard'
                                        elif self.MEDIUM_BUTTON.check_for_input(self.game.mouse_pos):
                                                  self.HARD_BUTTON.on = False
                                                  self.EASY_BUTTON.on = False
                                                  difficulty = 'Medium'

                              self.game.ui.display_mouse()
                              self.game.display.blit(self.game.ui_surface)
                              self.game.ui_surface.fill((0, 0, 0, 0))
                              pygame.display.flip()

                    new_stat = pd.DataFrame(
                              {'Coins': [0], 'Score': [0], 'Enemies Killed': [0], 'Difficulty': [difficulty]})
                    self.game.stats = pd.concat([self.game.stats, new_stat], ignore_index=True)
                    if difficulty == 'Easy':
                              self.game.enemy_manager.enemy_multiplier = EASY_ENEMY_MULTIPLYER
                              player_health_multiplier = EASY_PLAYER_HEALTH_MULTIPLYER
                              player_damage_multiplier = EASY_PLAYER_DAMAGE_MULTIPLYER
                    elif difficulty == 'Medium':
                              self.game.enemy_manager.enemy_multiplier = MEDIUM_ENEMY_MULTIPLYER
                              player_health_multiplier = MEDIUM_PLAYER_HEALTH_MULTIPLYER
                              player_damage_multiplier = MEDIUM_PLAYER_DAMAGE_MULTIPLYER
                    elif difficulty == 'Hard':
                              self.game.enemy_manager.enemy_multiplier = HARD_ENEMY_MULTIPLYER
                              player_health_multiplier = HARD_PLAYER_HEALTH_MULTIPLYER
                              player_damage_multiplier = HARD_PLAYER_DAMAGE_MULTIPLYER
                    self.game.player = Player(self.game, PLAYER_HEALTH * player_health_multiplier, PLAYER_RES,
                                              PLAYER_VEL,
                                              PLAYER_DAMAGE * player_damage_multiplier, self.game.window.rect.center)
                    return return_value


class GameOver:
          def __init__(self, game):
                    self.game = game

          def update(self):
                    if self.game.player.health < 0: self.running = False

          def loop(self):
                    pass
