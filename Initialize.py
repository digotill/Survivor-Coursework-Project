from Variables import *
from Tools import *
import pygame

display = pygame.display.set_mode(WIN_RES, pygame.RESIZABLE)

BG_entities_gif = import_gif("BG_entities", (12, 9))
Main_Menu_BG = pygame.transform.scale(pygame.image.load("Still BG\\Menu_BG.png").convert(), WIN_RES)
border = pygame.transform.scale(pygame.image.load("BG\\border.png").convert_alpha(), REN_RES)

Buttons = import_gif("Buttons Bar", (REN_RES[0] * 300 / WIN_RES[0], REN_RES[1] * 80 / WIN_RES[1]))

Health_bar = pygame.transform.scale(pygame.image.load("Health Bar\\health.png").convert_alpha(), (300, 90))
Stamina_bar = pygame.transform.scale(pygame.image.load("Health Bar\\Sprite-0005.png").convert_alpha(), (300, 90))

Player_run = import_gif("Player\\Run")
Player_idle = import_gif("Player\\Idle")
Player_hit = import_gif("Player\\Hit")

Enemy_idle = import_gif("Enemy1\\Idle")

Glock_bullet = pygame.image.load("Weapons\\01 - Individual sprites\\Bullets & Ammo\\Glock - P80\\Bullet.png").convert_alpha()
Rifle = pygame.image.load("Weapons\\rifle.png").convert_alpha()

cursor1 = pygame.transform.scale(pygame.image.load("cursor\\03.png").convert(), (MOUSE_WIDTH, MOUSE_HEIGHT))
cursor1.set_colorkey((255, 255, 255))
cursor2 = pygame.transform.scale(pygame.image.load("cursor\\04.png").convert(), (MOUSE_WIDTH, MOUSE_HEIGHT))
cursor2.set_colorkey((255, 255, 255))
