class Variables:
          def __init__(self, game):
                    self.game = game
                    self.game.changing_settings = False
                    self.game.immidiate_quit = False
                    self.game.in_menu = True
                    self.game.restart = False
                    self.game.running = True
                    self.game.game_time = 0
                    self.game.background_frame = 0
                    self.game.transition_frame = 0
                    self.game.playing_transition = False
                    self.game.fps = refresh_rate
                    self.game.stats = pd.DataFrame(columns=['Coins', 'Score', 'Enemies Killed', 'Difficulty'])