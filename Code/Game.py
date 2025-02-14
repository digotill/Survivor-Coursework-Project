from Code.Variables.SettingVariables import *
from Code.Managers import *
from Code.Shaders import *
from Code.Variables.GameVariables import *
from Code.Variables.LoadAssets import *
from Code.Individuals.Player import *
from Code.Managers.InputManager import *
from Code.Variables.Data import *

class Game:
          def __init__(self):

                    # Set up display and rendering surfaces
                    self.display = DISPLAY
                    self.displayS = pygame.Surface(RENRES).convert()
                    self.uiS = pygame.Surface(RENRES).convert()
                    self.shader = Shader(DEFAULT_VERTEX_SHADER, DEFAULT_FRAGMENT_SHADER, self.displayS)

                    # Initialize clock for managing frame rate
                    self.clock = pygame.time.Clock()
                    self.inputM = InputManager(self)
                    self.gameV = GameVariables(self)

                    # Initialize various game managers
                    self.eventM = EventManager(self)
                    self.enemyM = EnemyManager(self)
                    self.sparkM = SparkManager(self)
                    self.bulletM = BulletManager(self)
                    self.effectM = EffectManager(self)
                    self.rainM = RainManager(self)
                    self.interactablesM = InteractablesManager(self)
                    self.uiM = UIManager(self)
                    self.drawingM = DrawingManager(self)
                    self.grassM = GrassManager(self)
                    self.tilemapM = TileMapManager(self)
                    self.objectM = ObjectManager(self)
                    self.screeneffectM = ScreenEffectManager(self)
                    self.backgroundM = BackgroundManager(self)
                    self.experienceM = ExperienceManager(self)

                    self.player = Player(self)
                    self.cameraM = CameraManager(self)

                    self.soundM = SoundManager(self)

                    self.data = Data(self)
                    self.data.load_data()

          def refresh(self):
                    # Refresh the display and restart the game
                    pygame.display.flip()
                    self.__init__()
                    self.screeneffectM.set_transition_to_play()
                    self.run_game()

          def update_managers(self):
                    # Update game entities and managers
                    if not self.in_menu:
                              for manager in [self.enemyM, self.sparkM, self.bulletM, self.experienceM, self.rainM, self.player, self.effectM, self.cameraM]:
                                        manager.update()
                    self.interactablesM.update()
                    self.soundM.update()

          def draw_managers(self):
                    # Draw game elements in order
                    if not self.in_menu:
                              for manager in [self.tilemapM, self.effectM, self.drawingM, self.rainM, self.uiM]:
                                        manager.draw()
                    for manager in [self.backgroundM, self.interactablesM, self.screeneffectM]:
                              manager.draw()

          def update_display(self):
                    # Update the display with all drawn elements
                    self.uiM.update_display()
                    self.shader.render_direct(self.drawing_rect)
                    pygame.display.flip()

          def run_game(self):
                    self.soundM.play_music(self.assets["menu_music"])
                    # Main game loop
                    while self.running:
                              self.clock.tick_busy_loop(self.fps)
                              self.gameV.update()
                              self.eventM.handle_events()
                              self.update_managers()
                              self.draw_managers()
                              self.update_display()
                              if self.restart:
                                        self.data.save_data()
                                        self.refresh()
                    self.data.save_data()
