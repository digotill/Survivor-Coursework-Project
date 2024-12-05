from Code.Variables.Variables import *
from Code.Utilities.Utils import *
import pygame

display = pygame.display.set_mode(WIN_RES, pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.display.set_icon(load_image("Assets/Misc/Cover/cover.png"))
pygame.display.set_caption("Vampire Survivor")


Green_Waterfall = cached_import_gif("Assets/LoadingScreens/1", WIN_RES)
Orange_Pond = cached_import_gif("Assets/LoadingScreens/2", WIN_RES)


Player_Running = cached_import_gif("Assets/Entities/Player/new player/idle", player_attributes['res'])
Enemy_idle = cached_import_gif("Assets/Entities/Enemy1", enemy_attributes["res"])


Grass_Tile = load_image("Assets/Misc/Grass/grass.png", (window_attributes['tilemap_size'], window_attributes['tilemap_size']))
Cursor_Clicking = load_image("Assets/Misc/Mouse/Mouse3/Sprite-0002.png", general_settings['mouse_res'])
Cursor_Not_Clicking = load_image("Assets/Misc/Mouse/Mouse3/Sprite-0001.png", general_settings['mouse_res'])
Buttons = cached_import_gif("Assets/Misc/Buttons")
Health_bar = load_image("Assets/Misc/Bars/health.png")
Stamina_bar = load_image("Assets/Misc/Bars/Sprite-0005.png")
Outside_Health_bar = load_image("Assets/Misc/Bars/health_bar.png", ui["outside_bar_res"])


Slash_Effect = cached_import_gif("Assets/VFX/Slash")

AK_47 = load_image("Assets/Objects/Weapons/rifle.png", weapons['AK47']['res'])
Shotgun = load_image("Assets/Objects/Weapons/Shotgun.png", weapons['Shotgun']['res'])
Minigun = load_image("Assets/Objects/Weapons/Mini gun.png", weapons['Minigun']['res'])
Bullets = load_image("Assets/Objects/Bullet/Bullet 1/Bullet.png")
