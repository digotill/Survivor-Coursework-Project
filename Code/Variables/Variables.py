import copy
import pygame
import moderngl
import psutil
from pympler import asizeof
from perlin_noise import PerlinNoise
from Code.Utilities.Utils import *
from pygame.math import Vector2 as v2
from Code.Variables.AssetManager import *

pygame.init()

WIN_RES = 1280, int(1280 / (pygame.display.Info().current_w / pygame.display.Info().current_h))
REN_RES = 640, int(640 / (pygame.display.Info().current_w / pygame.display.Info().current_h))
GAME_SIZE = 2000, 2000

DISPLAY = pygame.display.set_mode(WIN_RES, pygame.OPENGL | pygame.DOUBLEBUF)

physical_cores = psutil.cpu_count(logical=False)
logical_cores = psutil.cpu_count(logical=True)

AM = AssetManager()
PF = False

pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.display.set_icon(AM.assets["cover"])
pygame.display.set_caption("Survivor Game")

General_Settings = {
          'volume': 0.5,
          'peaceful_mode': False,  # no enemies spawn
          'difficulty': (0.8, 1, 1.3),  # easy, medium, hard
          'enemies': (50, 0.2),  # max, spawn rate
          'brightness': (1.5, 1.5, 12),  # max, min, paused
          'sparks': (20, 0.3, 3.5, 0.1),  # friction, width, height, min_vel
          'hash_maps': (50, 40, 16, 10, 90, 30),  # Enemies, Bullets, Tilemap, Rain, Objects, Particles
          'cooldowns': (0.5, 0.1)  # toggle cooldowns, value checker cooldown
}

Window_Attributes = {
          'lerp_speed': 5,
          'mouse_smoothing': v2(10, 10),
          'window_mouse_smoothing_amount': 5,
          'deadzone': 1,
          'window_max_offset': 0.3,
          'shake_speed': 200,
          'reduced_screen_shake': 1,
}

Grass = {
          "tile_size": 16,
          "shade_amount": 100,
          "stiffness": 300,
          "max_unique": 5,
          "vertical_place_range": (0, 1),
          "wind_effect": (13, 25),
          "ground_shadow": (3, (0, 0, 1), 60, (1, 2)),  # radius, colour, strength, shift
          "density": 0.4,
          "Rot_Function": lambda x_val, y_val, game_time: int(math.sin(game_time * 2 + x_val / 100 + y_val / 150) * 15 + math.cos(game_time * 1.5 + y_val / 120 + x_val / 180) * 5)
}

Player_Attributes = {
          'name': 'player',
          'health': 100,
          "animations": {
                    "idle": AM.assets["player_idle"],
                    "run": AM.assets["player_running"],
          },
          'vel': 90,
          "sprint_vel": 140,
          'damage': 30,
          'acceleration': 200,
          "offset": (10, 10, -10, -10),  # distance from edge of area
          'animation_speed': 10,
          "hit_cooldown": 0.5,
          'stamina': 100,
          "stamina_consumption": 20,
          "stamina_recharge_rate": 30,
          "grass_force": 10,  # grass force drop off
}

Enemies = {
          "enemy1": create_enemy_settings(name="enemy1", health=100, vel=100, damage=20, stopping_distance=25, steering_strength=0.8, friction=0.2, animation_speed=5,
                                          hit_cooldown=0, separation_radius=20, separation_strength=5)
}

Keys = {
          'fullscreen': pygame.K_F11, 'fps': pygame.K_F12, 'escape': pygame.K_F10, 'ungrab': pygame.K_ESCAPE, 'sprint': pygame.K_LSHIFT,
}

UI_Settings = {
          "health_bar": (80, 30), "stamina_bar": (80, 30),
}

Screen_Shake = {
          "ak47": (5, 0.1), "shotgun": (25, 0.1), "minigun": (5, 0.1),  # magnitude, duration
}

