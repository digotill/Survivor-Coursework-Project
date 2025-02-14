from Code.Variables.ImportDependencies import *

# Initialize Pygame
pygame.init()

# Set window and rendering resolutions
WINRES = 1280, 720
RENRES = 640, 360
GAMESIZE = 1500, 1500

# Set up the display
DISPLAY = pygame.display.set_mode(WINRES, pygame.OPENGL | pygame.DOUBLEBUF)

# Toggle fullscreen twice (to fix a display issue)
pygame.display.toggle_fullscreen()
pygame.display.toggle_fullscreen()

# Initialize Methods class and rename files
M = Methods()
M.rename_files_recursive(r"C:\Users\digot\PycharmProjects\Survivor-Coursework-Project\Assets")
AM = LoadAssets()

DISPLAY_INFO = pygame.display.Info()

# Set up mouse cursor and window properties
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.display.set_icon(AM.assets["cover"])
pygame.display.set_caption("Survivor Game")

# General game settings
GENERAL = {
          'enemies': (10, 0.2, True, 0.1, 0.1),  # max, spawn rate, spawning on
          'brightness': (1.5, 1.5, 70),  # max, min, paused
          'sparks': (20, 0.3, 3.5, 0.1),  # friction, width, height, min_vel
          'hash_maps': (32, 40, 16, 100, 90, 30, 60, 16),  # Enemies, Bullets, Tilemap, Rain, Objects, Particles, Effects, XP
          'cooldowns': (0.5, 0.1),  # toggle cooldowns, value checker cooldown
          'animation_speeds': (15, 20, 10, 20), }  # main menu. transition, you died

# Progression settings
PROGRESSION = {0: {"canine_grey": 1}, 30: {"canine_grey": 0.8, "canine_white": 1}, 60: {"canine_grey": 0.1, "canine_white": 0.8, "canine_black": 1},
               90: {"canine_white": 0.1, "canine_black": 1, "werewolf": 0}, 120: {"canine_black": 1}, 160: {"pebble": 1}, 190: {"pebble": 0.8,"golem": 1},
               220: {"pebble": 0.1, "golem": 0.8, "armoured_golem": 1}, 250: {"golem": 0.1, "armoured_golem": 1}, 280: {"armoured_golem": 1}, 320: {"mini_peka": 1},
               350: {"mini_peka": 0.8, "bat": 1}, 380: {"mini_peka": 0.1, "bat": 0.8, "skinny": 1}, 410: {"bat": 0.1, "skinny": 1}, 440: {"skinny": 1}}

# Volume settings
VOLUMES = {"music_volume": 0.6, "gun_shot_frequancy": 0.1, "gun_shot_volume": 0.08, "click_shot_frequancy": 0.1, "click_shot_volume": 5}

# Boss settings
BOSSES = {130: "werewolf", 290: "titan", 450: "brain"}

# Difficulty settings    enemy speed, enemy health, enemy damage
DIFFICULTY = {"easy": (0.9, 0.8, 1), "medium": (1, 1, 1), "hard": (1.1, 5, 1)}

# Experience settings
EXPERIENCE = {"starting_max_xp": 100, "xp_progression_rate": 1.2, "blue": 10, "orange": 50, "green": 200, "purple": 1000, "animation_speed": 10,
              "attributes": {"speed": 200, "attraction_distance": 50, "collection_distance": 10}, "gradual_increase": 150}

# Miscellaneous settings
MISC = {"hit_effect": (20, 200), "enemy_spawns": 100, "transition_time": 1, "enviroment_density": (0.05, 16, 250), "blood_on_player_hit": 20,
        "ui_bars": (80, 30), "bullet_knockback": 80, "xp_bar": (240, 30), "blood": 0.6, "youdied_duration": 3, "blood_effect_duration": 4, "tutorial_pos": (40, 180)}

# Camera settings
CAMERA = {'lerp_speed': 5, 'mouse_smoothing': v2(10, 10), 'window_mouse_smoothing_amount': 5, 'deadzone': 1, 'window_max_offset': 0.3,
          'shake_speed': 200, 'reduced_screen_shake': 1}

