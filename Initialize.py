from Variables import *
from Tools import *
import pygame

display = pygame.display.set_mode(WIN_RES, pygame.RESIZABLE)

BG_entities_gif = import_gif("Assets\\Backgrounds\\Background Entities", (12, 9))
Main_Menu_BG = load("Backgrounds\\Menu_BG.png", WIN_RES)
border = load("Backgrounds\\border.png", REN_RES)

Buttons = import_gif("Assets\\Misc\\Buttons", (REN_RES[0] * 300 / WIN_RES[0], REN_RES[1] * 80 / WIN_RES[1]))
Health_bar = load("Misc\\Bars\\health.png", BARS_RES)
Stamina_bar = load("Misc\\Bars\\Sprite-0005.png", BARS_RES)

Player_run = import_gif("Assets\\Entities\\Player\\Run")
Player_idle = import_gif("Assets\\Entities\\Player\\Idle")
Player_hit = import_gif("Assets\\Entities\\Player\\Hit")

Pink_Monster = import_SpriteSheet("Assets\\Entities\\Player\\1 Pink_Monster\\Pink_Monster_Run_6.png", 0, 0, 32, 32, 6)

Enemy_idle = import_gif("Assets\\Entities\\Enemy1")

Rifle = load("Objects\\Weapons\\rifle.png", None, (0, 0, 0))

cursor1 = load("Misc\\Mouse\\Mouse1\\03.png", MOUSE_RES, (255, 255, 255))
cursor2 = load("Misc\\Mouse\\Mouse1\\04.png", MOUSE_RES, (255, 255, 255))
cover = load("Misc\\Cover\\cover.png", None)
