from Code.Variables.SettingVariables import *


class GameVariables:
          def __init__(self, game):
                    self.game = game  # Store reference to the game object

                    self.game.changing_settings = False  # Flag for settings change state
                    self.game.immidiate_quit = False  # Flag for immediate game quit
                    self.game.in_menu = True  # Flag for menu state
                    self.game.restart = False  # Flag for game restart
                    self.game.running = True  # Flag for game running state
                    self.game.died = False  # Flag for player death
                    self.game.playing_transition = False  # Flag for transition state

                    self.game.assets = AM.assets  # Store game assets
                    self.game.methods = M  # Store game methods
                    self.game.render_resolution = RENRES  # Set render resolution

                    self.game.game_time = 0  # Initialize game time
                    self.game.difficulty = "medium"  # Set default difficulty
                    self.game.fps = HZ  # Set frames per second
                    self.game.stats = pd.DataFrame(columns=['Coins', 'Level', 'Enemies Killed'])  # Initialize stats
                    self.game.uiS.set_colorkey((0, 0, 0))  # Set UI surface transparency
                    self.game.player = None  # Initialize player object

                    self.game.reduced_screen_shake = 1

                    self.game.colour_mode = 50


                    self.update()  # Call update method

          def update(self):
                    # Update game state variables each frame
                    self.game.inputM.update()  # Update input manager
                    self.game.keys = pygame.key.get_pressed()  # Get current keyboard state
                    self.game.mouse_pos = (max(0, min(pygame.mouse.get_pos()[0], self.game.display.width)),
                                           max(0, min(pygame.mouse.get_pos()[1], self.game.display.height)))  # Get clamped mouse position
                    self.game.correct_mouse_pos = (int(self.game.mouse_pos[0] * self.game.render_resolution[0] / self.game.display.width),
                                                   int(self.game.mouse_pos[1] * self.game.render_resolution[1] / self.game.display.height))  # Calculate corrected mouse position
                    if self.game.mouse_pos != pygame.mouse.get_pos(): pygame.mouse.set_pos(self.game.mouse_pos)  # Update mouse position if changed
                    self.game.mouse_state = pygame.mouse.get_pressed()  # Get current mouse button state
                    if self.game.clock.get_fps() != 0:
                              self.game.dt = 1 / self.game.clock.get_fps()  # Calculate delta time
                    else:
                              self.game.dt = 0
                    if not self.game.changing_settings and not self.game.in_menu: self.game.game_time += self.game.dt  # Update game time
                    self.game.ticks = pygame.time.get_ticks() / 1000  # Get current time in seconds
                    if self.game.ticks % 10 == 0: gc.collect()  # Perform garbage collection every 10 seconds
                    if self.game.player is not None and self.game.player.health <= 0: self.game.died = True  # Check for player death
