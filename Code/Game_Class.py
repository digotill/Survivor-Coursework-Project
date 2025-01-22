from Code.Variables.SettingsVariables import *
from Code.Managers import *
from Code.Variables.GameVariables import *
from Code.Variables.LoadAssets import *
from Code.Individuals.Player import *


class Game:
          def __init__(self):
                    # Initialize Pygame
                    pygame.init()

                    # Set up display and rendering surfaces
                    self.display = DISPLAY
                    self.display_surface = pygame.Surface(REN_RES).convert()
                    self.ui_surface = pygame.Surface(REN_RES).convert()
                    self.shader = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER,
                                                        pygame_shaders.DEFAULT_FRAGMENT_SHADER, self.display_surface)

                    # Initialize clock for managing frame rate
                    self.clock = pygame.time.Clock()
                    self.game_variables = GameVariables(self)

                    # Initialize various game managers
                    self.event_manager = EventManager(self)
                    self.enemy_manager = EnemyManager(self)
                    self.spark_manager = SparkManager(self)
                    self.bullet_manager = BulletManager(self)
                    self.sound_manager = SoundManager(self)
                    self.rain_manager = RainManager(self)
                    self.button_manager = ButtonManager(self)
                    self.ui_manager = UIManager(self)
                    self.drawing_manager = DrawingManager(self)
                    self.grass_manager = GrassManager(self)
                    self.tilemap_manager = TileMapManager(self)
                    self.object_manager = ObjectManager(self)
                    self.screen_effect_manager = ScreenEffectManager(self)
                    self.background_manager = BackgroundManager(self)

                    self.player = Player(self)
                    self.camera = CameraManager(self)

                    # Initialize and run the main menu
                    self.run_game()

          def refresh(self):
                    # Refresh the display and restart the game
                    pygame.display.flip()
                    self.__init__()

          def update_groups(self):
                    # Update game entities and managers
                    if not self.in_menu:
                              for manager in [self.enemy_manager, self.spark_manager, self.bullet_manager,
                                              self.rain_manager, self.player, self.player.gun, self.button_manager]:
                                        manager.update()
                    elif self.in_menu:
                              for manager in [self.button_manager]:
                                        manager.update()

          def draw_groups(self):
                    # Draw game elements in order
                    if not self.in_menu:
                              self.tilemap_manager.draw()
                              self.grass_manager.draw()
                              self.drawing_manager.draw()
                              self.bullet_manager.draw()
                              self.spark_manager.draw()
                              self.rain_manager.draw()
                              self.ui_manager.draw()
                              self.button_manager.draw()
                              self.screen_effect_manager.draw()
                    elif self.in_menu:
                              for manager in [self.background_manager, self.button_manager, self.screen_effect_manager]:
                                        manager.draw()

          def update_display(self):
                    # Update the display with all drawn elements
                    self.ui_manager.update_display()
                    self.shader.render_direct(pygame.Rect(0, 0, self.display.width, self.display.height))
                    pygame.display.flip()

          def run_game(self):
                    # Main game loop
                    while self.running:
                              self.clock.tick_busy_loop(self.fps)
                              self.game_variables.update()
                              self.event_manager.handle_events()
                              self.update_groups()
                              self.draw_groups()
                              self.update_display()
                              if self.restart:
                                        self.refresh()
