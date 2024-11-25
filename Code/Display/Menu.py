from Code.Classes.Buttons import *
from Code.Variables.Initialize import *
import random


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.PLAY_BUTTON = Button(Buttons[0], PLAY_BUTTON_POS, game, True, PLAY_BUTTON_NAME, FONT,
                                              PLAY_BUTTON_BASE_COLOUR, PLAY_BUTTON_HOVERING_COLOUR)
                    self.QUIT_BUTTON = Button(Buttons[2], QUIT_BUTTON_POS, game,  True, QUIT_BUTTON_NAME, FONT,
                                              QUIT_BUTTON_BASE_COLOUR, QUIT_BUTTON_HOVERING_COLOUR)
                    self.buttons = [self.PLAY_BUTTON, self.QUIT_BUTTON]
                    for button in self.buttons:
                              button.active = True
                    self.BG = Main_Menu_BG
                    self.loading_screen = loading_screen_1 if random.random() < 0.5 else loading_screen_2
                    self.current_frame = 0

          def loop(self):
                    while True:
                              self.game.clock.tick(self.game.fps)
                              if self.game.display.size != WIN_RES:
                                        self.game.display.blit(pygame.transform.scale(self.loading_screen[int(self.current_frame) % len(self.loading_screen)], self.game.display.size))
                              else: self.game.display.blit(self.loading_screen[int(self.current_frame) % len(self.loading_screen)])
                              self.current_frame += ANIMATION_SPEED * self.game.dt * 3

                              self.game.event_manager()
                              self.game.update_game_variables()

                              for button in self.buttons:
                                        button.draw()
                                        button.update_pos()
                                        button.changeColor(self.game.mouse_pos)

                              if pygame.mouse.get_pressed()[0]:
                                        if self.PLAY_BUTTON.check_for_input(self.game.mouse_pos): return True
                                        elif self.QUIT_BUTTON.check_for_input(self.game.mouse_pos): return False

                              self.game.ui.display_mouse()

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