# Grass settings
GRASS = {"tile_size": 16, "shade_amount": 100, "stiffness": 300, "max_unique": 5, "vertical_place_range": (0, 1), "wind_effect": (13, 25), "density": 0.4,
         "shadow_radius": 3, "shadow_strength": 60, "shadow_shift": (1, 2),
         "Rot_Function": lambda x_val, y_val, game_time: int(math.sin(game_time * 2 + x_val / 100 + y_val / 100) * 15), "positions": {"forest_grass": [0, 1, 2, 3, 4],
         "snow_grass": [5, 6, 7, 8, 9], "spring_grass": [10, 11, 12, 13, 14], "cherryblossom_grass": [15, 16, 17, 18, 19], "wasteland_grass": [20, 21, 22, 23, 24]}}

# Player settings
PLAYER = {'health': 200, "res": (16, 16), 'vel': 100, "sprint_vel": 180, "slowed_vel": 50, 'damage': 30, 'acceleration': 200, "offset": (10, 10, -10, -10),
          'animation_speed': 10, "hit_cooldown": 0.4, 'stamina': 100, "stamina_consumption": 30, "stamina_recharge_rate": 8, "grass_force": 10, "slow_cooldown": 0.1}

# Effect settings
EFFECTS = {"blood": {"name": "blood", "res": (48, 48), "speed": (800, 30), "direction": 20, "animation_speed": 40, "vanish_time": (1, 1.5), "variety": 10}, }

# Screen shake settings     magnitude, duration
SHAKE = {"ak47": (5, 0.1), "shotgun": (25, 0.1), "minigun": (5, 0.1), "hit": (20, 0.5)}

# Spark effect settings
SPARKS = {"muzzle_flash": {"spread": 20, "scale": 0.8, "colour": (255, 255, 255), "amount": 10, "min_vel": 3, "max_vel": 10}}

# Map generation settings
MAP = {"biomes_map": (0.004, 1), "biomes_density_map": (0.05, 4), "tiles_map": (0.2, 1), "gun_shake_map": (0.1, 2), "camera_shake_map": (0.1, 3)}

# Biome settings       chance of biome spawning, tree density, padding density
BIOMES = {"wasteland": (0.35, 1, 1), "spring": (0.45, 0.5, 0.5), "forest": (0.55, 0.5, 0.5), "snow": (0.6, 0.5, 0.5), "cherryblossom": (1, 0.5, 0.5), }

# Tile settings
TILES = {"Tile_Ranges": {"water_tile": -0.1, "grass_tile": 1}, "transitions": [["grass_tile", "water_tile"]], "animation_speed": 5, "animated_tiles": [], }

# Rain effect settings
RAIN = {"spawn_rate": 0.1, "amount_spawning": 5, "animation_speed": 30, "angle": 40, "vel": (800, 50), "lifetime": (0.5, 0.8)}

# Weapon settings
WEAPONS = {
          "ak47": {"vel": 750, "spread": 3, "fire_rate": 0.15, "lifetime": 3, "lifetime_randomness": 0.2, "damage": 50, "distance": -2, "friction": 0.1,
                   "spread_time": 2, "pierce": 2, "shots": 1, "name": "ak47"},
          "shotgun": {"vel": 900, "spread": 15, "fire_rate": 0.9, "lifetime": 0.5, "lifetime_randomness": 0.2, "damage": 40, "distance": -2, "friction": 0.1,
                      "spread_time": 2, "pierce": 5, "shots": 10, "name": "shotgun"}}