Sparks_Settings = {
          "enemy_hit": create_spark_settings(spread=60, scale=1, colour=(255, 0, 0), amount=5, min_vel=3, max_vel=10),
          "muzzle_flash": create_spark_settings(spread=20, scale=0.8, colour=(255, 255, 255), amount=10, min_vel=3, max_vel=10)
}

Perlin_Noise = {
          "biome_map": (0.004, 4), "density_map": (0.05, 4), "overworld_map": (0.05, 1), "gun_shake_map": (0.1, 2), "camera_shake_map": (0.1, 3)
}

Weapons = {
          "ak47": create_weapon_settings(vel=750, spread=3, reload_time=2, fire_rate=0.1, clip_size=30, lifetime=3, lifetime_randomness=0.2, damage=16,
                                         distance=-2, friction=0.1, animation_speed=5, spread_time=2, pierce=3, shots=1, name="ak47"
                                         ),
          "shotgun": create_weapon_settings(vel=900, spread=15, reload_time=0.5, fire_rate=0.8, clip_size=8, lifetime=0.5, lifetime_randomness=0.2, damage=50,
                                            distance=-2, friction=0.1, animation_speed=5, spread_time=2, pierce=1, shots=20, name="shotgun"
                                            ),
          "minigun": create_weapon_settings(vel=600, spread=5, reload_time=10, fire_rate=0.01, clip_size=100, lifetime=2, lifetime_randomness=0.2, damage=5,
                                            distance=-12, friction=0.1, animation_speed=5, spread_time=0.2, pierce=0, shots=1, name="minigun"
                                            ),
}

AllButtons = {
          "In_Game": {"resume": create_button("Resume", v2(240, 135), AM.assets["button1"]),
                      "fullscreen": create_button("Fullscreen", v2(240, 170), AM.assets["button1"]),
                      "quit": create_button("QUIT", v2(240, 240), AM.assets["button1"]),
                      "return": create_button("Return", v2(240, 90), AM.assets["button1"])
                      },
          "Weapons": {"ak47": create_button("ak47", v2(140, 240), perfect_outline(AM.assets["ak47"]), text_pos="left"),
                      "shotgun": create_button("shotgun", v2(140, 215), perfect_outline(AM.assets["shotgun"]), text_pos="left"),
                      "minigun": create_button("minigun", v2(140, 180), perfect_outline(AM.assets["minigun"]), text_pos="left"),
                      },
          "Sliders": {"brightness": create_slider(v2(360, 235), AM.assets["button2"], "Brightness:  ", 0, 100, 50),
                      "fps": create_slider(v2(360, 180), AM.assets["button2"], "Max FPS:  ", 20, 240, pygame.display.get_current_refresh_rate())
                      },
          "Menu_Buttons": {"play": create_button("play", v2(200, 240), AM.assets["button1"]),
                           "quit": create_button("quit", v2(280, 240), AM.assets["button1"]),
                           "easy": create_button("easy", v2(200, 190), AM.assets["button1"]),
                           "medium": create_button("medium", v2(200, 150), AM.assets["button1"]),
                           "hard": create_button("hard", v2(280, 190), AM.assets["button1"]),
                           },
          'speed': 300,
}

Objects_Config = {
          "rock": (100, False),  # amount, collisions
          "tree": (0.2, 20),  # density, spreadoutness
          "placement": (20, 10),  # distance from original position, attempts
}

Biomes_Config = {
          "dead": (0.35, 1), "yellowish": (0.4, 1), "green": (0.5, 1), "ripe": (0.6, 1), "lush": (1, 1),  # chance, amount
}

Tiles_Congifig = {
          "Tile_Ranges": {"water_tile": -0.1, "grass_tile": 1,
                          },
          "transitions": [["grass_tile", "water_tile"]],
          "animation_speed": 5,
          "animated_tiles": [],
}

Rain_Config = {
          "spawn_rate": (0.05, 12),  # spawn rate, amount spawning
          "look": (30, 40),  # animation speed, angle
          "vel": (600, 50),  # initial value, randomness
          "lifetime": (0.9, 0.8),  # initial value, randomness
}
