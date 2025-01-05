import copy
import pygame
import moderngl
from perlin_noise import PerlinNoise
from Code.Utilities.Utils import *
from pygame.math import Vector2 as v2

pygame.init()

PROFILE = False

MONITER_RES = pygame.display.Info().current_w, pygame.display.Info().current_h
MONITER_RATIO = MONITER_RES[0] / MONITER_RES[1]
WIN_RES = 1280, int(1280 / MONITER_RATIO)
REN_RES = 640, int(640 / MONITER_RATIO)
GAME_SIZE = 2000, 2000

Display = pygame.display.set_mode(WIN_RES, pygame.OPENGL | pygame.DOUBLEBUF)
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.display.set_icon(load_image("Assets/UI/Cover/cover.png"))
pygame.display.set_caption("Survivor Game")
#pygame.display.toggle_fullscreen()

General_Settings = {
          'volume': 0.5,
          'peaceful_mode': True,
          'EASY_difficulty': 1.3,
          'MEDIUM_difficulty': 1,
          'HARD_difficulty': 0.6,
          'max_enemies': 50,
          'enemy_spawn_rate': 1,
          'max_brightness': 5,
          'min_brightness': 5,
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
                    "ground_shadow": [3, (0, 0, 1), 40, (1, 2)],  # radius, colour, strength, shift
          },
          "Grass_Path": "Assets/Misc/Grass",
          "Buffer_Size": 1,
          "Precision": 30,
          "Density": 0.9,
          "Rot_Function": lambda x_val, y_val, game_time: int(math.sin(game_time * 2 + x_val / 100 + y_val / 150) * 15 +
                                                              math.cos(game_time * 1.5 + y_val / 120 + x_val / 180) * 5)
}

Entity_Images = {
          "player": {
                    "idle": import_gif("Assets/Entities/newplayer/idle"),
                    "run": import_gif("Assets/Entities/newplayer/running"),
                    "sprinting": import_gif("Assets/Entities/newplayer/running"),
          },
          "enemy1": import_gif("Assets/Entities/Enemy1", (32, 36)),
}

