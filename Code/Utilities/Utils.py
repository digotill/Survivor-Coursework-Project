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


def change_by_diff(number, diff):
          diff = random.random() * diff
          if random.randint(0, 1) == 0:
                    return number - diff
          else:
                    return number + diff


def change_by_random(number, amount):
          if random.random() < 0.5:
                    return number - random.randint(0, amount)
          else:
                    return number + random.randint(0, amount)


def load_image(file_path, res=None, *color_keys):
          img = pygame.image.load(file_path).convert_alpha()
          if res: img = pygame.transform.scale(img, res)
          for color_key in color_keys: img.set_colorkey(color_key)
          return img


@functools.lru_cache(maxsize=None)
def cached_load(file_path, res=None, *color_keys):
          return load_image(file_path, res, *color_keys)




def import_4x4_spritesheet(filename, tile_size=16, res=None, *colour_keys):
          sheet = cached_load(filename, None, *colour_keys)
          tiles = []
          x_tiles, y_tiles = 4, 4
          for y in range(4):
                    for x in range(4):
                              tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                              tile.blit(sheet, (0, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
                              if res:
                                        tile = pygame.transform.scale(tile, res)
                              tiles.append(tile)
          return {
                    "topleft": [tiles[0]],
                    "topright": [tiles[x_tiles - 1]],
                    "bottomleft": [tiles[x_tiles * (y_tiles - 1)]],
                    "bottomright": [tiles[-1]],
                    "top": tiles[1:x_tiles - 1],
                    "right": [tiles[i * x_tiles + x_tiles - 1] for i in range(1, y_tiles - 1)],
                    "bottom": tiles[x_tiles * (y_tiles - 1) + 1: -1],
                    "left": [tiles[i * x_tiles] for i in range(1, y_tiles - 1)],
          }


def import_2d_spritesheet(filename, x_tiles, y_tiles, tile_size=16, res=None, *colour_keys):
          sheet = cached_load(filename, None, *colour_keys)
          tiles = []
          for y in range(y_tiles):
                    for x in range(x_tiles):
                              tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                              tile.blit(sheet, (0, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
                              if res:
                                        tile = pygame.transform.scale(tile, res)
                              tiles.append(tile)
          return tiles


def import_2x2_spritesheet(filename, tile_size=16, res=None, *colour_keys):
          sheet = cached_load(filename, None, *colour_keys)
          tiles = []
          for y in range(2):
                    for x in range(2):
                              tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                              tile.blit(sheet, (0, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
                              if res:
                                        tile = pygame.transform.scale(tile, res)
                              tiles.append(tile)
          return {
                    "bottomright": [tiles[0]],
                    "bottomleft": [tiles[1]],
                    "topright": [tiles[2]],
                    "topleft": [tiles[3]],
          }


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


def lookup_colour(colour):
          color_list = [(c, v) for c, v in pygame.color.THECOLORS.items() if colour in c]
          for colour in color_list: print(colour)


def normalize(val, amt, target):
          if val > target + amt:
                    val -= amt
          elif val < target - amt:
                    val += amt
          else:
                    val = target
          return val


def remove_string(main_string, string_to_remove):
          return main_string.replace(string_to_remove, '')


def string_ends_with(main_string, ending):
          return main_string.endswith(ending)


def remove_opposite_directions(direction_string):
          opposite_pairs = [("top", "bottom"), ("left", "right")]
          result = direction_string.lower()

          for pair in opposite_pairs:
                    if all(direction in result for direction in pair):
                              result = result.replace(pair[0], "").replace(pair[1], "")

          return result if result else direction_string


def create_weapon_settings(res, vel, spread, reload_time, fire_rate, clip_size, lifetime, lifetime_randomness,
                           damage, distance, friction, animation_speed, spread_time,
                           pierce, shake_mag, shake_duration, shots, gun_image, bullet_image, name):
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
                    "distance": distance,
                    "friction": friction,
                    "animation_speed": animation_speed,
                    "spread_time": spread_time,
                    "pierce": pierce,
                    "shake_mag": shake_mag,
                    "shake_duration": shake_duration,
                    "shots": shots,
                    "gun_image": pygame.transform.scale(gun_image, res),
                    "bullet_image": bullet_image,
                    "name": name
          }


def create_button(text_input, pos, image, res=(46, 15), axis="y", axisl="max", text_pos="center", speed=900,
                  base_colour=(255, 255, 255),
                  hovering_colour=(255, 0, 0), hover_slide=True, hover_offset=10, hover_speed=20,
                  current_hover_offset=0, active=False, on=False):
          return {
                    "text_input": text_input,
                    "pos": pos,
                    "res": res,
                    "axis": axis,
                    "axisl": axisl,
                    "text_pos": text_pos,
                    "image": image,
                    "speed": speed,
                    "base_colour": base_colour,
                    "hovering_colour": hovering_colour,
                    "hover_slide": hover_slide,
                    "hover_offset": hover_offset,
                    "hover_speed": hover_speed,
                    "current_hover_offset": current_hover_offset,
                    "active": active,
                    "on": on
          }


def create_slider(pos, image, text_input, min_value, max_value, initial_value, axis="y", axisl="max", text_pos="right",
                  circle_base_colour=(255, 255, 255), circle_hovering_color=(255, 0, 0), speed=900,
                  hover_slide=False, hover_offset=10, hover_speed=20, current_hover_offset=0, active=False,
                  res=(46, 15), base_colour=(255, 255, 255),
                  is_dragging=False, line_colour=(120, 120, 120), line_thickness=2):
          return {
                    "text_input": text_input,
                    "pos": pos,
                    "image": image,
                    "min_value": min_value,
                    "max_value": max_value,
                    "value": initial_value,
                    "axis": axis,
                    "axisl": axisl,
                    "text_pos": text_pos,
                    "circle_base_colour": circle_base_colour,
                    "circle_hovering_colour": circle_hovering_color,
                    "speed": speed,
                    "hover_slide": hover_slide,
                    "hover_offset": hover_offset,
                    "hover_speed": hover_speed,
                    "current_hover_offset": current_hover_offset,
                    "active": active,
                    "res": res,
                    "base_colour": base_colour,
                    "is_dragging": is_dragging,
                    "line_colour": line_colour,
                    "line_thickness": line_thickness
          }


def create_spark_settings(spread, scale, colour, amount, min_vel, max_vel):
          return {
                    "spread": spread,
                    "scale": scale,
                    "colour": colour,
                    "amount": amount,
                    "min_vel": min_vel,
                    "max_vel": max_vel,
          }


def create_enemy_settings(name, health, res, vel, damage, stopping_distance,
                          steering_strength, friction, images, animation_speed, hit_cooldown):
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
                    "images": images,
                    "hit_cooldown": hit_cooldown,
                    "separation_radius": res[0],
                    "separation_strength": 0.5,
          }


def create_object_settings(images, res, amount, collision):
          return {
                    'images': images,
                    'res': res,
                    'amount': amount,
                    'collision': collision,
          }
