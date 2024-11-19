from Code.Classes.Button_Class import *
from Code.Variables.Initialize import *


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.PLAY_BUTTON = Button(Buttons[0], PLAY_BUTTON_POS, game, True, PLAY_BUTTON_NAME, FONT,
                                              PLAY_BUTTON_BASE_COLOUR, PLAY_BUTTON_HOVERING_COLOUR)
                    self.OPTIONS_BUTTON = Button(Buttons[1], OPTIONS_BUTTON_POS, game,  True, OPTIONS_BUTTON_NAME, FONT,
                                                 OPTIONS_BUTTON_BASE_COLOUR, OPTIONS_BUTTON_HOVERING_COLOUR)
                    self.QUIT_BUTTON = Button(Buttons[2], QUIT_BUTTON_POS, game,  True, QUIT_BUTTON_NAME, FONT,
                                              QUIT_BUTTON_BASE_COLOUR, QUIT_BUTTON_HOVERING_COLOUR)
                    self.BG = Main_Menu_BG

          def loop(self):
                    while True:
                              self.game.clock.tick(self.game.fps)

                              new_bg = pygame.transform.scale(self.BG, pygame.display.get_window_size())
                              self.game.display.blit(new_bg, (0, 0))

                              self.game.event_manager()
                              self.game.update_game_variables()

                              if pygame.mouse.get_pressed()[0]:
                                        if self.PLAY_BUTTON.check_for_input(self.game.mouse_pos): return True
                                        elif self.OPTIONS_BUTTON.check_for_input(self.game.mouse_pos): self.game.settings.loop()
                                        elif self.QUIT_BUTTON.check_for_input(self.game.mouse_pos): return False

                              for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
                                        button.draw()
                                        button.update_pos()
                                        button.changeColor(self.game.mouse_pos)
                              self.game.background.display_mouse()

                              if self.game.running: pygame.display.flip()
                              else: break



class GameOver:
          def __init__(self, game):
                    self.game = game

          def update(self):
                    if self.game.player.health < 0: self.running = False

          def loop(self):
                    pass


class Settings:
          def __init__(self, game):
                    self.game = game

          def loop(self):
                    pass
