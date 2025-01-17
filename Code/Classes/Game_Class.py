from Code.Classes.Managers import *
from Code.Display.EventManager import *
from Code.Display.Menu import *
from Code.Display.UIManager import *
from Code.Display.Camera import *
from Code.Classes.TileMapManager import TileMapManager
from Code.Classes.GrassManager import *
from Code.Variables.AssetManager import *
from Code.Shaders import pygame_shaders
from memory_profiler import profile


class Game:
          def __init__(self):
                    # Initialize Pygame
                    pygame.init()

                    # Set up display and rendering surfaces
                    self.display = DISPLAY
                    self.display_screen = pygame.Surface(REN_RES).convert()
                    # Initialize shader for post-processing effects
                    self.shader = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER,
                                                        pygame_shaders.DEFAULT_FRAGMENT_SHADER, self.display_screen)

                    # Create a separate surface for UI elements
                    self.ui_surface = pygame.Surface(REN_RES).convert()
                    self.ui_surface.set_colorkey((0, 0, 0))  # Set black as transparent for UI surface
                    
                    # Initialize clock for managing frame rate
                    self.clock = pygame.time.Clock()

                    # Game state variables
                    self.running = True
                    self.game_time = 0
                    self.fps = refresh_rate
                    self.assets = AM.assets
                    self.changing_settings = False
                    self.immidiate_quit = False
                    self.in_menu = True
                    self.restart = False
                    
                    # Initialize DataFrame for storing game statistics
                    self.stats = pd.DataFrame(columns=['Coins', 'Score', 'Enemies Killed', 'Difficulty'])

                    # Initialize various game managers
                    self.event_manager = EventManager(self)
                    self.enemy_manager = EnemyManager(self)
                    self.particle_manager = ParticleManager(self)
                    self.bullet_manager = BulletManager(self)
                    self.button_manager = ButtonManager(self)
                    self.sound_manager = SoundManager(self)
                    self.grass_manager = GrassManager(self)
                    self.rain_manager = RainManager(self)
                    self.ui_manager = UIManager(self)
                    self.drawing_manager = DrawingManager(self)

                    #Generate tilemap and objects
                    self.tilemap = TileMapManager(self)
                    self.object_manager = ObjectManager(self)

                    # Update initial game variables
                    self.update_game_variables()

                    # Initialize and run the main menu
                    self.mainmenu = MainMenu(self)

                    # Initialize camera
                    self.camera = Camera(self)

                    self.run_game()

          def refresh(self):
                    # Refresh the display and restart the game
                    pygame.display.flip()
                    self.__init__()
                    self.run_game()

          def update_groups(self):
                    # Update game entities and managers
                    if not self.changing_settings:
                              self.enemy_manager.update()
                              self.particle_manager.update()
                              self.bullet_manager.update()
                              self.rain_manager.update()
                    self.player.update()
                    self.player.gun.update()
                    self.button_manager.update()

          def draw_groups(self):
                    # Draw game elements in order
                    self.tilemap.draw()
                    self.grass_manager.update()
                    self.drawing_manager.draw()
                    self.bullet_manager.draw()
                    self.particle_manager.draw()
                    self.rain_manager.draw()
                    self.ui_manager.darken_screen()
                    self.ui_manager.draw_bars()
                    self.ui_manager.draw_fps()
                    self.ui_manager.draw_time()
                    self.button_manager.draw()

          def update_display(self):
                    # Update the display with all drawn elements
                    self.ui_manager.display_mouse()
                    self.display_screen.blit(self.ui_surface, (0, 0))
                    self.ui_surface.fill((0, 0, 0, 0))
                    self.ui_manager.draw_brightness()
                    self.shader.render_direct(pygame.Rect(0, 0, self.display.width, self.display.height))
                    pygame.display.flip()

          def manage_events(self):
                    # Handle various game events
                    self.event_manager.handle_quitting()
                    self.event_manager.update_grab()
                    self.event_manager.fullscreen_toggle()
                    if not self.in_menu:
                              self.event_manager.update_changing_settings()
                              self.event_manager.update_fps_toggle()

          def update_game_variables(self):
                    # Update game state variables each frame
                    self.keys = pygame.key.get_pressed()
                    self.mouse_pos = (max(0, min(pygame.mouse.get_pos()[0], self.display.width)),
                                      max(0, min(pygame.mouse.get_pos()[1], self.display.height)))
                    self.correct_mouse_pos = (int(self.mouse_pos[0] * REN_RES[0] / self.display.width),
                                              int(self.mouse_pos[1] * REN_RES[1] / self.display.height))
                    if self.mouse_pos != pygame.mouse.get_pos():
                              pygame.mouse.set_pos(self.mouse_pos)
                    self.mouse_state = pygame.mouse.get_pressed()
                    if self.clock.get_fps() != 0: self.dt = 1 / self.clock.get_fps()
                    else: self.dt = 0
                    if not self.changing_settings:
                              self.game_time += self.dt

          #@profile
          def run_game(self):
                    # Main game loop
                    while self.running:
                              self.clock.tick_busy_loop(self.fps)
                              self.update_game_variables()
                              self.manage_events()
                              self.update_groups()
                              self.draw_groups()
                              self.update_display()
                              if self.restart: self.refresh()
                              elif self.immidiate_quit: return None
