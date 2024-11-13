from _internal.Variables.Variables import *
from _internal.Utilities.Tools import *
import pygame

display = pygame.display.set_mode(WIN_RES, pygame.RESIZABLE)

BG_entities_gif = import_gif("Assets\\Backgrounds\\Background Entities", (12, 9))
Main_Menu_BG = load("Backgrounds\\Menu_BG.png", WIN_RES)
border = load("Backgrounds\\border.png", REN_RES)

Buttons = import_gif("Assets\\Misc\\Buttons", (REN_RES[0] * 300 / WIN_RES[0], REN_RES[1] * 80 / WIN_RES[1]))
Health_bar = load("Misc\\Bars\\health.png", BARS_RES)
Stamina_bar = load("Misc\\Bars\\Sprite-0005.png", BARS_RES)

Player_Running = import_SpriteSheet("Assets\\Entities\\Player\\AnimationSheet_Character.png", 0, 98, 32, 32, 8)
Player_Walking = import_SpriteSheet("Assets\\Entities\\Player\\AnimationSheet_Character.png", 0, 2 + 32 * 2, 32, 32, 4)
Player_Dying = import_SpriteSheet("Assets\\Entities\\Player\\AnimationSheet_Character.png", 0, 2 + 32 * 7, 32, 32, 8)
Player_Idle = import_SpriteSheet("Assets\\Entities\\Player\\AnimationSheet_Character.png", 0, 2 + 32 * 0, 32, 32, 2)
Player_Blinking = import_gif("Assets\\Entities\\Player\\AnimationSheet_Character_Blinking", 0, 2 + 32 * 1, 32, 32, 2)

Enemy_idle = import_gif("Assets\\Entities\\Enemy1")

Rifle = load("Objects\\Weapons\\rifle.png", None, (0, 0, 0))

cursor1 = load("Misc\\Mouse\\Mouse1\\03.png", MOUSE_RES, (255, 255, 255))
cursor2 = load("Misc\\Mouse\\Mouse1\\04.png", MOUSE_RES, (255, 255, 255))
cover = load("Misc\\Cover\\cover.png", None)
