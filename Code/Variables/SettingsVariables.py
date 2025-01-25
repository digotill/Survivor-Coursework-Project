import copy, traceback, cProfile, os, ctypes, logging, moderngl, psutil, time, threading, platform, functools, math, os, random, pygame, gc
import pandas as pd
import numpy as np
from pympler import asizeof
from perlin_noise import PerlinNoise
from pygame.math import Vector2 as v2
from copy import deepcopy
from itertools import product
from pstats import Stats
from Code.Shaders import pygame_shaders
from Code.Variables.LoadAssets import *
from Code.DataStructures.Timer import *
from Code.Utilities.Methods import *
from memory_profiler import profile

pygame.init()

WIN_RES = (1280, int(1280 / (pygame.display.Info().current_w / pygame.display.Info().current_h)))
REN_RES = 640, int(640 / (pygame.display.Info().current_w / pygame.display.Info().current_h))
GAME_SIZE = 3000, 3000

DISPLAY = pygame.display.set_mode(WIN_RES, pygame.OPENGL | pygame.DOUBLEBUF)

pygame.display.toggle_fullscreen()
pygame.display.toggle_fullscreen()

operating_system = platform.system()
refresh_rate = pygame.display.get_current_refresh_rate()

M = Methods()
M.rename_files_recursive(r"C:\Users\digot\PycharmProjects\Survivor-Coursework-Project\Assets")
AM = LoadAssets()
PF = False

pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.display.set_icon(AM.assets["cover"])
pygame.display.set_caption("Survivor Game")

General_Settings = {
          'volume': 0.5,
          'peaceful_mode': False,  # no enemies spawn
          'difficulty': (0.8, 1, 1.3),  # easy, medium, hard
          'enemies': (100, 0.2),  # max, spawn rate
          'brightness': (1.5, 1.5, 20),  # max, min, paused
          'sparks': (20, 0.3, 3.5, 0.1),  # friction, width, height, min_vel
          'hash_maps': (50, 40, 16, 100, 90, 30, 60),  # Enemies, Bullets, Tilemap, Rain, Objects, Particles, Effects
          'cooldowns': (0.5, 0.1),  # toggle cooldowns, value checker cooldown
          'animation_speeds': (15, 20, 10),  # main menu. transition, you died
          "rock": (100, False),  # amount, collisions
          "tree": (0.05, 16),  # density, spreadoutness
          "screen_effect": (1, 5),  # time
          "update_fraction": (0.35, 0.05),  # rain update fraction, enemy update fraction
          "damages": (3, 5),  # acid damage
}

MISC = {"hit_effect": (20, 200), "enemy_spawns": 100}

CAMERA = {'lerp_speed': 5, 'mouse_smoothing': v2(10, 10), 'window_mouse_smoothing_amount': 5, 'deadzone': 1, 'window_max_offset': 0.3,
          'shake_speed': 200, 'reduced_screen_shake': 1, }

GRASS = {"tile_size": 16, "shade_amount": 100, "stiffness": 300, "max_unique": 5, "vertical_place_range": (0, 1), "wind_effect": (13, 25), "density": 0.4,
          "shadow_radius": 3, "shadow_strength": 60, "shadow_shift": (1, 2),
          "Rot_Function": lambda x_val, y_val, game_time: int(math.sin(game_time * 2 + x_val / 100 + y_val / 150) * 15), "positions": {"forest_grass": [0, 1, 2, 3, 4],
          "lush_grass": [5, 6, 7, 8, 9], "spring_grass": [10, 11, 12, 13, 14], "cherryblossom_grass": [15, 16, 17, 18, 19], "wasteland_grass": [20, 21, 22, 23, 24]}}

PLAYER = {'health': 100, 'vel': 90, "sprint_vel": 140, "slowed_vel": 50, 'damage': 30, 'acceleration': 200, "offset": (10, 10, -10, -10), 'animation_speed': 10,
                     "hit_cooldown": 0.8, 'stamina': 100, "stamina_consumption": 20, "stamina_recharge_rate": 30, "grass_force": 10, "slow_cooldown": 0.1}

ENEMIES = {"mantis": {"name": "mantis", "res": (32, 32), "health": 100, "vel": 100, "damage": 15, "attack_range": 50, "stopping_range": 25 ** 2,
                      "steering_strength": 0.4, "friction": 0.2, "animation_speed": 15, "hit_cooldown": 0, "separation_radius": 20, "separation_strength": 0.2, "armour": 1}}

KEYS = {'fullscreen': pygame.K_F11, 'fps': pygame.K_F12, 'escape': pygame.K_F10, "movement": [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d],
                    'ungrab': pygame.K_ESCAPE, 'sprint': pygame.K_LSHIFT, "dodge": pygame.K_SPACE}

