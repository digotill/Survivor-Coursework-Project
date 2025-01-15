import copy
import pygame
import moderngl
from perlin_noise import PerlinNoise
from Code.Utilities.Utils import *
from pygame.math import Vector2 as v2
from Code.Variables.AssetManager import *

pygame.init()

WIN_RES = 1280, int(1280 / (pygame.display.Info().current_w / pygame.display.Info().current_h))
REN_RES = 640, int(640 / (pygame.display.Info().current_w / pygame.display.Info().current_h))
GAME_SIZE = 2000, 2000
DISPLAY = pygame.display.set_mode(WIN_RES, pygame.OPENGL | pygame.DOUBLEBUF)

AM = AssetManager()
PF = False

pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.display.set_icon(AM.assets["Cover"])
pygame.display.set_caption("Survivor Game")
#pygame.display.toggle_fullscreen()

General_Settings = {
          'volume': 0.5,
          'peaceful_mode': True,
          'difficulty': [0.8, 1, 1.3],
          'max_enemies': 50,
          'enemy_spawn_rate': 0.2,
          'max_brightness': 1.5,
          'min_brightness': 1.5,
          'spatial_hash_map_size': 100,
          'tilemap_size': 15,
          'darkness': (12, 12, 12)
}

Window_Attributes = {
          'lerp_speed': 5,
          'mouse_smoothing': v2(10, 10),
          'deadzone': 3,
          'window_mouse_smoothing_amount': 50,
          'window_max_offset': 0.3,
          'shake_speed': 200,
          'shake_seed': random.random() * 1000,
          'shake_directions': v2(1, 1),
          'reduced_screen_shake': 1,
          'shake_duration': 0,
          'shake_start_time': 0,
          'shake_magnitude': 0,
}

Grass = {
          "Grass_Settings": {
                    "tile_size": 16,
                    "shade_amount": 100,
                    "stiffness": 300,
                    "max_unique": 5,
                    "vertical_place_range": [0, 1],
                    "padding": 13,
                    "ground_shadow": [3, (0, 0, 1), 60, (1, 2)],  # radius, colour, strength, shift
          },
          "Precision": 25,
          "Density": 0.6,
          "Rot_Function": lambda x_val, y_val, game_time: int(math.sin(game_time * 2 + x_val / 100 + y_val / 150) * 15 +
                                                              math.cos(game_time * 1.5 + y_val / 120 + x_val / 180) * 5)
}

Player_Attributes = {
          'name': 'Player',
          'health': 100,
          'res': AM.assets["player_idle"][0].size,
          "animations": {
                    "idle": AM.assets["player_idle"],
                    "run": AM.assets["player_running"],
                    "sprinting": AM.assets["player_running"],
          },
          'vel': 90,
          'damage': 30,
          'stamina': 100,
          'acceleration': 200,
          "offset": (10, 10, -10, -10),
          'animation_speed': 10,
          "hit_cooldown": 0.5,
          "sprint_speed": 140,
          "stamina_consumption": 20,
          "stamina_recharge_rate": 30,
          "max_stamina": 100,
          "grass_force_dropoff": 10,
}

Enemies = {
          "enemy1": create_enemy_settings(name="Enemy", health=100, res=AM.assets["enemy 1"][0].size, vel=100,
                                          damage=20,
                                          stopping_distance=25, steering_strength=0.8, friction=0.2,
                                          images=AM.assets["enemy 1"], animation_speed=5, hit_cooldown=0,
                                          )
}

Cooldowns = {
          'fps': 0.5,
          'fullscreen': 0.5,
          'settings': 0.5,
          'buttons': 0.5,
}

Keys = {
          'fullscreen': pygame.K_F11,
          'fps': pygame.K_F12,
          'escape': pygame.K_F10,
          'ungrab': pygame.K_ESCAPE,
          'sprint': pygame.K_LSHIFT
}

UI_Settings = {
          "health_bar": (135, 95),
          "stamina_bar": (170, 95),
          "bar_res": (94, 8),
          "outside_bar_res": (106, 19),
          "fps": (150, 70),
          "time": (150, 70),
          "fps_time_size": 14,
}

Screen_Shake = {
          "shooting": {
                    "AK47_magnitude": 5,
                    "AK47_duration": 0.1,
                    "Shotgun_magnitude": 25,
                    "Shotgun_duration": 0.1,
                    "Minigun_magnitude": 5,
                    "Minigun_duration": 0.1
          }
}

Sparks_Settings = {
          "enemy_hit": create_spark_settings(spread=60, scale=1, colour=(255, 0, 0), amount=5, min_vel=3, max_vel=10),
          "muzzle_flash": create_spark_settings(spread=20, scale=0.8, colour=(255, 255, 255), amount=10, min_vel=3,
                                                max_vel=10)
}

