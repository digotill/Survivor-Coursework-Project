from functools import wraps
import pygame, os, random

def import_gif(file_name, res=None, *args):
          array = []
          for root, dirs, files in os.walk(file_name):
                    for file in files:
                              if file.endswith('.jpg') or file.endswith('.png'):
                                        img = pygame.image.load(
                                                  file_name + "\\" + str(os.path.basename(file))).convert_alpha()
                                        if not (res is None):
                                                  img = pygame.transform.scale(img, res)
                                        for a in args:
                                                  img.set_colorkey(a)
                                        array.append(img)
          return array


def import_SpriteSheet(filename, px, py, tw, th, tiles):
          sheet = pygame.image.load(filename).convert_alpha()
          array = []
          cropped = pygame.Surface((tw, th))
          for i in range(tiles):
                    cropped.blit(sheet, (0, 0), (px + tw * i, py, tw, th))
                    cropped.set_colorkey((0, 0, 0))
                    array.append(cropped)
                    cropped = pygame.Surface((tw, th))
          return array


def random_xy(rect1, rect2, sprite_width, sprite_height):
          while True:
                    x = random.randint(rect1.left, rect1.right - sprite_width)
                    y = random.randint(rect1.top, rect1.bottom - sprite_height)

                    if not rect2.collidepoint(x, y):
                              return x, y


def memoize(func):
          cache = {}

          @wraps(func)
          def wrapper(*args, **kwargs):
                    key = str(*args) + str(kwargs)

                    if key not in cache:
                              cache[key] = func(*args, **kwargs)

                    return cache[key]

          return wrapper


def load(filename, res=None, *args):
          image = pygame.image.load("Assets\\" + filename).convert_alpha() if res is None else pygame.transform.scale(
                    pygame.image.load("Assets\\" + filename).convert_alpha(), res)
          for a in args: image.set_colorkey(a)
          return image

def change_random(number, diff):
          random_diff = random.uniform(0, diff)
          if random.randint(0, 1) == 0: return number - random_diff
          else: return number + random_diff
