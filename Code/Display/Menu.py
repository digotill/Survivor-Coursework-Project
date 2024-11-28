from Code.Classes.Buttons import *
from Code.Variables.Initialize import *
from Code.Variables.Variables import *
from Code.Classes.Entities import *
import random



class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.PLAY_BUTTON = Button(Buttons[0], PLAY_BUTTON_POS, game, True, PLAY_BUTTON_NAME, FONT,
                                              PLAY_BUTTON_BASE_COLOUR, PLAY_BUTTON_HOVERING_COLOUR)
                    self.QUIT_BUTTON = Button(Buttons[2], QUIT_BUTTON_POS, game,  True, QUIT_BUTTON_NAME, FONT,
                                              QUIT_BUTTON_BASE_COLOUR, QUIT_BUTTON_HOVERING_COLOUR)
                    self.EASY_BUTTON = SwitchButton(Buttons[0], EASY_BUTTON_POS, game, True, EASY_BUTTON_NAME, FONT,
                                              EASY_BUTTON_BASE_COLOUR, EASY_BUTTON_HOVERING_COLOUR)
                    self.MEDIUM_BUTTON = SwitchButton(Buttons[0], MEDIUM_BUTTON_POS, game, True, MEDIUM_BUTTON_NAME, FONT,
                                                      MEDIUM_BUTTON_BASE_COLOUR, MEDIUM_BUTTON_HOVERING_COLOUR, on=True)
                    self.HARD_BUTTON = SwitchButton(Buttons[0], HARD_BUTTON_POS, game, True, HARD_BUTTON_NAME, FONT,
                                                    HARD_BUTTON_BASE_COLOUR, HARD_BUTTON_HOVERING_COLOUR)
                    self.buttons = [self.PLAY_BUTTON, self.QUIT_BUTTON, self.EASY_BUTTON, self.MEDIUM_BUTTON, self.HARD_BUTTON]
                    for button in self.buttons:
                              button.active = True
                    self.BG = Main_Menu_BG
                    self.loading_screen = loading_screen_1 if random.random() < 0.5 else loading_screen_2
                    self.current_frame = 0
                    self.in_menu = False

          def loop(self):
                    global player_health_multiplier, player_damage_multiplier
                    self.in_menu = True
                    return_value = None
                    difficulty = 'Medium'
                    while self.in_menu and self.game.running:
                              self.game.clock.tick(self.game.fps)
                              if self.game.display.size != WIN_RES:
                                        self.game.display.blit(pygame.transform.scale(self.loading_screen[int(self.current_frame) % len(self.loading_screen)], self.game.display.size))
                              else: self.game.display.blit(self.loading_screen[int(self.current_frame) % len(self.loading_screen)])
                              self.current_frame -= ANIMATION_SPEED * self.game.dt * 3

                              self.game.manage_events()
                              self.game.update_game_variables()

                              for button in self.buttons:
                                        button.update_size_and_position()
                                        button.changeColor(self.game.mouse_pos)
                                        button.draw()

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
                              pygame.display.flip()

                    new_stat = pd.DataFrame(
                              {'Coins': [0], 'Score': [0], 'Enemies Killed': [0], 'Difficulty': [difficulty]})
                    self.game.stats = pd.concat([self.game.stats, new_stat], ignore_index=True)
                    if difficulty == 'Easy':
                              self.game.enemy_manager.enemy_multiplier = 0.7
                              player_health_multiplier = 1.5
                              player_damage_multiplier = 1.1
                    elif difficulty == 'Medium':
                              self.game.enemy_manager.enemy_multiplier = 1
                              player_health_multiplier = 1
                              player_damage_multiplier = 1
                    elif difficulty == 'Hard':
                              self.game.enemy_manager.enemy_multiplier = 1.3
                              player_health_multiplier = 0.7
                              player_damage_multiplier = 0.9
                    self.game.player = Player(self.game, PLAYER_HEALTH * player_health_multiplier, PLAYER_RES, PLAYER_VEL,
                                         PLAYER_DAMAGE * player_damage_multiplier, self.game.window.rect.center)
                    return return_value


class GameOver:
          def __init__(self, game):
                    self.game = game

          def update(self):
                    if self.game.player.health < 0: self.running = False

          def loop(self):
                    pass