General_Spark_Settings = {
          "friction": 20,
          "width": 0.3,
          "height": 3.5,
          "min_vel": 0.1,
}

Perlin_Noise = {
          "1 octave": PerlinNoise(1, random.randint(0, 100000)),
          "2 octaves": PerlinNoise(2, random.randint(0, 100000)),
          "3 octaves": PerlinNoise(3, random.randint(0, 100000))
}

Weapons = {
          "AK47": create_weapon_settings(
                    vel=750, spread=3, reload_time=2, fire_rate=0.1, clip_size=30,
                    lifetime=3, lifetime_randomness=0.2, damage=16,
                    distance=-2, friction=0.1, animation_speed=5, spread_time=2,
                    pierce=3, shake_mag=2, shake_duration=1, shots=1,
                    gun_image=AM.assets["AK47"], res=AM.assets["AK47"].size,
                    bullet_image=AM.assets["Bullet"], name="AK47"
          ),
          "Shotgun": create_weapon_settings(
                    vel=900, spread=15, reload_time=0.5, fire_rate=0.8, clip_size=8,
                    lifetime=0.5, lifetime_randomness=0.2, damage=50,
                    distance=-2, friction=0.1, animation_speed=5, spread_time=2,
                    pierce=1, shake_mag=2, shake_duration=1, shots=20,
                    gun_image=AM.assets["Shotgun"], res=AM.assets["Shotgun"].size,
                    bullet_image=AM.assets["Bullet"], name="Shotgun"
          ),
          "Minigun": create_weapon_settings(
                    vel=600, spread=5, reload_time=10, fire_rate=0.01, clip_size=100,
                    lifetime=2, lifetime_randomness=0.2, damage=5,
                    distance=-12, friction=0.1, animation_speed=5, spread_time=0.2,
                    pierce=0, shake_mag=2, shake_duration=1, shots=1,
                    gun_image=AM.assets["Minigun"], res=AM.assets["Minigun"].size,
                    bullet_image=AM.assets["Bullet"], name="Minigun"
          )
}

AllButtons = {
          "In_Game": {
                    "resume": create_button("Resume", v2(240, 135), AM.assets["Button1"]),
                    "fullscreen": create_button("Fullscreen", v2(240, 170), AM.assets["Button1"]),
                    "quit": create_button("QUIT", v2(240, 240), AM.assets["Button1"]),
                    "return": create_button("Return", v2(240, 90), AM.assets["Button1"])
          },
          "Weapons": {
                    "AK47": create_button("AK47", v2(140, 240), perfect_outline(Weapons["AK47"]["gun_image"]),
                                          text_pos="left"),
                    "Shotgun": create_button("Shotgun", v2(140, 215),
                                             perfect_outline(Weapons["Shotgun"]["gun_image"]),
                                             text_pos="left"),
                    "Minigun": create_button("Minigun", v2(140, 180),
                                             perfect_outline(Weapons["Minigun"]["gun_image"]),
                                             text_pos="left"),
          },
          "Sliders": {
                    "brightness": create_slider(v2(360, 235), AM.assets["Button2"], "Brightness:  ", 0, 100,
                                                50),
                    "fps": create_slider(v2(360, 180), AM.assets["Button2"], "Max FPS:  ", 20, 240,
                                         pygame.display.get_current_refresh_rate())
          },
          "Menu_Buttons": {
                    "play": create_button("PLAY", v2(200, 240), AM.assets["Button1"]),
                    "quit": create_button("QUIT", v2(280, 240), AM.assets["Button1"]),
                    "easy": create_button("EASY", v2(200, 190), AM.assets["Button1"]),
                    "medium": create_button("MEDIUM", v2(200, 150), AM.assets["Button1"]),
                    "hard": create_button("HARD", v2(280, 190), AM.assets["Button1"]),
          },
          'speed': 300,
}


Objects_Config = {
          "Rock": create_object_settings(AM.assets["Rock"], AM.assets["Rock"][0].size, 100, True),
}

Tiles_Congifig = {
          "Tile_Ranges": {
                    "Water_Tile": -0.2,
                    "Grass_Tile": 1,
          },
          "transitions": [["Grass_Tile", "Water_Tile"]],
          "animation_speed": 5,
          "animated_tiles": [],
          "tile_map_size": 16,
}

Rain_Config = {
          "animation": AM.assets["Rain"],
          "rate": 0.0001,
          "animation_speed": 20,
          "amount": 3,
          "vel": 600,
          "vel_randomness": 50,
          "lifetime": 0.9,
          "lifetime_randomness": 0.8,
          "angle": 40,
          "res": AM.assets["Rain"][0].size
}

# lookup_colour("red")
