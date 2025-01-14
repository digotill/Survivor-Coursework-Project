import pygame
import os
from PIL import Image
import io


class AssetManager:
          def __init__(self):
                    self.assets = {}
                    self.load_all_assets()

          def load_all_assets(self):
                    assets_dir = "New Assets"
                    for root, dirs, files in os.walk(assets_dir):
                              for file in files:
                                        file_path = os.path.join(root, file)
                                        file_name, file_ext = os.path.splitext(file)

                                        if "tileset" in file_name.lower():
                                            self.import_tileset(file_path, file_name)
                                        elif file_ext.lower() in ['.png', '.jpg', '.jpeg']:
                                                  self.load_image(file_path, file_name)
                                        elif file_ext.lower() == '.gif':
                                                  self.import_gif(file_path, file_name)
                                        elif file_ext.lower() in ['.wav', '.ogg', '.mp3']:
                                                  self.load_sound(file_path, file_name)
                                        elif file_ext.lower() in ['.ttf']:
                                                  self.load_font(file_path, file_name)

          def import_gif(self, path, name):
                    frames = []
                    with Image.open(path) as gif:
                              for frame_index in range(gif.n_frames):
                                        gif.seek(frame_index)
                                        frame_rgba = gif.convert("RGBA")
                                        pygame_image = pygame.image.fromstring(
                                                  frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
                                        )
                                        frames.append(pygame_image)
                    self.assets[name] = frames

          def load_image(self, file_path, name, res=None, *color_keys):
                    img = pygame.image.load(file_path).convert_alpha()
                    if res:
                              img = pygame.transform.scale(img, res)
                    for color_key in color_keys:
                              img.set_colorkey(color_key)
                    self.assets[name] = img

          def load_sound(self, file_path, name):
                    sound = pygame.mixer.Sound(file_path)
                    self.assets[name] = sound

          def import_tileset(self, filepath, name):
                    tileset_image = pygame.image.load(filepath).convert_alpha()
                    tile = pygame.Surface((16, 16), pygame.SRCALPHA)
                    array = ["0202", "2210", "2121", "0122", "2222", "2112", "1111", "1221", "2020", "1022", "1212", "2201", "0000", "0220", "2222", "2002"]
                    dictionary = {}
                    count = 0
                    for i in range(4):
                              for j in range(4):
                                        tile.blit(tileset_image, (0, 0), (i * 16, j * 16, 16, 16))
                                        dictionary[array[count]] = tile.copy()
                                        count += 1
                    array = ["1000", "0100", "0010", "0001"]
                    count = 0
                    for i in range(4):
                              tile.blit(tileset_image, (0, 0), (16 * 2, 16 * 1, 16, 16))
                              dictionary[array[count]] = tile.copy()
                              count += 1
                    self.assets[name] = dictionary

          def load_font(self, file_path, name):
                    self.assets[name] = pygame.font.Font(file_path, int(name[4:]))
