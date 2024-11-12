import pygame, time, math
from Variables import *
from Managers import *
from Grid import *
from Effects import *
from Entities import *
from Initialize import *
from Window import *
from Menu import *
from Button_Class import *


class Game:
          def __init__(self):
                    pygame.init()
                    pygame.mixer.init()
                    self.display = pygame.display.set_mode(WIN_RES, pygame.RESIZABLE)
                    self.screen = pygame.Surface(REN_RES).convert()
                    self.display_screen = pygame.Surface(REN_RES).convert()
                    self.display_screen.set_colorkey((0, 0, 0))
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

                    self.grids = Grids(self)

                    self.small_window = Window(self, REN_RES, BIG_RES)
                    self.big_window = BIG_RES

                    self.BG_entities = BG_entities_manager(self, NUMBER_OF_BG_ENTITIES)

                    self.player = Player(self, PLAYER_HEALTH, PLAYER_RES, PLAYER_VEL, PLAYER_DAMAGE,
                                         (self.small_window.rect.centerx, self.small_window.rect.centery), PLAYER_NAME, Player_run)
                    self.gun = Gun(self, Rifle, PLAYER_GUN_RES, PLAYER_GUN_DISTANCE)

                    self.running = True
                    self.game_time = None
                    self.fps = FPS_WIN
                    self.dt = 0
                    self.sound = None
                    self.fullscreen = False
                    self.mouse_pos = pygame.mouse.get_pos()
                    self.mouse_state = pygame.mouse.get_pressed()
                    self.keys = pygame.key.get_pressed()
                    self.Last_Resize = 0

                    pygame.display.set_caption(GAME_NAME)
                    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
                    pygame.display.set_icon(pygame.image.load("cover\\cover.png").convert())

          def refresh(self):
                    pygame.mixer.Sound.stop(self.sound)
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
                    self.screen.fill(BG_COLOUR)
                    self.BG_entities.draw()
                    self.player.blit()
                    self.gun.draw()
                    self.enemy_manager.draw_enemies()
                    self.object_manager.draw()
                    self.bullet_manager.draw()
                    self.particle_manager.draw_particles()
                    self.background.draw()

          def event_manager(self):
                    for event in pygame.event.get():
                              if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]: self.running = False
                    if self.keys[pygame.K_F11] and self.Last_Resize + FULLSCREEN_COOLDOWN < time.time():
                              self.fullscreen = not self.fullscreen
                              if self.fullscreen:
                                        pygame.display.set_window_position((0, 0))
                                        self.display = pygame.display.set_mode(MAX_WIN_RES, pygame.NOFRAME)
                              else:
                                        pygame.display.set_window_position((MAX_WIN_RES[0] / 2 - REN_RES[0] / 2, MAX_WIN_RES[1] / 2 - REN_RES[1] / 2))
                                        self.display = pygame.display.set_mode(REN_RES, pygame.RESIZABLE)
                              self.Last_Resize = time.time()

          def update_somethings(self):
                    self.keys = pygame.key.get_pressed()
                    self.mouse_pos = pygame.mouse.get_pos()
                    self.mouse_state = pygame.mouse.get_pressed()

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
                              if self.running: pygame.display.flip()
                    pygame.quit()


if __name__ == "__main__":
          game = Game()
          game.run_game()