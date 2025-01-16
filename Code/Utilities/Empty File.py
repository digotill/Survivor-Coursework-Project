# CTRL E for recent stuff
# CTRL W for delete word
# Double shift to find text
# CTRL + SHIFT + F to find in all files
# Double click CTRL to run
# SHIFT + F6 to rename
# CTRL + ALT + L to reformat code


import os


def rename_images_to_lowercase_and_underscore(directory):
          for filename in os.listdir(directory):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                              new_filename = filename.lower().replace(' ', '_')
                              if filename != new_filename:
                                        old_path = os.path.join(directory, filename)
                                        new_path = os.path.join(directory, new_filename)
                                        os.rename(old_path, new_path)
                                        print(f"Renamed: {filename} -> {new_filename}")


# Replace 'path_to_your_image_directory' with the actual path to your image directory
image_directory = r"C:\Users\digot\PycharmProjects\Survivor\Assets\VFX"
rename_images_to_lowercase_and_underscore(image_directory)
