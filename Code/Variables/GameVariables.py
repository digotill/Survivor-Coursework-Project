from Code.Variables.SettingsVariables import *

class GameVariables:
          def __init__(self, game):
                    self.game = game
                    self.game.changing_settings = False
                    self.game.immidiate_quit = False
                    self.game.gc_counter = 0
                    self.game.in_menu = True
                    self.game.restart = False
                    self.game.running = True
                    self.game.game_time = 0
                    self.game.playing_transition = False
                    self.game.fps = refresh_rate
                    self.game.assets = AM.assets
                    self.game.difficulty = "medium"
                    self.game.stats = pd.DataFrame(columns=['Coins', 'Level', 'Enemies Killed'])
                    self.game.ui_surface.set_colorkey((0, 0, 0))
                    self.update()

          def update(self):
                    # Update game state variables each frame
                    self.game.keys = pygame.key.get_pressed()
                    self.game.mouse_pos = (max(0, min(pygame.mouse.get_pos()[0], self.game.display.width)),
                                      max(0, min(pygame.mouse.get_pos()[1], self.game.display.height)))
                    self.game.correct_mouse_pos = (int(self.game.mouse_pos[0] * REN_RES[0] / self.game.display.width),
                                              int(self.game.mouse_pos[1] * REN_RES[1] / self.game.display.height))
                    if self.game.mouse_pos != pygame.mouse.get_pos():
                              pygame.mouse.set_pos(self.game.mouse_pos)
                    self.game.mouse_state = pygame.mouse.get_pressed()
                    if self.game.clock.get_fps() != 0:
                              self.game.dt = 1 / self.game.clock.get_fps()
                    else:
                              self.game.dt = 0
                    if not self.game.changing_settings and not self.game.in_menu:
                              self.game.game_time += self.game.dt
                    self.game.gc_counter += 1
                    if self.game.gc_counter % 100 == 0:
                              gc.collect()
