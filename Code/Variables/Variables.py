import copy
from perlin_noise import PerlinNoise
from Code.Utilities.Utils import *
from pygame.math import Vector2 as v2

pygame.init()

START_FULLSCREEN = False
PEACEFUL_MODE = False
PROFILE = False

MONITER_RES = pygame.display.Info().current_w, pygame.display.Info().current_h
MIN_WIN_RES = 1280, 720
WIN_RES = MONITER_RES if START_FULLSCREEN else MIN_WIN_RES
GAME_SIZE = 3840, 2160
REN_RES = 640, 360

Display = pygame.display.set_mode(WIN_RES, pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.display.set_icon(load_image("Assets/Misc/Cover/cover.png"))
pygame.display.set_caption("Survivor Game")

General_Settings = {
          'difficulty': "MEDIUM",
          'volume': 0.5,
          'animation_speed': 5,
          'main_menu_animation_speed': 15,
          'mouse_res': (13, 13),
          'font': "Assets/Font/font2.ttf",
          'font_size': 1.4,
          'EASY_difficulty': 1.3,
          'MEDIUM_difficulty': 1,
          'HARD_difficulty': 0.6,
          'buttons_res': (46, 15),
          'buttons_speed': 900,
          'buttons_friction': 300,
          'fps_size': 15,
          'enemy_separation_radius': 15,
          'enemy_separation_strength': 0.4,
          'max_enemies': 100,
          'brightness': 50,
          'max_brightness': 2.5,
          'min_brightness': 0.5,
          'spatial_hash_map_size': 100,
          'tilemap_size': 16,
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
          'target_offset': v2(0, 0),
          'current_offset': v2(0, 0),
          'shake_duration': 0,
          'shake_start_time': 0,
          'shake_magnitude': 0,
}

Entity_Images = {
          "player": cached_import_gif("Assets/Entities/Player/new player/idle", (64, 64)),
          "enemy1": cached_import_gif("Assets/Entities/Enemy1", (32, 36)),
}

Player_Attributes = {
          'name': 'Player',
          'health': 100,
          'res': Entity_Images["player"][0].size,
          'vel': 200,
          'damage': 30,
          'stamina': 100,
          'acceleration': 600,
          'offset_x1': 0,
          'offset_x2': 0,
          'offset_y1': 0,
          'offset_y2': 0,
          'animation_speed': 5,
          "images": Entity_Images["player"],
}

Enemies = {
          "enemy1": create_enemy_settings(name="Enemy", health=100, res=Entity_Images["enemy1"][0].size, vel=320, damage=20,
                                          stopping_distance=25, steering_strength=0.8, friction=0.2,
                                          images=Entity_Images["enemy1"]
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
}

UI_Settings = {
          "health_bar": (135, 95),
          "stamina_bar": (170, 95),
          "bar_res": (94, 8),
          "outside_bar_res": (106, 19),
          "fps": (150, 70),
          "time": (150, 70),
}

Screen_Shake = {
          'bullet_impact_shake_duration': 0.5,
          'bullet_impact_shake_magnitude': 4,
}

Sparks_Settings = {
          "bullet": create_spark_settings(spread=10, size=0.6, colour=(255, 0, 0), amount=3, min_vel=3, max_vel=10),
          "gun": create_spark_settings(spread=5, size=0.3, colour=(255, 255, 255), amount=3, min_vel=3, max_vel=10)
}

General_Spark_Settings = {
          "friction": 20,
          "width": 0.3,
          "height": 3.5,
          "min_vel": 1,
}

Perlin_Noise = {
          "perlin": PerlinNoise(3, random.randint(0, 100000))
}

Bullet_Images = {
          "bullet1": load_image("Assets/Objects/Bullet/Bullet 1/Bullet.png")
}

Weapon_Images = {
          "AK47": load_image("Assets/Objects/Weapons/rifle.png", (32, 13)),
          "Shotgun": load_image("Assets/Objects/Weapons/Shotgun.png", (30, 13)),
          "Minigun": load_image("Assets/Objects/Weapons/Mini gun.png", (34, 16))
}

Weapons = {
          "AK47": create_weapon_settings(
                    vel=750, spread=3, reload_time=2, fire_rate=0.1, clip_size=30,
                    lifetime=3, lifetime_randomness=0.2, damage=8, distance_parrallel=-2,
                    distance_perpendicular=0, friction=0.1, animation_speed=5, spread_time=2,
                    pierce=2, shake_mag=2, shake_duration=1, shots=1,
                    gun_image=Weapon_Images["AK47"], res=Weapon_Images["AK47"].size,
                    bullet_image=Bullet_Images["bullet1"]
          ),
          "Shotgun": create_weapon_settings(
                    vel=900, spread=15, reload_time=0.5, fire_rate=0.8, clip_size=8,
                    lifetime=0.5, lifetime_randomness=0.2, damage=5, distance_parrallel=-2,
                    distance_perpendicular=0, friction=0.1, animation_speed=5, spread_time=2,
                    pierce=1, shake_mag=2, shake_duration=1, shots=20,
                    gun_image=Weapon_Images["Shotgun"], res=Weapon_Images["Shotgun"].size,
                    bullet_image=Bullet_Images["bullet1"]
          ),
          "Minigun": create_weapon_settings(
                    vel=600, spread=10, reload_time=10, fire_rate=0.01, clip_size=100,
                    lifetime=2, lifetime_randomness=0.2, damage=1, distance_parrallel=-10,
                    distance_perpendicular=0, friction=0.1, animation_speed=5, spread_time=2,
                    pierce=1, shake_mag=2, shake_duration=1, shots=1,
                    gun_image=Weapon_Images["Minigun"], res=Weapon_Images["Minigun"].size,
                    bullet_image=Bullet_Images["bullet1"]
          )
}

Button_Images = {
          "Button1": load_image("Assets/Misc/Buttons/Sprite-0001.png"),
          "Button2": load_image("Assets/Misc/Buttons/Sprite-0002.png"),
          "Button3": load_image("Assets/Misc/Buttons/Sprite-0003.png"),
          "Button4": load_image("Assets/Misc/Buttons/Sprite-0004.png")
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
                              "brightness": create_slider(v2(360, 235), Button_Images["Button2"], "Brightness", 0, 100,
                                                          General_Settings['brightness']),
                              "fps": create_slider(v2(360, 180), Button_Images["Button2"], "Max FPS", 60, 500,
                                                   pygame.display.get_current_refresh_rate())
                    },
                    "Menu_Buttons": {
                              "play": create_button("PLAY", v2(200, 240), Button_Images["Button1"]),
                              "quit": create_button("QUIT", v2(280, 240), Button_Images["Button1"]),
                              "easy": create_button("EASY", v2(200, 190), Button_Images["Button1"]),
                              "medium": create_button("MEDIUM", v2(200, 150), Button_Images["Button1"]),
                              "hard": create_button("HARD", v2(280, 190), Button_Images["Button1"]),
                    }
          }


Loading_Screens = {
          "Green_Waterfall": cached_import_gif("Assets/LoadingScreens/1", WIN_RES),
          "Orange_Pond": cached_import_gif("Assets/LoadingScreens/2", WIN_RES)
}

Tile_Images = {
          "Grass_Tile": load_image("Assets/Misc/Tiles/grass.png",
                                   (General_Settings['tilemap_size'], General_Settings['tilemap_size'])),
          "Water_Tile": load_image("Assets/Misc/Tiles/water.png",
                                   (General_Settings['tilemap_size'], General_Settings['tilemap_size']))
}

Cursor_Images = {
          "Cursor_Clicking": load_image("Assets/Misc/Mouse/Mouse3/Sprite-0002.png", General_Settings['mouse_res']),
          "Cursor_Not_Clicking": load_image("Assets/Misc/Mouse/Mouse3/Sprite-0001.png", General_Settings['mouse_res'])
}

Bar_Images = {
          "Health_bar": load_image("Assets/Misc/Bars/health.png"),
          "Stamina_bar": load_image("Assets/Misc/Bars/Sprite-0005.png"),
          "Outside_Health_bar": load_image("Assets/Misc/Bars/health_bar.png", UI_Settings["outside_bar_res"])
}

Effect_Images = {
          "Slash_Effect": cached_import_gif("Assets/VFX/Slash")
}

# lookup_colour("red")
