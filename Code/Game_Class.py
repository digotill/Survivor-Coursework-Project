from Code.Variables.SettingsVariables import *
from Code.Managers import *
from Code.Variables.GameVariables import *
from Code.Menus import *
from Code.Variables.LoadAssets import *


class Game:
          def __init__(self):
                    # Initialize Pygame
                    pygame.init()

                    # Set up display and rendering surfaces
                    self.display = DISPLAY
                    self.display_screen = pygame.Surface(REN_RES).convert()
                    self.ui_surface = pygame.Surface(REN_RES).convert()
                    self.shader = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, pygame_shaders.DEFAULT_FRAGMENT_SHADER, self.display_screen)

                    # Initialize clock for managing frame rate
                    self.clock = pygame.time.Clock()
                    self.game_variables = GameVariables(self)

                    # Initialize various game managers
                    self.event_manager = EventManager(self)
                    self.enemy_manager = EnemyManager(self)
                    self.particle_manager = SparkManager(self)
                    self.bullet_manager = BulletManager(self)
                    self.sound_manager = SoundManager(self)
                    self.grass_manager = GrassManager(self)
                    self.rain_manager = RainManager(self)
                    self.button_manager = ButtonManager(self)
                    self.ui_manager = UIManager(self)
                    self.drawing_manager = DrawingManager(self)
                    self.tilemap = TileMapManager(self)
                    self.object_manager = ObjectManager(self)

                    self.player = Player(self, Player_Attributes)
                    self.camera = CameraManager(self)

                    # Initialize and run the main menu
                    self.mainmenu = MainMenu(self)
                    self.run_game()

          def refresh(self):
                    # Refresh the display and restart the game
                    pygame.display.flip()
                    self.__init__()

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
                    self.ui_manager.draw()
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

          #@profile
          def run_game(self):
                    # Main game loop
                    while self.running:
                              self.clock.tick_busy_loop(self.fps)
                              self.game_variables.update()
                              self.manage_events()
                              self.update_groups()
                              self.draw_groups()
                              self.update_display()
                              if self.restart:
                                        self.refresh()
                              elif self.immidiate_quit:
                                        return None
