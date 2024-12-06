from perlin_noise import PerlinNoise
from Code.Utilities.Utils import *
from pygame.math import Vector2 as v2

pygame.init()

START_FULLSCREEN = False
PEACEFUL_MODE = True
STARTING_DIFFICULTY = "MEDIUM"
MONITER_RES = pygame.display.Info().current_w, pygame.display.Info().current_h
MIN_WIN_RES = 1280, 720
MAX_WIN_RES = 2560, 1440
WIN_RES = MONITER_RES if START_FULLSCREEN else MIN_WIN_RES
PLAYABLE_AREA_SIZE = 3840, 2160
REN_RES = 640, 360

player_attributes = {
          'name': 'Player',
          'health': 100,
          'res': (64, 64),
          'vel': 200,
          'damage': 30,
          'stamina': 100,
          'acceleration': 600,
          'offset_x1': 0,
          'offset_x2': 0,
          'offset_y1': 0,
          'offset_y2': 0,
          'animation_speed': 5,
}

enemy_attributes = {
          'name': "Enemy",
          'health': 100,
          'res': (32, 36),
          'vel': 320,
          'damage': 20,
          'spawn_rate': 1,
          'bullet_res': (10, 10),
          'bullet_damage': 10,
          'bullet_lifetime': 1000,
          'bullet_speed': 700,
          'stopping_distance': 25,
          'steering_strength': 0.8,
          'friction': 0.2,
          'max_enemies': 50,
          'animation_speed': 5,
}

screen_shake = {
          'bullet_impact_shake_duration': 0.5,
          'bullet_impact_shake_magnitude': 4,
}

general_settings = {
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
}

window_attributes = {
          'lerp_speed': 5,
          'mouse_smoothing': v2(10, 10),
          'deadzone': 3,
          'mouse_smoothing_amount': 50,
          'max_offset': 0.3,
          'shake_speed': 200,
          'shake_seed': random.random() * 1000,
          'shake_directions': v2(1, 1),
          'reduced_screen_shake': 1,
          'brightness': 50,
          'max_brightness': 2.5,
          'min_brightness': 0.5,
          'spatial_hash_map_size': 100,
          'tilemap_size': 16,
          'darkness': (12, 12, 12)
}

cooldowns = {
          'fps': 0.5,
          'fullscreen': 0.5,
          'settings': 0.5,
          'buttons': 0.5,
}

keys = {
          'fullscreen': pygame.K_F11,
          'fps': pygame.K_F12,
          'escape': pygame.K_F10,
          'ungrab': pygame.K_ESCAPE,
}

ui = {
          "health_bar": (135, 95),
          "stamina_bar": (170, 95),
          "bar_res": (94, 8),
          "outside_bar_res": (106, 19),
          "fps": (150, 70),
          "time": (150, 70),
}

sparks = {
          "bullet": create_spark_settings(
                    spread=10,
                    size=0.6,
                    colour=(255, 0, 0),
                    amount=3
          ),
          "gun": create_spark_settings(
                    spread=5,
                    size=0.3,
                    colour=(255, 255, 255),
                    amount=3
          )
}

perlin_noise = {
          "perlin_octaves": 3,
          "perlin_seed": random.randint(0, 100000)
}
perlin_noise["perlin"] = PerlinNoise(octaves=perlin_noise["perlin_octaves"], seed=perlin_noise["perlin_seed"])

buttons = {
          "play": create_button_settings("PLAY", (200, 240)),
          "quit": create_button_settings("QUIT", (280, 240)),
          "easy": create_button_settings("EASY", (200, 190)),
          "medium": create_button_settings("MEDIUM", (200, 150)),
          "hard": create_button_settings("HARD", (280, 190)),
          "fullscreen": create_button_settings("Fullscreen", (240, 170)),
          "new_quit": create_button_settings("Quit", (240, 215)),
          "resume": create_button_settings("Resume", (240, 135)),
          "AK47": create_button_settings("0", (140, 240)),
          "Shotgun": create_button_settings("0", (140, 215)),
          "Minigun": create_button_settings("0", (140, 180)),
          "Return": create_button_settings("Return", (240, 90)),
}

sliders = {
          "brightness": {
                    "pos": (360, 235),
                    "text": "Brightness: ",
                    "axis": "y",
                    "axisl": "max",
                    "text_pos": "right"
          },
          "fps": {
                    "pos": (360, 180),
                    "text": "Max FPS: ",
                    "axis": "y",
                    "axisl": "max",
                    "text_pos": "right"
          }
}

weapons = {
          "AK47": create_weapon_settings((32, 13), 750, 3, 2, 0.1, 30, 3,
                                         0.2, 2, -2, 0, 0.1, 5, 2, 2, 2, 1),
          "Shotgun": create_weapon_settings((30, 13), 900, 15, 0.5, 0.8, 8, 0.5,
                                            0.2, 5, -2, 0, 0.1, 5, 2, 1, 2, 1),
          "Minigun": create_weapon_settings((34, 16), 600, 10, 10, 0.01, 100, 2,
                                            0.2, 1, -10, 0, 0.1, 5, 2, 1, 2, 1)
}
