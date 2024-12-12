from Code.Classes.Entities import *


class Window(main):
          def __init__(self, game):
                    self.game = game
                    self.res = REN_RES

                    self.set_attributes(Window_Attributes)

                    self.v_ = v2(GAME_SIZE[0] / 2 - self.res[0] / 2, GAME_SIZE[1] / 2 - self.res[1] / 2)
                    self.pos = self.v_
                    self.rect = pygame.Rect(self.pos.x, self.pos.y, self.res[0], self.res[1])
                    self.offset_rect = self.rect.copy()


          def move(self, dx, dy, move_horizontally, move_vertically):

                    new_x = self.pos.x + dx * self.game.player.current_vel * self.game.dt
                    new_y = self.pos.y + dy * self.game.player.current_vel * self.game.dt

                    mouse_target = v2(self.game.correct_mouse_pos[0] - 0.5 * REN_RES[0],
                                      self.game.correct_mouse_pos[1] - 0.5 * REN_RES[1])

                    self.mouse_smoothing = v2(
                              self.lerp(self.mouse_smoothing.x, mouse_target.x,
                                        self.window_mouse_smoothing_amount * self.game.dt),
                              self.lerp(self.mouse_smoothing.y, mouse_target.y,
                                        self.window_mouse_smoothing_amount * self.game.dt))

                    if abs(self.mouse_smoothing.x) < self.deadzone:
                              self.mouse_smoothing.x = 0
                    if abs(self.mouse_smoothing.y) < self.deadzone:
                              self.mouse_smoothing.y = 0

                    self.target_offset.x = self.window_max_offset * int(self.mouse_smoothing.x)
                    self.target_offset.y = self.window_max_offset * int(self.mouse_smoothing.y)

                    self.current_offset = v2(
                              self.lerp(self.current_offset.x, self.target_offset.x, self.lerp_speed * self.game.dt),
                              self.lerp(self.current_offset.y, self.target_offset.y, self.lerp_speed * self.game.dt))

                    rounded_offset = v2(round(self.current_offset.x), round(self.current_offset.y))

                    if (move_horizontally and 0 < new_x < GAME_SIZE[0] - self.res[0] and
                            self.res[0] / 2 < self.game.player.pos.x < GAME_SIZE[0] - self.res[0] / 2):
                              self.pos.x = new_x
                    if (move_vertically and 0 < new_y < GAME_SIZE[1] - self.res[1] and
                            self.res[1] / 2 < self.game.player.pos.y < GAME_SIZE[1] - self.res[1] / 2):
                              self.pos.y = new_y

                    if 0 < self.pos.x + rounded_offset.x < GAME_SIZE[0] - self.res[0]:
                              self.offset_rect.x = self.pos.x + rounded_offset.x
                    if 0 < self.pos.y + rounded_offset.y < GAME_SIZE[1] - self.res[1]:
                              self.offset_rect.y = self.pos.y + rounded_offset.y

                    shake_offset = self.calculate_shake()

                    self.offset_rect.x = max(0, min(self.pos.x + rounded_offset.x + shake_offset.x,
                                                    GAME_SIZE[0] - self.res[0]))
                    self.offset_rect.y = max(0, min(self.pos.y + rounded_offset.y + shake_offset.y,
                                                    GAME_SIZE[1] - self.res[1]))

                    player_left = self.game.player.pos.x - self.offset_rect.x - self.game.player.res[0] / 2
                    player_right = player_left + self.game.player.res[0]
                    player_top = self.game.player.pos.y - self.offset_rect.y - self.game.player.res[1] / 2
                    player_bottom = player_top + self.game.player.res[1]

                    if player_left < self.game.player.offset_x1:
                              self.offset_rect.x += player_left - self.game.player.offset_x1
                    elif player_right > self.res[0] - self.game.player.offset_x2:
                              self.offset_rect.x += player_right - (self.res[0] - self.game.player.offset_x2)

                    if player_top < self.game.player.offset_y1:
                              self.offset_rect.y += player_top - self.game.player.offset_y1
                    elif player_bottom > self.res[1] - self.game.player.offset_y2:
                              self.offset_rect.y += player_bottom - (self.res[1] - self.game.player.offset_y2)

                    self.offset_rect.x = max(0, min(self.offset_rect.x, GAME_SIZE[0] - self.res[0]))
                    self.offset_rect.y = max(0, min(self.offset_rect.y, GAME_SIZE[1] - self.res[1]))

          def calculate_shake(self):
                    current_time = pygame.time.get_ticks()
                    elapsed_time = (current_time - self.shake_start_time) / 1000.0

                    if elapsed_time > self.shake_duration:
                              self.shake_duration = 0
                              return v2(0, 0)

                    fade_out = 1 - (elapsed_time / self.shake_duration)
                    sin_value = math.sin(self.shake_speed * (self.shake_seed + elapsed_time))

                    noise_x = self.get_2d_noise(self.shake_seed + elapsed_time, 0)
                    noise_y = self.get_2d_noise(0, self.shake_seed + elapsed_time)
                    noise_offset = v2(noise_x, noise_y)

                    direction = (
                            self.shake_direction + noise_offset * self.reduced_screen_shake).normalize()

                    shake_offset = direction * sin_value * self.shake_magnitude * fade_out
                    return v2(int(shake_offset.x), int(shake_offset.y))

          @staticmethod
          def get_2d_noise(x, y):
                    scaled_x, scaled_y = x * 0.1, y * 0.1
                    return Perlin_Noise["perlin"]([scaled_x, scaled_y])

          def add_screen_shake(self, duration, magnitude):
                    self.shake_duration = duration
                    self.shake_magnitude = magnitude
                    self.shake_start_time = pygame.time.get_ticks()
                    self.shake_seed = self.game.game_time
                    self.shake_direction = v2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

          @staticmethod
          def lerp(start, end, amount):
                    return start + (end - start) * amount