EFFECTS = {"blood": {"name": "blood", "res": (48, 48), "speed": (800, 30), "direction": 20, "animation_speed": 40, "vanish_time": (1, 1.5), "variety": 10},}

UI = {"health_bar": (80, 30), "stamina_bar": (80, 30), }

SCREENSHAKE = {"ak47": (5, 0.1), "shotgun": (25, 0.1), "minigun": (5, 0.1), }  # magnitude, duration

SPARKS = {"enemy_hit": {"spread": 60, "scale": 1, "colour": (255, 0, 0), "amount": 5, "min_vel": 3, "max_vel": 10},
                   "muzzle_flash": {"spread": 20, "scale": 0.8, "colour": (255, 255, 255), "amount": 10, "min_vel": 3, "max_vel": 10}}

MAP = {"biomes_map": (0.004, 1), "biomes_density_map": (0.05, 4), "tiles_map": (0.2, 1), "gun_shake_map": (0.1, 2), "camera_shake_map": (0.1, 3)}

BIOMES = {"wasteland": (0.35, 1, True, 0.5), "spring": (0.45, 1, True, 0.5), "forest": (0.55, 1, True, 0.5), "lush": (0.6, 1, True, 1),
          "cherryblossom": (1, 1, True, 0.5), }  # chance, tree density, has padding, padding density

TILES = {"Tile_Ranges": {"water_tile": -0.1, "grass_tile": 1}, "transitions": [["grass_tile", "water_tile"]], "animation_speed": 5, "animated_tiles": [], }

RAIN = {"spawn_rate": 0.1, "amount_spawning": 5, "animation_speed": 30, "angle": 40, "vel": (800, 50), "lifetime": (0.5, 0.8)}

WEAPONS = {
          "ak47": {"vel": 750, "spread": 3, "fire_rate": 0.1, "lifetime": 3, "lifetime_randomness": 0.2, "damage": 50, "distance": -2, "friction": 0.1,
                   "spread_time": 2, "pierce": 2, "shots": 1, "name": "ak47"},
          "shotgun": {"vel": 900, "spread": 15, "fire_rate": 0.8, "lifetime": 0.5, "lifetime_randomness": 0.2, "damage": 50, "distance": -2, "friction": 0.1,
                      "spread_time": 2, "pierce": 2, "shots": 10, "name": "shotgun"},
          "minigun": {"vel": 600, "spread": 5, "fire_rate": 0.01, "lifetime": 2, "lifetime_randomness": 0.2, "damage": 5, "distance": -12, "friction": 0.1,
                      "spread_time": 0.2, "pierce": 1, "shots": 1, "name": "minigun"}}

BUTTONS = {
          "In_Game_Buttons": {
                    "resume": M.create_button("resume", v2(240, 135), AM.assets["button5"]),
                    "fullscreen": M.create_button("fullscreen", v2(240, 170), AM.assets["button5"]),
                    "quit": M.create_button("quit", v2(240, 240), AM.assets["button5"]),
                    "return": M.create_button("return", v2(240, 90), AM.assets["button5"])
          },
          "Weapon_Buttons": {
                    "ak47": M.create_button("ak47", v2(140, 240), M.get_image_outline(AM.assets["ak47"]), {"text_pos": "left", "on": True, "active": True}),
                    "shotgun": M.create_button("shotgun", v2(140, 215), M.get_image_outline(AM.assets["shotgun"]), {"text_pos": "left", "active": True}),
                    "minigun": M.create_button("minigun", v2(140, 180), M.get_image_outline(AM.assets["minigun"]), {"text_pos": "left", "active": True}),
          },
          "Menu_Buttons": {
                    "play": M.create_button("play", v2(200, 240), AM.assets["button5"], {"active": True}),
                    "quit": M.create_button("quit", v2(280, 240), AM.assets["button5"], {"active": True}),
                    "easy": M.create_button("easy", v2(200, 190), AM.assets["button5"], {"active": True}),
                    "medium": M.create_button("medium", v2(200, 150), AM.assets["button5"], {"on": True, "active": True}),
                    "hard": M.create_button("hard", v2(280, 190), AM.assets["button5"], {"active": True})
          },
          "Sliders": {
                    "brightness": M.create_slider(v2(360, 235), "brightness:  ", 0, 100, 50, AM.assets["button7"]),
                    "fps": M.create_slider(v2(360, 180), "max fps:  ", 20, 240, refresh_rate, AM.assets["button7"])
          },
          "End_Screen_Buttons": {
                    "restart": M.create_button("restart", v2(240, 40), AM.assets["button5"]),
                    "quit": M.create_button("quit", v2(400, 40), AM.assets["button5"])
          }
}
