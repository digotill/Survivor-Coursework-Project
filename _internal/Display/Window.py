import pygame, math
from _internal.Variables.Variables import *
from pygame.math import Vector2 as v2
from _internal.Classes.Entities import *


class Window(RectEntity):
        def __init__(self, game, res, big_res, name=None, angle=30):
            RectEntity.__init__(self, game, (big_res[0] / 2 - res[0] / 2, big_res[1] / 2 - res[1] / 2), res, PLAYER_VEL, name, angle)
            self.offset_rect = pygame.Rect(self.pos.x, self.pos.y, self.res[0], self.res[1])
            self.little_offset_rect = self.offset_rect.copy()
            self.target_offset = v2(0, 0)
            self.current_offset = v2(0, 0)
            self.lerp_speed = WINDOW_LERP_SPEED
            self.mouse_smoothing = v2(0, 0)
            self.deadzone = 3

        def move(self):
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
                    self.lerp(self.mouse_smoothing.y, mouse_target.y, 0.1)
        )

            if abs(self.mouse_smoothing.x) < self.deadzone:
                    self.mouse_smoothing.x = 0
            if abs(self.mouse_smoothing.y) < self.deadzone:
                    self.mouse_smoothing.y = 0

            self.target_offset.x = WINDOW_MAX_OFFSET * int(self.mouse_smoothing.x)
            self.target_offset.y = WINDOW_MAX_OFFSET * int(self.mouse_smoothing.y)

            self.current_offset = v2(
                    self.lerp(self.current_offset.x, self.target_offset.x, self.lerp_speed),
                    self.lerp(self.current_offset.y, self.target_offset.y, self.lerp_speed))

            rounded_offset = v2(round(self.current_offset.x), round(self.current_offset.y))

            if self.res[0] / 2 < self.game.player.pos.x < self.game.big_window[0] - self.res[0] / 2:
                    self.pos.x = new_x
                    self.rect.x = self.pos.x
                    self.offset_rect.x = self.rect.x + rounded_offset.x
            if self.res[1] / 2 < self.game.player.pos.y < self.game.big_window[1] - self.res[1] / 2:
                    self.pos.y = new_y
                    self.rect.y = self.pos.y
                    self.offset_rect.y = self.rect.y + rounded_offset.y

        @staticmethod
        def lerp(start, end, amount):
                return start + (end - start) * amount
