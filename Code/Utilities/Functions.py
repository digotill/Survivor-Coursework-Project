import functools, math, os, random, pygame


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


def get_unique_filename(path):
          root, ext = os.path.splitext(path)
          counter = 1
          while os.path.exists(path):
                    path = f"{root}_{counter}{ext}"
                    counter += 1
          return path


def rename_files_recursive(directory):
          for root, dirs, files in os.walk(directory):
                    for filename in files:
                              if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                                        new_filename = filename.lower().replace(' ', '_')
                                        if filename != new_filename:
                                                  old_path = os.path.join(root, filename)
                                                  new_path = os.path.join(root, new_filename)
                                                  if os.path.exists(new_path):
                                                            new_path = get_unique_filename(new_path)
                                                  os.rename(old_path, new_path)
                                                  print(f"Renamed: {old_path} -> {new_path}")
          for root, dirs, files in os.walk(directory):
                    for filename in files:
                              if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                                        base, ext = os.path.splitext(filename)
                                        if base.endswith('_1'):
                                                  new_base = base[:-2]  # Remove the last two characters ('_1')
                                                  new_filename = f"{new_base}{ext}"
                                                  old_path = os.path.join(root, filename)
                                                  new_path = os.path.join(root, new_filename)

                                                  if not os.path.exists(new_path):
                                                            os.rename(old_path, new_path)
                                                            print(f"Renamed: {old_path} -> {new_path}")
                                                  else:
                                                            print(f"Skipped: {old_path} (Target name already exists)")


Button_config = {
          "button": {"res": (46, 15), "axis": "y", "axisl": "max", "text_pos": "center", "speed": 1500, "base_colour": (255, 255, 255), "distance_factor": 0.3,
                     "hovering_colour": (85, 107, 47), "hover_slide": True, "hover_offset": 15, "hover_speed": 30, "on": False, "active": False, "current_hover_offset": 0,
                     },
          "slider": {"res": (46, 15), "axis": "y", "axisl": "max", "text_pos": "right", "speed": 1500, "base_colour": (255, 255, 255), "distance_factor": 0.3,
                     "circle_base_colour": (255, 255, 255), "circle_hovering_colour": (255, 0, 0), "hover_slide": False, "hover_offset": 15, "hover_speed": 30,
                     "line_thickness": 2, "line_colour": (120, 120, 120), "on": False, "active": False, "current_hover_offset": 0,
                     }
}


def create_button(text_input, pos, image, dictionary2=None):
          value = {
                    "text_input": text_input,
                    "pos": pos,
                    "image": image,
          }
          value.update(Button_config["button"])
          if dictionary2 is not None:
                    value.update(dictionary2)
          return value


def create_slider(pos, text_input, min_value, max_value, initial_value, image, dictionary2=None):
          value = {
                    "text_input": text_input,
                    "pos": pos,
                    "min_value": min_value,
                    "max_value": max_value,
                    "value": initial_value,
                    "image": image,
          }
          value.update(Button_config["slider"])
          if dictionary2 is not None:
                    value.update(dictionary2)
          return value
