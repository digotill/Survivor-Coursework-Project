def create_weapon_settings(vel, spread, reload_time, fire_rate, clip_size, lifetime, lifetime_randomness,
                           damage, distance, friction, animation_speed, spread_time,
                           pierce, shots, name):
          return {
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
                    "shots": shots,
                    "name": name
          }


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


def create_spark_settings(spread, scale, colour, amount, min_vel, max_vel):
          return {
                    "spread": spread,
                    "scale": scale,
                    "colour": colour,
                    "amount": amount,
                    "min_vel": min_vel,
                    "max_vel": max_vel,
          }


def create_enemy_settings(name, health, vel, damage, stopping_distance,
                          steering_strength, friction, animation_speed, hit_cooldown, separation_radius, separation_strength):
          return {
                    'name': name,
                    'health': health,
                    'vel': vel,
                    'damage': damage,
                    'stopping_distance': stopping_distance,
                    'steering_strength': steering_strength,
                    'friction': friction,
                    'animation_speed': animation_speed,
                    "hit_cooldown": hit_cooldown,
                    "separation_radius": separation_radius,
                    "separation_strength": separation_strength,
          }
