import pygame, time, math
from _internal.Variables.Variables import *
from _internal.Classes.Managers import *
from _internal.Utilities.Grid import *
from _internal.Display.Effects import *
from _internal.Classes.Entities import *
from _internal.Variables.Initialize import *
from _internal.Display.Window import *
from _internal.Display.Menu import *
from _internal.Classes.Button_Class import *
from _internal.Display.Event_Manager import *


class Game:
          def __init__(self):
                    pygame.init()
                    pygame.mixer.init()
                    self.display = pygame.display.set_mode(WIN_RES, pygame.RESIZABLE)
                    self.display_screen = pygame.Surface(REN_RES).convert()
                    self.clock = pygame.time.Clock()

                    self.settings = Settings(self)
                    self.mainmenu = MainMenu(self)
                    self.game_over = GameOver(self)

                    self.enemy_manager = EnemyManager(self)
                    self.particle_manager = ParticleManager(self)
                    self.object_manager = ObjectManager(self)
                    self.bullet_manager = BulletManager(self)
                    self.sound_manager = SoundManager(self)

                    self.background = BackgroundAndHud(self)

                    self.small_window = Window(self, REN_RES, PLAYABLE_AREA)
                    self.big_window = PLAYABLE_AREA

                    self.BG_entities = BG_Entities_Manager(self)

                    self.player = Player(self, PLAYER_HEALTH, PLAYER_RES, PLAYER_VEL, PLAYER_DAMAGE, (self.small_window.rect.centerx,
                                                            self.small_window.rect.centery), PLAYER_NAME, Player_Running)

                    self.running = True
                    self.game_time = 0
                    self.fps = FPS
                    self.dt = 0

                    self.mouse_pos = pygame.mouse.get_pos()
                    self.correct_mouse_pos = pygame.mouse.get_pos()
                    self.mouse_state = pygame.mouse.get_pressed()
                    self.keys = pygame.key.get_pressed()

                    self.event_manager_class = Event_Manager(self)

                    pygame.display.set_caption(GAME_NAME)
                    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
                    pygame.display.set_icon(cover)

          def refresh(self):
                    self.__init__()
                    pygame.display.flip()
                    self.run_game()

          def display_mouse(self):
                    if pygame.mouse.get_focused():
                              if self.mouse_state[0]: self.display.blit(cursor1, (self.mouse_pos[0], self.mouse_pos[1]))
                              else: self.display.blit(cursor2, (self.mouse_pos[0], self.mouse_pos[1]))

          def update_groups(self):
                    self.enemy_manager.update_enemies()
                    self.object_manager.update()
                    self.player.update()
                    self.particle_manager.update_particles()
                    self.bullet_manager.update()
                    self.background.update()
                    self.game_over.update()
                    self.update_somethings()

          def draw_groups(self):
                    self.display_screen.fill(BG_COLOUR)
                    self.BG_entities.draw()
                    self.player.blit()
                    self.player.gun.draw()
                    self.enemy_manager.draw_enemies()
                    self.object_manager.draw()
                    self.bullet_manager.draw()
                    self.particle_manager.draw_particles()
                    self.background.draw_border()
                    self.background.draw_bars()
                    self.background.draw_fps()
                    self.background.draw_time()

          def event_manager(self):
                    self.event_manager_class.update_window_events()
                    self.event_manager_class.update_size()
                    self.event_manager_class.update_fps_toggle()
                    self.event_manager_class.update_grab()

          def update_somethings(self):
                    self.keys = pygame.key.get_pressed()
                    self.mouse_pos = pygame.mouse.get_pos()
                    self.correct_mouse_pos = int(self.mouse_pos[0] * REN_RES[0] / self.display.width), int(self.mouse_pos[1] * REN_RES[1] / self.display.height)
                    self.mouse_state = pygame.mouse.get_pressed()
                    self.game_time = pygame.time.get_ticks() / 1000

          def run_game(self):
                    main_menu = self.mainmenu.loop()
                    prev_time = time.time()
                    if main_menu is False: return None
                    while self.running:
                              self.clock.tick(self.fps)
                              now = time.time()
                              self.dt = now - prev_time
                              prev_time = now
                              self.event_manager()
                              self.small_window.move()
                              self.update_groups()
                              self.draw_groups()
                              self.display.blit(pygame.transform.scale(self.display_screen, self.display.size))
                              self.game_time = pygame.time.get_ticks()
                              self.display_mouse()
                              if self.player.health < 0: self.running = False
                              if self.running: pygame.display.flip()
                    pygame.quit()


if __name__ == "__main__":
          game = Game()
          game.run_game()
