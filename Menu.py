from Button_Class import *
from Initialize import *


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.PLAY_BUTTON = Button(Buttons[0], (300, 500), game, True, "Play", FONT, "black", "blue")
                    self.OPTIONS_BUTTON = Button(Buttons[1], (700, 800), game,  True, "Options", FONT, "black", "blue")
                    self.QUIT_BUTTON = Button(Buttons[2], (500, 700), game,  True, "Quit", FONT, "black", "blue")
                    self.BG = Main_Menu_BG

          def loop(self):
                    while True:
                              self.game.clock.tick(self.game.fps)

                              new_bg = pygame.transform.scale(self.BG, pygame.display.get_window_size())
                              self.game.display.blit(new_bg, (0, 0))

                              self.game.event_manager()
                              self.game.update_somethings()

                              if pygame.mouse.get_pressed()[0]:
                                        if self.PLAY_BUTTON.check_for_input(self.game.mouse_pos): return True
                                        elif self.OPTIONS_BUTTON.check_for_input(self.game.mouse_pos): self.game.settings.loop()
                                        elif self.QUIT_BUTTON.check_for_input(self.game.mouse_pos): return False

                              for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
                                        button.draw()
                                        button.update_pos()
                                        button.changeColor(self.game.mouse_pos)
                              self.game.display_mouse()

                              if self.game.running: pygame.display.flip()
                              else: break


class GameOver:
          def __init__(self, game):
                    self.game = game

          def update(self):
                    pass

          def loop(self):
                    pass


class Settings:
          def __init__(self, game):
                    self.game = game

          def loop(self):
                    pass
