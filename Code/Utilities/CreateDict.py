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


def create_button(text_input, pos, dictionary, dictionary2=None):
          value = {
                    "text_input": text_input,
                    "pos": pos,
          }
          value.update(dictionary)
          if dictionary2 is not None:
                    value.update(dictionary2)
          return value


def create_slider(pos, text_input, min_value, max_value, initial_value, dictionary, dictionary2=None):
          value = {
                    "text_input": text_input,
                    "pos": pos,
                    "min_value": min_value,
                    "max_value": max_value,
                    "value": initial_value,
          }
          value.update(dictionary)
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
