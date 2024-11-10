from Variables import *
from Tools import *
import pygame

display = pygame.display.set_mode(WIN_RES, pygame.RESIZABLE)

BG_entities_gif = import_gif("BG_entities")
Main_Menu_BG = pygame.transform.scale(pygame.image.load("Still BG\\Menu_BG.png").convert(), WIN_RES)

START_BUTTON = pygame.transform.scale(pygame.image.load("Buttons\\StartButton.jpg").convert(), (200, 70))
START_BUTTON.set_colorkey((255, 255, 255))
MENU_BUTTON = pygame.transform.scale(pygame.image.load("Buttons\\MenuButton.jpg").convert(), (200, 70))
MENU_BUTTON.set_colorkey((255, 255, 255))
EXIT_BUTTON = pygame.transform.scale(pygame.image.load("Buttons\\ExitButton.jpg").convert(), (200, 70))
EXIT_BUTTON.set_colorkey((255, 255, 255))

Health_bar = pygame.transform.scale(pygame.image.load("Health Bar\\health_bar.png").convert_alpha(), (300, 90))
Mana_bar = pygame.transform.scale(pygame.image.load("Health Bar\\mana_bar.png").convert_alpha(), (300, 45))

Player_run = import_gif("Player\\Run")
Player_idle = import_gif("Player\\Idle")
Player_hit = import_gif("Player\\Hit")

Enemy_idle = import_gif("Enemy1\\Idle")

Glock_array = import_SpriteSheet("Weapons\\02 - Sprite sheets\\Glock - P80 [64x48]"
                                 "\\[SHOOT WITH CASING AND MUZZLE FLASH] Glock - P80.png", 0, 0, 64, 48, 12)
Glock_bullet = pygame.image.load("Weapons\\01 - Individual sprites\\Bullets & Ammo\\Glock - P80\\Bullet.png").convert_alpha()

BG_sprite1 = import_gif("BG_entities\\sprite1")
BG_sprite2 = import_gif("BG_entities\\sprite2")
BG_sprite3 = import_gif("BG_entities\\sprite3")
BG_sprite4 = import_gif("BG_entities\\sprite4")

cursor1 = pygame.transform.scale(pygame.image.load("cursor\\03.png").convert(), (MOUSE_WIDTH, MOUSE_HEIGHT))
cursor1.set_colorkey((255, 255, 255))
cursor2 = pygame.transform.scale(pygame.image.load("cursor\\04.png").convert(), (MOUSE_WIDTH, MOUSE_HEIGHT))
cursor2.set_colorkey((255, 255, 255))
