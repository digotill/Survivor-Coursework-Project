import functools
import math
import os
import random
import numpy as np
import pygame


def random_xy(rect1, rect2, sprite_width, sprite_height):
          while True:
                    x = random.randint(rect1.left, rect1.right - sprite_width)
                    y = random.randint(rect1.top, rect1.bottom - sprite_height)
                    if not rect2.collidepoint(x, y): return x, y


def change_random(number, diff):
          diff = random.random() * diff
          if random.randint(0, 1) == 0:
                    return number - diff
          else:
                    return number + diff


def calculate_distances(player_pos, enemy_positions):
          return np.linalg.norm(enemy_positions - player_pos, axis=1)


def check_collisions(player_rect, object_rects):
          player_array = np.array([player_rect.left, player_rect.top, player_rect.right, player_rect.bottom])
          objects_array = np.array([[rect.left, rect.top, rect.right, rect.bottom] for rect in object_rects])

          collisions = np.all((player_array[:2] < objects_array[:, 2:]) &
                              (player_array[2:] > objects_array[:, :2]), axis=1)

          return np.where(collisions)[0]


def load_image(file_path, res=None, *color_keys):
          img = pygame.image.load(file_path).convert_alpha()
          if res: img = pygame.transform.scale(img, res)
          for color_key in color_keys: img.set_colorkey(color_key)
          return img


@functools.lru_cache(maxsize=None)
def cached_load(file_path, res=None, *color_keys):
          return load_image(file_path, res, *color_keys)


def cached_import_gif(file_name, res=None, *color_keys):
          file_paths = [os.path.join(file_name, f) for f in os.listdir(file_name) if f.endswith(('.jpg', '.png'))]
          return [cached_load(file_path, res, *color_keys) for file_path in file_paths]


def import_SpriteSheet(filename, px, py, tw, th, tiles, res=None, *color_keys):
          sheet = load_image(filename, None, *color_keys)
          array = []
          for i in range(tiles):
                    cropped = pygame.Surface((tw, th), pygame.SRCALPHA)
                    cropped.blit(sheet, (0, 0), (px + tw * i, py, tw, th))
                    if res: cropped = pygame.transform.scale(cropped, res)
                    array.append(cropped)
          return array


def perfect_outline(img, outline_color=(255, 255, 255)):
          mask = pygame.mask.from_surface(img)
          mask_outline = mask.outline()
          mask_surf = pygame.Surface(img.get_size(), pygame.SRCALPHA)

          for x, y in mask_outline:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                              mask_surf.set_at((x + dx, y + dy), outline_color)

          outlined_img = img.copy()
          outlined_img.blit(mask_surf, (0, 0))
          outlined_img.blit(img)
          return outlined_img


def create_weapon_settings(res, vel, spread, reload_time, fire_rate, clip_size, lifetime, lifetime_randomness,
                           damage, distance_parrallel, distance_perpendicular, friction, animation_speed, spread_time,
                           pierce, shake_mag, shake_duration, shots, gun_image, bullet_image):
          return {
                    "res": res,
                    "vel": vel,
                    "spread": spread,
                    "reload_time": reload_time,
                    "fire_rate": fire_rate,
                    "clip_size": clip_size,
                    "lifetime": lifetime,
                    "lifetime_randomness": lifetime_randomness,
                    "damage": damage,
                    "distance_parrallel": distance_parrallel,
                    "distance_perpendicular": distance_perpendicular,
                    "friction": friction,
                    "animation_speed": animation_speed,
                    "spread_time": spread_time,
                    "pierce": pierce,
                    "shake_mag": shake_mag,
                    "shake_duration": shake_duration,
                    "shots": shots,
                    "gun_image": gun_image,
                    "bullet_image": bullet_image
          }


def create_button_settings(name, pos, res=(46, 15), axis="y", axisl="max", text_pos="center", image=None):
          dictionary = {
                    "name": name,
                    "pos": pos,
                    "res": res,
                    "axis": axis,
                    "axisl": axisl,
                    "text_pos": text_pos
          }
          if image is not None: dict["image"] = image
          return dictionary


def create_spark_settings(spread, size, colour, amount):
          return {
                    "spread": spread,
                    "size": size,
                    "colour": colour,
                    "amount": amount
          }


def create_enemy_settings(name, health, res, vel, damage, stopping_distance,
                          steering_strength, friction, image, animation_speed=5):
          return {
                    'name': name,
                    'health': health,
                    'res': res,
                    'vel': vel,
                    'damage': damage,
                    'stopping_distance': stopping_distance,
                    'steering_strength': steering_strength,
                    'friction': friction,
                    'animation_speed': animation_speed,
                    "image": image
          }
