import pygame, math, random
from Code.Variables.Variables import *
from pygame.math import Vector2 as v2
from Code.Classes.Entities import *

class Window(RectEntity):
        def __init__(self, game, res, big_res, name=None, angle=30):
                    RectEntity.__init__(self, game, (big_res[0] / 2 - res[0] / 2, big_res[1] / 2 - res[1] / 2), res, 0, name, angle)
                    self.offset_rect = pygame.Rect(self.pos.x, self.pos.y, self.res[0], self.res[1])
                    self.little_offset_rect = self.offset_rect.copy()
                    self.target_offset = v2(0, 0)
                    self.current_offset = v2(0, 0)
                    self.lerp_speed = WINDOW_LERP_SPEED
                    self.mouse_smoothing = v2(0, 0)
                    self.deadzone = WINDOW_DEADZONE
                    self.shake_duration = 0
                    self.shake_start_time = 0
                    self.shake_magnitude = 0
                    self.shake_speed = WINDOW_SHAKE_SPEED
                    self.shake_seed = random.random() * WINDOW_SHAKE_SEED
                    self.shake_direction = v2(WINDOW_SHAKE_DIRECTION)
                    self.shake_noise_magnitude = WINDOW_SHAKE_NOISE_MAGNITUDE
                    self.current_rounded_offset = v2(0, 0)
                    self.max_window_offset = WINDOW_MAX_OFFSET

        def move(self, move_horizontal, move_vertical):
            a = self.game.keys[pygame.K_a]
            d = self.game.keys[pygame.K_d]
            w = self.game.keys[pygame.K_w]
            s = self.game.keys[pygame.K_s]

            dx, dy = 0, 0
            if a: dx -= 1
            if d: dx += 1
            if s: dy += 1
            if w: dy -= 1

            magnitude = math.sqrt(dx ** 2 + dy ** 2)
            if magnitude != 0:
                    dx /= magnitude
                    dy /= magnitude

            new_x = self.pos.x + dx * self.game.player.current_vel * self.game.dt
            new_y = self.pos.y + dy * self.game.player.current_vel * self.game.dt

            mouse_target = v2(self.game.correct_mouse_pos[0] - 0.5 * REN_RES[0],
                    self.game.correct_mouse_pos[1] - 0.5 * REN_RES[1])
            self.mouse_smoothing = v2(
                    self.lerp(self.mouse_smoothing.x, mouse_target.x, 0.1),
                    self.lerp(self.mouse_smoothing.y, mouse_target.y, 0.1))

            if abs(self.mouse_smoothing.x) < self.deadzone:
                    self.mouse_smoothing.x = 0
            if abs(self.mouse_smoothing.y) < self.deadzone:
                    self.mouse_smoothing.y = 0

            self.target_offset.x = self.max_window_offset * int(self.mouse_smoothing.x)
            self.target_offset.y = self.max_window_offset * int(self.mouse_smoothing.y)

            self.current_offset = v2(
                    self.lerp(self.current_offset.x, self.target_offset.x, self.lerp_speed),
                    self.lerp(self.current_offset.y, self.target_offset.y, self.lerp_speed))

            self.current_rounded_offset = v2(round(self.current_offset.x), round(self.current_offset.y))

            if move_horizontal: self.pos.x = new_x
            if move_vertical: self.pos.y = new_y

            if 0 < self.pos.x < self.game.big_window[0] - self.res[0]:
                    if 0 < self.pos.x + self.current_rounded_offset.x < self.game.big_window[0] - self.res[0]:
                              self.offset_rect.x = self.pos.x + self.current_rounded_offset.x
            if 0 < self.pos.y < self.game.big_window[1] - self.res[1]:
                    if 0 < self.pos.y + self.current_rounded_offset.y < self.game.big_window[1] - self.res[1]:
                              self.offset_rect.y = self.pos.y + self.current_rounded_offset.y

            if self.shake_duration > 0:
                      shake_offset = self.calculate_shake()
                      self.offset_rect.x += shake_offset.x
                      self.offset_rect.y += shake_offset.y

            print(self.pos )

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

                  direction = (self.shake_direction + noise_offset * self.shake_noise_magnitude).normalize()

                  shake_offset = direction * sin_value * self.shake_magnitude * fade_out
                  return v2(int(shake_offset.x), int(shake_offset.y))

        @staticmethod
        def get_2d_noise(x, y):

                  def fade(t):
                            return t * t * t * (t * (t * 6 - 15) + 10)

                  def lerp(t, a_, b_):
                            return a_ + t * (b_ - a_)

                  def grad(hash_, x_, y_):
                            h = hash_ & 15

                            grad_x = 1 if h < 8 else -1
                            grad_y = 1 if h < 4 else -1 if h in [12, 13] else 0
                            return grad_x * x_ + grad_y * y_

                  p = [151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225,
                       140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148,
                       247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32,
                       57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175,
                       74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111, 229, 122,
                       60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54,
                       65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169,
                       200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64,
                       52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212,
                       207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213,
                       119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
                       129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104,
                       218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241,
                       81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157,
                       184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205, 93,
                       222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180]

                  p += p
                  x, y = int(x * 255), int(y * 255)
                  xi, yi = x & 255, y & 255
                  xf, yf = x - xi, y - yi
                  u, v = fade(xf), fade(yf)

                  a = p[xi] + yi
                  aa = p[a]
                  ab = p[a + 1]
                  b = p[xi + 1] + yi
                  ba = p[b]
                  bb = p[b + 1]

                  x1 = lerp(u, grad(p[aa], xf, yf), grad(p[ba], xf - 1, yf))
                  x2 = lerp(u, grad(p[ab], xf, yf - 1), grad(p[bb], xf - 1, yf - 1))
                  return lerp(v, x1, x2)

        def add_screen_shake(self, duration, magnitude):
                  self.shake_duration = duration
                  self.shake_magnitude = magnitude
                  self.shake_start_time = pygame.time.get_ticks()
                  self.shake_seed = random.random() * 1000
                  self.shake_direction = v2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

        @staticmethod
        def lerp(start, end, amount):
                return start + (end - start) * amount
