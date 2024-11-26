from functools import wraps
import functools
import pygame, os, random
import numpy as np
import pandas as pd
import pygame

def import_SpriteSheet(filename, px, py, tw, th, tiles, res=None, *color_keys):
    sheet = load_image(filename, None, *color_keys)
    array = []
    for i in range(tiles):
        cropped = pygame.Surface((tw, th), pygame.SRCALPHA)
        cropped.blit(sheet, (0, 0), (px + tw * i, py, tw, th))
        if res:
            cropped = pygame.transform.scale(cropped, res)
        array.append(cropped)
    return array

def random_xy(rect1, rect2, sprite_width, sprite_height):
          while True:
                    x = random.randint(rect1.left, rect1.right - sprite_width)
                    y = random.randint(rect1.top, rect1.bottom - sprite_height)
                    if not rect2.collidepoint(x, y): return x, y

def change_random(number, diff):
          diff = random.random() * diff
          if random.randint(0, 1) == 0: return number - diff
          else: return number + diff

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
    if res:
        img = pygame.transform.scale(img, res)
    for color_key in color_keys:
        img.set_colorkey(color_key)
    return img

@functools.lru_cache(maxsize=None)
def cached_load(file_path, res=None, *color_keys):
    return load_image(file_path, res, *color_keys)

def cached_import_gif(file_name, res=None, *color_keys):
    file_paths = [os.path.join(file_name, f) for f in os.listdir(file_name) if f.endswith(('.jpg', '.png'))]
    return [cached_load(file_path, res, *color_keys) for file_path in file_paths]