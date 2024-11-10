from Button import *
from Initialize import *


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.PLAY_BUTTON = Button(START_BUTTON, ratiox=0.5, ratioy=0.4, game=game)
                    self.OPTIONS_BUTTON = Button(MENU_BUTTON, ratiox=0.5, ratioy=0.5, game=game)
                    self.QUIT_BUTTON = Button(EXIT_BUTTON, ratiox=0.5, ratioy=0.6, game=game)
                    self.BG = Main_Menu_BG

          def loop(self):
                    while True:
                              self.game.clock.tick(self.game.fps)

                              new_bg = pygame.transform.scale(self.BG, pygame.display.get_window_size())
                              self.game.display.blit(new_bg, (0, 0))

                              self.game.event_manager()
                              self.game.update_somethings()

                              if pygame.mouse.get_pressed()[0]:
                                        if self.PLAY_BUTTON.check_for_input(pygame.mouse.get_pos()): return True
                                        elif self.OPTIONS_BUTTON.check_for_input(pygame.mouse.get_pos()): self.game.settings.loop()
                                        elif self.QUIT_BUTTON.check_for_input(pygame.mouse.get_pos()): return False

                              for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
                                        button.update()
                                        button.update_pos(WIN_RES[0], WIN_RES[1])
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
