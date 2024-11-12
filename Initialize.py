from Variables import *
from Tools import *
import pygame

display = pygame.display.set_mode(WIN_RES, pygame.RESIZABLE)

BG_entities_gif = import_gif("BG_entities")
Main_Menu_BG = pygame.transform.scale(pygame.image.load("Still BG\\Menu_BG.png").convert(), WIN_RES)

Buttons = import_gif("Buttons Bar", (300, 80))

Health_bar = pygame.transform.scale(pygame.image.load("Health Bar\\health.png").convert_alpha(), (300, 90))
Stamina_bar = pygame.transform.scale(pygame.image.load("Health Bar\\Sprite-0005.png").convert_alpha(), (300, 90))

Player_run = import_gif("Player\\Run")
Player_idle = import_gif("Player\\Idle")
Player_hit = import_gif("Player\\Hit")

Enemy_idle = import_gif("Enemy1\\Idle")

Glock_bullet = pygame.image.load("Weapons\\01 - Individual sprites\\Bullets & Ammo\\Glock - P80\\Bullet.png").convert_alpha()

Rifle = pygame.image.load("Weapons\\rifle.png").convert_alpha()

BG_sprites = import_gif("BG_entities")

cursor1 = pygame.transform.scale(pygame.image.load("cursor\\03.png").convert(), (MOUSE_WIDTH, MOUSE_HEIGHT))
cursor1.set_colorkey((255, 255, 255))
cursor2 = pygame.transform.scale(pygame.image.load("cursor\\04.png").convert(), (MOUSE_WIDTH, MOUSE_HEIGHT))
cursor2.set_colorkey((255, 255, 255))
