from Code.Classes.Managers import *
from Code.Display.EventManager import *
from Code.Display.Menu import *
from Code.Display.UI import *
from Code.Display.Window import *
from Code.Classes.TileMap import TileMap
from Code.Classes.GrassManager import *


class Game:
          def __init__(self):
                    pygame.init()

                    self.display = Display
                    self.display_screen = pygame.Surface(REN_RES).convert()
                    self.ui_surface = pygame.Surface(REN_RES).convert()
                    self.ui_surface.set_colorkey((0, 0, 0))
                    self.clock = pygame.time.Clock()

                    self.running = True
                    self.game_time = 0
                    self.fps = AllButtons["Sliders"]["fps"]["value"]
                    self.dt = 0
                    self.changing_settings = False
                    self.immidiate_quit = False
                    self.in_menu = True
                    self.restart = False
                    self.stats = pd.DataFrame(columns=['Coins', 'Score', 'Enemies Killed', 'Difficulty'])

                    self.event_manager = EventManager(self)
                    self.enemy_manager = EnemyManager(self)
                    self.particle_manager = ParticleManager(self)
                    self.object_manager = ObjectManager(self)
                    self.bullet_manager = BulletManager(self)
                    self.button_manager = ButtonManager(self)
                    self.sound_manager = SoundManager(self)
                    self.grass_manager = GrassManager(self)

                    self.ui = UI(self)
                    self.window = Window(self)
                    self.tilemap = TileMap(self)

                    self.update_game_variables()

                    self.mainmenu = MainMenu(self)
                    self.gameover = GameOver(self)
                    self.mainmenu.loop()

          def refresh(self):
                    self.__init__()
                    pygame.display.flip()
                    self.run_game()

          def update_groups(self):
                    if not self.changing_settings:
                              self.enemy_manager.update_enemies()
                              self.particle_manager.update()
                              self.bullet_manager.update()
                              self.object_manager.update()
                    self.player.update()
                    self.player.gun.update()
                    self.button_manager.update_buttons()

          def draw_groups(self):
                    self.tilemap.draw()
                    self.grass_manager.draw()
                    self.player.draw()
                    self.player.gun.draw()
                    self.enemy_manager.draw_enemies()
                    self.object_manager.draw()
                    self.bullet_manager.draw()
                    self.particle_manager.draw()
                    self.ui.darken_screen()
                    self.ui.draw_bars()
                    self.ui.draw_fps()
                    self.ui.draw_time()
                    self.button_manager.draw_buttons()

          def update_display(self):
                    self.display_screen.blit(self.ui_surface)
                    self.ui_surface.fill((0, 0, 0, 0))
                    self.display.blit(pygame.transform.scale(self.display_screen, self.display.size))
                    self.ui.display_mouse()
                    self.ui.draw_brightness()
                    pygame.display.flip()

          def manage_events(self):
                    self.event_manager.handle_events()
                    self.event_manager.update_size()
                    self.event_manager.update_grab()
                    if not self.in_menu:
                              self.event_manager.update_changing_settings()
                              self.event_manager.update_fps_toggle()

          def update_game_variables(self):
                    self.keys = pygame.key.get_pressed()
                    self.mouse_pos = pygame.mouse.get_pos()
                    self.window_ratio = REN_RES[0] / self.display.width
                    self.correct_mouse_pos = (int(self.mouse_pos[0] * self.window_ratio),
                                              int(self.mouse_pos[1] * self.window_ratio))
                    self.mouse_state = pygame.mouse.get_pressed()
                    if not self.changing_settings:
                              self.game_time += self.dt
                    if self.clock.get_fps() == 0:
                              fps = 200
                    else:
                              fps = self.clock.get_fps()
                    self.dt = 1 / fps

          def run_game(self):
                    while self.running:
                              self.clock.tick_busy_loop(self.fps)
                              self.update_game_variables()
                              self.manage_events()
                              self.update_groups()
                              self.draw_groups()
                              self.update_display()
                              if self.restart: self.refresh()
                              if self.immidiate_quit: return None
                    pygame.quit()