# Button settings for various game states
BUTTONS = {
          "In_Game_Buttons": {
                    "resume": M.create_button("resume", v2(320, 135), AM.assets["button12"]),
                    "fullscreen": M.create_button("fullscreen", v2(580, 90), AM.assets["button12"], {"axis": "x", "axisl": "max"}),
                    "quit": M.create_button("quit", v2(320, 180), AM.assets["button12"]),
                    "return": M.create_button("return", v2(320, 90), AM.assets["button12"]), },
          "Weapon_Buttons": {
                    "ak47": M.create_button("ak47", v2(600, 220), M.get_image_outline(AM.assets["ak47"]), {"text_pos": "left", "on": True, "active": True, "axisl": "max", "axis": "x"}),
                    "shotgun": M.create_button("shotgun", v2(600, 140), M.get_image_outline(AM.assets["shotgun"]), {"text_pos": "left", "active": True, "axisl": "max", "axis": "x"})},
          "Menu_Buttons": {
                    "play": M.create_button("play", v2(280, 180), AM.assets["button12"], {"active": True}),
                    "quit": M.create_button("quit", v2(360, 180), AM.assets["button12"], {"active": True}),
                    "easy": M.create_button("easy", v2(220, 30), AM.assets["button12"], {"active": True, "axisl": "min"}),
                    "medium": M.create_button("medium", v2(320, 30), AM.assets["button12"], {"on": True, "active": True, "axisl": "min"}),
                    "hard": M.create_button("hard", v2(420, 30), AM.assets["button12"], {"active": True, "axisl": "min"})},
          "Sliders": {"brightness":
                    M.create_slider(v2(60, 225), "brightness:  ", 0, 100, 50, AM.assets["button12"], {"axis": "x", "axisl": "min"}),
                    "fps": M.create_slider(v2(60, 180), "max fps:  ", 20, 240, 240, AM.assets["button12"], {"axis": "x", "axisl": "min"}),
                    "shake": M.create_slider(v2(60, 135), "reduced shake:  ", 0, 100, 100, AM.assets["button12"], {"axis": "x", "axisl": "min"}),
                    "colour": M.create_slider(v2(60, 90), "colour mode:  ", 1, 100, 50, AM.assets["button12"], {"axis": "x", "axisl": "min"}),
                    "volume": M.create_slider(v2(60, 315), "sound volume:  ", 0, 100, 20, AM.assets["button12"], {"axis": "x", "axisl": "min"}),
                    "text_size": M.create_slider(v2(60, 270), "text size:  ", 100, 150, 100, AM.assets["button12"], {"axis": "x", "axisl": "min"})},
          "End_Screen_Buttons": {
                    "restart": M.create_button("restart", v2(240, 270), AM.assets["button8"], {"axis": "y", "axisl": "max", "res": (92, 30)}),
                     "quit": M.create_button("quit", v2(400, 270), AM.assets["button8"], {"axis": "y", "axisl": "max", "res": (92, 30)})},
          "XP_bar": M.create_button("", v2(320, 30), AM.assets["xp_bar_uncoloured"], {"text_pos": "top", "active": True, "hover_slide": True,
                                                                                      "res": AM.assets["xp_bar_uncoloured"].size, "distance_factor": 0.1, "axisl": "min"})
}

# Enemy settings
ENEMIES = { # name, res, health, vel, damage, attack_range, stopping_range, steering_strength, friction, animation_speed, hit_cooldown, separation_radius, separation_strength, armour, attack_cooldown, xp_chances, has_shadow
          "canine_grey": M.create_enemy("canine_grey", (48, 32), 200, 140, 20, 50, 1, {"blue": 0.9, "orange": 0.95, "green": 0.99, "purple": 1}, True),
          "canine_white": M.create_enemy("canine_white", (48, 32), 300, 150, 25, 50, 1, {"blue": 0.8, "orange": 0.9, "green": 0.95, "purple": 1}, True),
          "canine_black": M.create_enemy("canine_black", (48, 32), 400, 150, 30, 50, 2, {"blue": 0.6, "orange": 0.7, "green": 0.9, "purple": 1}, True),
          "werewolf": M.create_enemy("werewolf", (184, 64), 8000, 200, 60, 100, 5, {"blue": 0, "orange": 0, "green": 0, "purple": 1}, False),
          "pebble": M.create_enemy("pebble", (32, 32), 500, 150, 40, 50, 2, {"blue": 0.5, "orange": 0.65, "green": 0.85, "purple": 1}, False),
          "golem": M.create_enemy("golem", (32, 32), 600, 160, 50, 50, 2, {"blue": 0.45, "orange": 0.6, "green": 0.8, "purple": 1}, False),
          "armoured_golem": M.create_enemy("armoured_golem", (32, 32), 700, 160, 60, 50, 5, {"blue": 0.35, "orange": 0.5, "green": 0.75, "purple": 1}, False),
          "titan": M.create_enemy("titan", (130, 100), 16000, 220, 80, 50, 10, {"blue": 0, "orange": 0, "green": 0, "purple": 1}, False),
          "mini_peka": M.create_enemy("mini_peka", (32, 32), 800, 160, 70, 50, 1, {"blue": 0.3, "orange": 0.45, "green": 0.7, "purple": 1}, True),
          "bat": M.create_enemy("bat", (64, 64), 900, 165, 80, 50, 1, {"blue": 0.25, "orange": 0.4, "green": 0.6, "purple": 1}, False),
          "skinny": M.create_enemy("skinny", (64, 64), 1000, 170, 90, 50, 1, {"blue": 0.2, "orange": 0.3, "green": 0.6, "purple": 1}, False),
          "brain": M.create_enemy("brain", (80, 64), 30000, 210, 100, 50, 2, {"blue": 0, "orange": 0, "green": 0, "purple": 1}, False),
}
