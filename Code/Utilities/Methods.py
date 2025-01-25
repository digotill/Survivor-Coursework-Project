import functools, math, os, random, pygame

class Methods:
          def __init__(self):
                    self.button_config = {
                              "button": {"res": (46, 15), "axis": "y", "axisl": "max", "text_pos": "center", "speed": 1500, "base_colour": (255, 255, 255), "distance_factor": 0.3,
                                         "hovering_colour": (85, 107, 47), "hover_slide": True, "hover_offset": 15, "hover_speed": 30, "on": False, "active": False, "current_hover_offset": 0,
                                         },
                              "slider": {"res": (46, 15), "axis": "y", "axisl": "max", "text_pos": "right", "speed": 1500, "base_colour": (255, 255, 255), "distance_factor": 0.3,
                                         "circle_base_colour": (255, 255, 255), "circle_hovering_colour": (255, 0, 0), "hover_slide": False, "hover_offset": 15, "hover_speed": 30,
                                         "line_thickness": 2, "line_colour": (120, 120, 120), "on": False, "active": False, "current_hover_offset": 0,
                                         }
                    }

          @staticmethod
          def get_transparent_image(image, alpha):
                    transparent_image = image.copy()
                    transparent_image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
                    return transparent_image

          @staticmethod
          def get_shadow_image(self, image):
                    shadow_image = self.game.assets["shadow"].copy()
                    return pygame.transform.scale(shadow_image, (image.width, shadow_image.height))

          @staticmethod
          def get_image_outline(img, outline_color=(255, 255, 255)):
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

          @staticmethod
          def lerp(start, end, amount):
                    return start + (end - start) * amount

          @staticmethod
          def normalize(val, amt, target):
                    if val > target + amt:
                              val -= amt
                    elif val < target - amt:
                              val += amt
                    else:
                              val = target
                    return val

          @staticmethod
          def change(number, diff):
                    return number + random.uniform(-diff, diff)

          @staticmethod
          def lookup_colour(colour):
                    color_list = [(c, v) for c, v in pygame.color.THECOLORS.items() if colour in c]
                    for colour in color_list: print(colour)

          def rename_files_recursive(self, directory):
                    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')

                    for root, _, files in os.walk(directory):
                              for filename in files:
                                        if filename.lower().endswith(image_extensions):
                                                  old_path = os.path.join(root, filename)
                                                  new_filename = filename.lower().replace(' ', '_')

                                                  # Remove '_1' suffix if present
                                                  base, ext = os.path.splitext(new_filename)
                                                  if base.endswith('_1'):
                                                            new_filename = f"{base[:-2]}{ext}"

                                                  if filename != new_filename:
                                                            new_path = os.path.join(root, new_filename)
                                                            new_path = self.get_unique_filename(new_path)

                                                            try:
                                                                      os.rename(old_path, new_path)
                                                                      print(f"Renamed: {old_path} -> {new_path}")
                                                            except OSError as e:
                                                                      print(f"Error renaming {old_path}: {e}")

          @staticmethod
          def get_unique_filename(path):
                    root, ext = os.path.splitext(path)
                    counter = 1
                    while os.path.exists(path):
                              path = f"{root}_{counter}{ext}"
                              counter += 1
                    return path

          def create_button(self, text_input, pos, image, dictionary2=None):
                    value = {
                              "text_input": text_input,
                              "pos": pos,
                              "image": image,
                    }
                    value.update(self.button_config["button"])
                    if dictionary2 is not None:
                              value.update(dictionary2)
                    return value

          def create_slider(self, pos, text_input, min_value, max_value, initial_value, image, dictionary2=None):
                    value = {
                              "text_input": text_input,
                              "pos": pos,
                              "min_value": min_value,
                              "max_value": max_value,
                              "value": initial_value,
                              "image": image,
                    }
                    value.update(self.button_config["slider"])
                    if dictionary2 is not None:
                              value.update(dictionary2)
                    return value

          @staticmethod
          def set_attributes(object1, attributes):
                    for key, value in attributes.items():
                              setattr(object1, key, value)

          @staticmethod
          def set_rect(self):
                    self.rect = pygame.Rect(self.pos.x - self.res[0] / 2, self.pos.y - self.res[1] / 2, self.res[0],
                                            self.res[1])
