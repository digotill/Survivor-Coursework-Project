from Code.Variables.SettingVariables import *
from Code.Individuals.Gun import *

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
                    self.game.playing_end_trantition = False  # Flag for end screen transition state
                    self.game.loaded_game = False    # Flag for whether a game has been loaded

                    self.game.assets = AM.assets  # Store game assets
                    self.game.methods = M  # Store game methods
                    self.game.render_resolution = RENRES  # Set render resolution

                    self.game.game_time = 0  # Initialize game time
                    self.game.difficulty = "medium"  # Set default difficulty
                    self.game.fps = 240  # Set frames per second
                    self.game.uiS.set_colorkey((0, 0, 0))  # Set UI surface transparency
                    self.game.player = None  # Initialize player object
                    self.game.reduced_screen_shake = 1
                    self.game.colour_mode = 50
                    self.game.master_volume = 1
                    self.game.text_size = 1
                    self.update_font_sizes()
                    self.update()  # Call update method

          def update_font_sizes(self):
                    self.game.assets["font8"] = pygame.font.Font("Assets/UI/fonts/font8.ttf", int(8 * self.game.text_size))
                    self.game.assets["font14"] = pygame.font.Font("Assets/UI/fonts/font14.ttf", int(14 * self.game.text_size))

          def update_rect(self):
                    self.game.drawing_rect = pygame.Rect(0, 0, self.game.display.width, self.game.display.height)

          def update(self):
                    # Update game state variables each frame
                    self.game.displayinfo = pygame.display.Info()
                    self.game.inputM.update()  # Update input manager
                    if self.game.clock.get_fps() != 0: self.game.dt = 1 / self.game.clock.get_fps()  # Calculate delta time
                    else: self.game.dt = 0
                    dt = min(self.game.dt, 1/20)
                    if not self.game.changing_settings and not self.game.in_menu: self.game.game_time += dt  # Update game time
                    self.game.ticks = pygame.time.get_ticks() / 1000  # Get current time in seconds
                    if self.game.ticks % 10 == 0: gc.collect()  # Perform garbage collection every 10 seconds
                    if self.game.player is not None and self.game.player.health <= 0: self.game.died = True  # Check for player death
                    if getattr(self.game, "interactablesM", None) is not None and self.game.interactablesM.grabbing_slider: self.update_font_sizes()  # Update font sizes
                    self.game.fullscreen = pygame.display.is_fullscreen()  # Flag for fullscreen mode
                    self.update_rect()
