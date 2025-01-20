from Code.Individuals.Player import *
from Code.Individuals.Buttons import *
from Code.Individuals.Gun import *


class MainMenu:
          def __init__(self, game):
                    self.game = game
                    self.background_frame = 0
                    self.transition_frame = 0
                    self.loop()


          def loop(self):
                    while self.game.in_menu and self.game.running:
                              self.game.clock.tick(self.game.fps)
                              self.game.manage_events()
                              self.game.game_variables.update()

                              self.draw_background()
                              self.game.button_manager.update()
                              self.game.button_manager.draw()
                              self.draw_transition()

                              self.game.update_display()

                    self.update()

          def update(self):
                    new_stat = pd.DataFrame({'Coins': [0], 'Score': [0], 'Enemies Killed': [0]})
                    self.game.stats = pd.concat([self.game.stats, new_stat], ignore_index=True)

          def draw_background(self):
                    frame = int(self.background_frame) % len(self.game.assets["main_menu"])
                    self.game.display_screen.blit(self.game.assets["main_menu"][frame])
                    self.background_frame += self.game.dt * General_Settings['animation_speeds'][0]

          def draw_transition(self):
                    if self.game.playing_transition:
                              frame = int(self.transition_frame) % len(self.game.assets["transition_screeneffect"])
                              self.game.ui_surface.blit(self.game.assets["transition_screeneffect"][frame])
                              self.transition_frame += self.game.dt * General_Settings['animation_speeds'][1]
                              if self.transition_frame > len(self.game.assets["transition_screeneffect"]) - 1:
                                        self.game.in_menu = False