Player_Attributes = {
          'name': 'Player',
          'health': 100,
          'res': Entity_Images["player"]["idle"][0].size,
          "animations": Entity_Images["player"],
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
          "enemy1": create_enemy_settings(name="Enemy", health=100, res=Entity_Images["enemy1"][0].size, vel=320,
                                          damage=20,
                                          stopping_distance=25, steering_strength=0.8, friction=0.2,
                                          images=Entity_Images["enemy1"], animation_speed=5, hit_cooldown=0.1,
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
          "player": {
                    "run_magnitude": 1.1,
                    "run_duration": 0.1,
                    "sprinting_magnitude": 1.5,
                    "sprinting_duration": 0.2
          },
          "shooting": {
                    "AK47_magnitude": 10,
                    "AK47_duration": 0.1,
                    "Shotgun_magnitude": 25,
                    "Shotgun_duration": 0.1,
                    "Minigun_magnitude": 15,
                    "Minigun_duration": 0.1
          }
}

Sparks_Settings = {
          "bullet": create_spark_settings(spread=10, scale=0.6, colour=(255, 0, 0), amount=3, min_vel=3, max_vel=10),
          "gun": create_spark_settings(spread=5, scale=0.3, colour=(255, 255, 255), amount=3, min_vel=3, max_vel=10)
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

Bullet_Images = {
          "bullet1": load_image("Assets/Misc/Bullet/Bullet 1/Bullet.png", (12, 9))
}

Weapon_Images = {
          "AK47": load_image("Assets/Misc/Weapons/rifle.png", (32, 13)),
          "Shotgun": load_image("Assets/Misc/Weapons/Shotgun.png", (30, 13)),
          "Minigun": load_image("Assets/Misc/Weapons/Mini gun.png", (34, 16))
}

Weapons = {
          "AK47": create_weapon_settings(
                    vel=750, spread=3, reload_time=2, fire_rate=0.1, clip_size=30,
                    lifetime=3, lifetime_randomness=0.2, damage=8,
                    distance=-2, friction=0.1, animation_speed=5, spread_time=2,
                    pierce=5, shake_mag=2, shake_duration=1, shots=1,
                    gun_image=Weapon_Images["AK47"], res=Weapon_Images["AK47"].size,
                    bullet_image=Bullet_Images["bullet1"], name="AK47"
          ),
          "Shotgun": create_weapon_settings(
                    vel=900, spread=15, reload_time=0.5, fire_rate=0.8, clip_size=8,
                    lifetime=0.5, lifetime_randomness=0.2, damage=5,
                    distance=-2, friction=0.1, animation_speed=5, spread_time=2,
                    pierce=1, shake_mag=2, shake_duration=1, shots=20,
                    gun_image=Weapon_Images["Shotgun"], res=Weapon_Images["Shotgun"].size,
                    bullet_image=Bullet_Images["bullet1"], name="Shotgun"
          ),
          "Minigun": create_weapon_settings(
                    vel=600, spread=50, reload_time=10, fire_rate=0.01, clip_size=100,
                    lifetime=2, lifetime_randomness=0.2, damage=1,
                    distance=-12, friction=0.1, animation_speed=5, spread_time=0.2,
                    pierce=1, shake_mag=2, shake_duration=1, shots=1,
                    gun_image=Weapon_Images["Minigun"], res=Weapon_Images["Minigun"].size,
                    bullet_image=Bullet_Images["bullet1"], name="Minigun"
          )
}

Button_Images = {
          "Button1": load_image("Assets/UI/Buttons/Sprite-0001.png"),
          "Button2": load_image("Assets/UI/Buttons/Sprite-0002.png"),
          "Button3": load_image("Assets/UI/Buttons/Sprite-0003.png"),
          "Button4": load_image("Assets/UI/Buttons/Sprite-0004.png")
}

AllButtons = {
          "In_Game": {
                    "resume": create_button("Resume", v2(240, 135), Button_Images["Button1"]),
                    "fullscreen": create_button("Fullscreen", v2(240, 170), Button_Images["Button1"]),
                    "quit": create_button("QUIT", v2(240, 240), Button_Images["Button1"]),
                    "return": create_button("Return", v2(240, 90), Button_Images["Button1"])
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
                    "brightness": create_slider(v2(360, 235), Button_Images["Button2"], "Brightness:  ", 0, 100,
                                                50),
                    "fps": create_slider(v2(360, 180), Button_Images["Button2"], "Max FPS:  ", 30, 240,
                                         pygame.display.get_current_refresh_rate())
          },
          "Menu_Buttons": {
                    "play": create_button("PLAY", v2(200, 240), Button_Images["Button1"]),
                    "quit": create_button("QUIT", v2(280, 240), Button_Images["Button1"]),
                    "easy": create_button("EASY", v2(200, 190), Button_Images["Button1"]),
                    "medium": create_button("MEDIUM", v2(200, 150), Button_Images["Button1"]),
                    "hard": create_button("HARD", v2(280, 190), Button_Images["Button1"]),
          },
          'speed': 300,
}

Loading_Screens = {
          "Green_Waterfall": import_gif("Assets/LoadingScreens/1"),
          "animation_speed": 15,
}

Tile_Images = {
          "Grass_Tile": import_2d_spritesheet("Assets/Tiles/grass/Sprite-0001.png", 2, 2),
          "Water_Tile": import_2d_spritesheet("Assets/Tiles/water/Sprite-0001.png", 2, 2),
          "Grass_Tile_Water_Tile4x4": import_4x4_spritesheet("Assets/Tiles/Grass_Water/Sprite-0001.png"),
          "Grass_Tile_Water_Tile2x2": import_2x2_spritesheet("Assets/Tiles/Grass_Water/Sprite-0002.png"),
}

Object_Images = {
          "Rocks": import_gif("Assets/Objects/Rocks"),
          "Cars": import_gif("Assets/Objects/Cars"),
}

Objects_Config = {
          "Rock": create_object_settings(Object_Images["Rocks"], Object_Images["Rocks"][0].size, 100, True)
}

Tiles_Congifig = {
          "Tile_Ranges": {
                    "Water_Tile": -0.2,
                    "Grass_Tile": 1,
          },
          "animation_speed": 5,
          "animated_tiles": ["Water_Tile"],
          "tile_map_size": 16,
}

Cursor_Config = {
          "Cursor_Images": import_gif("Assets/UI/Mouse/Mouse3", (13, 13))
}

Bar_Images = {
          "Health_bar": load_image("Assets/UI/Bars/health.png"),
          "Stamina_bar": load_image("Assets/UI/Bars/Sprite-0005.png"),
          "Outside_Health_bar": load_image("Assets/UI/Bars/health_bar.png", UI_Settings["outside_bar_res"])
}

Effect_Images = {
          "Rain": import_gif("Assets/VFX/Rain"),
          "Blood": import_SpriteSheet("Assets/VFX/Blood/Sprite-0001.png", 0, 0, 49, 48, 6),
          "Electric": import_gif("Assets/VFX/electric"),
}

Rain_Config = {
          "animation": Effect_Images["Rain"],
          "rate": 0.0001,
          "animation_speed": 20,
          "amount": 3,
          "vel": 600,
          "vel_randomness": 50,
          "lifetime": 0.9,
          "lifetime_randomness": 0.8,
          "angle": 40,
          "res": Effect_Images["Rain"][0].size
}

Font_Config = {
          'font': "Assets/Font/font2.ttf",
          'font_size': 1.4,
}

# lookup_colour("red")
