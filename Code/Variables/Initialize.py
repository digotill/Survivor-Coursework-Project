from Code.Variables.Variables import *
from Code.Utilities.Utils import *
import pygame

display = pygame.display.set_mode(WIN_RES, pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.display.set_icon(load_image("Assets/Misc/Cover/cover.png"))
pygame.display.set_caption("Vampire Survivor")

BG_entities_gif = cached_import_gif("Assets/Backgrounds/Background Entities", BG_ENTITIES_RES)
loading_screen_1 = cached_import_gif("Assets/LoadingScreens/1", WIN_RES)
loading_screen_2 = cached_import_gif("Assets/LoadingScreens/2", WIN_RES)
Buttons = cached_import_gif("Assets/Misc/Buttons")
Health_bar = load_image("Assets/Misc/Bars/health.png")
Stamina_bar = load_image("Assets/Misc/Bars/Sprite-0005.png")
Outside_Health_bar = load_image("Assets/Misc/Bars/health_bar.png", None, (0, 0, 0))
Player_Running = cached_import_gif("Assets/Entities/Player/new player/idle", PLAYER_RES)
Enemy_idle = cached_import_gif("Assets/Entities/Enemy1", ENEMY_RES)
Slash_Effect = cached_import_gif("Assets/VFX/Slash", )
grass = load_image("Assets/Misc/Grass/grass.png", BG_ENTITIES_RES)
AK_47 = load_image("Assets/Objects/Weapons/rifle.png", AK47_RES, (0, 0, 0))
AK_47_Bullet = load_image("Assets/Objects/Bullet/Bullet 1/Bullet.png")
Minigun = load_image("Assets/Objects/Weapons/Mini gun.png", MINIGUN_RES)
cursor1 = load_image("Assets/Misc/Mouse/Mouse3/Sprite-0002.png", MOUSE_RES)
cursor2 = load_image("Assets/Misc/Mouse/Mouse3/Sprite-0001.png", MOUSE_RES,)
