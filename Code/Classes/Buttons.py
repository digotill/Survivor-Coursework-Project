from pygame.math import Vector2 as v2

from Code.Variables.Variables import *


class SlidingButtons:
          def __init__(self, game, image, pos, axis, axisl, res=PLAY_BUTTON_RES, speed=SETTINGS_BUTTON_SPEED,
                       text_input=None, font=FONT, base_colour=(255, 255, 255), hovering_colour=(255, 0, 0)):
                    self.game = game
                    self.image = pygame.transform.scale(image, res)
                    self.rect = self.image.get_rect(center=pos)
                    self.original_pos = v2(pos)
                    self.active = False
                    self.speed = speed
                    self.axis = axis
                    self.axis_location = axisl
                    self.starting_pos = self.calculate_starting_position()
                    self.current_pos = v2(self.starting_pos)
                    self.rect.center = self.current_pos
                    if text_input is not None:
                              self.has_text = True
                    else:
                              self.has_text = False
                    self.text_input = text_input
                    self.font_path = font
                    self.base_color = base_colour
                    self.hovering_color = hovering_colour
                    if self.has_text:
                              self.setup_text()

          def calculate_starting_position(self):
                    if self.axis == "x":
                              x = REN_RES[
                                            0] + self.rect.width / 2 + 1 if self.axis_location == "max" else -self.rect.width / 2 - 1
                              return x, self.original_pos.y
                    else:
                              y = REN_RES[
                                            1] + self.rect.height / 2 + 1 if self.axis_location == "max" else -self.rect.height / 2 - 1
                              return self.original_pos.x, y

          def setup_text(self):
                    self.font_size = int(self.rect.height / BUTTONS_SIZE / 1.2)
                    self.font = pygame.font.Font(self.font_path, self.font_size)
                    self.text = self.font.render(self.text_input, False, self.base_color)
                    self.text_rect = self.text.get_rect(center=self.rect.center)

          def draw(self):
                    if self.is_visible_on_screen():
                              self.game.ui_surface.blit(self.image, self.rect)
                              if self.has_text:
                                        self.game.ui_surface.blit(self.text, self.text_rect)

          def is_visible_on_screen(self):
                    screen_rect = self.game.display_screen.get_rect()
                    return self.rect.colliderect(screen_rect)

          def update(self):
                    target = self.original_pos if self.active else v2(self.starting_pos)
                    distance = (target - self.current_pos).length()
                    speed_factor = min(distance / SETTINGS_BUTTON_FRICTION, 1)

                    direction = (target - self.current_pos).normalize() if distance > 0 else v2(0, 0)
                    movement = direction * self.speed * speed_factor * self.game.dt
                    if movement.length() > distance:
                              self.current_pos = target
                    else:
                              self.current_pos += movement

                    self.rect.center = self.current_pos
                    if self.has_text:
                              self.text_rect.center = self.rect.center

          def check_for_input(self):
                    return self.rect.collidepoint(self.game.correct_mouse_pos)

          def changeColor(self):
                    if self.has_text:
                              color = self.hovering_color if self.rect.collidepoint(
                                        self.game.correct_mouse_pos) else self.base_color
                              self.text = self.font.render(self.text_input, False, color)
                              self.text_rect = self.text.get_rect(center=self.rect.center)


class NewSlider:
          def __init__(self, game, image, pos, axis, axisl, res=PLAY_BUTTON_RES, circle_radius=None,
                       speed=SETTINGS_BUTTON_SPEED, initial_value=0.5, min_value=0,
                       max_value=1, circle_base_colour=(255, 255, 255), circle_hovering_color=(255, 0, 0),
                       text_input=None, font=FONT, text_base_color=(255, 255, 255),
                       text_pos="up"):
                    self.game = game
                    self.image = pygame.transform.scale(image, res)
                    self.rect = self.image.get_rect(center=pos)
                    self.original_pos = v2(pos)
                    if circle_radius is None:
                              self.circle_radius = 0.3 * self.rect.height
                    else:
                              self.circle_radius = circle_radius
                    self.circle_base_colour = circle_base_colour
                    self.circle_hovering_color = circle_hovering_color
                    self.padding = self.circle_radius * 2
                    self.circle_surface = pygame.Surface((self.circle_radius * 2, self.circle_radius * 2))
                    self.circle_surface.set_colorkey((0, 0, 0))
                    self.current_colour = self.circle_base_colour
                    pygame.draw.circle(self.circle_surface, self.current_colour,
                                       (self.circle_radius, self.circle_radius), self.circle_radius)
                    self.max_value = max_value
                    self.min_value = min_value
                    self.value = initial_value
                    self.circle_rect = pygame.Rect(self.rect.x + self.value * self.rect.width - self.circle_radius,
                                                   self.rect.y - self.circle_radius + 0.5 * self.rect.height,
                                                   self.circle_radius * 2, self.circle_radius * 2)
                    self.active = False
                    self.speed = speed
                    self.line_color = (100, 100, 100)
                    self.line_thickness = 2
                    self.text_pos = text_pos
                    self.axis = axis
                    self.update_value = False
                    self.axis_location = axisl
                    self.is_dragging = False
                    self.starting_pos = self.calculate_starting_position()
                    self.current_pos = v2(self.starting_pos)
                    self.rect.center = self.current_pos
                    if text_input is not None:
                              self.has_text = True
                    else:
                              self.has_text = False
                    if self.has_text:
                              self.text_input = text_input
                              self.font_path = font
                              self.text_base_color = text_base_color
                              self.font = pygame.font.Font(self.font_path, int(self.rect.height / BUTTONS_SIZE / 1.2))

          def calculate_starting_position(self):
                    if self.axis == "x":
                              x = REN_RES[
                                            0] + self.rect.width / 2 + 1 if self.axis_location == "max" else -self.rect.width / 2 - 1
                              return x, self.original_pos.y
                    else:
                              y = REN_RES[
                                            1] + self.rect.height / 2 + 1 if self.axis_location == "max" else -self.rect.height / 2 - 1
                              return self.original_pos.x, y

          def draw(self):
                    if self.is_visible_on_screen():
                              self.game.ui_surface.blit(self.image, self.rect)

                              line_start = (self.rect.left + self.padding, self.rect.centery)
                              line_end = (self.rect.right - self.padding, self.rect.centery)
                              pygame.draw.line(self.game.ui_surface, self.line_color, line_start, line_end,
                                               self.line_thickness)

                              self.game.ui_surface.blit(self.circle_surface,
                                                        (self.circle_rect.x, self.circle_rect.y + 1))
                              self.game.ui_surface.blit(self.text, self.text_rect)

          def update_text(self):
                    self.text = self.font.render(self.text_input + str(int(self.value)), False, self.text_base_color)
                    self.text_rect = self.text.get_rect(center=self.rect.center)
                    if self.text_pos == "top":
                              self.text_rect.centery = self.rect.top - 0.3 * self.text_rect.height
                    elif self.text_pos == "bottom":
                              self.text_rect.centery = self.rect.bottom + 0.3 * self.text_rect.height
                    elif self.text_pos == "left":
                              self.text_rect.centerx = self.rect.left - 0.6 * self.text_rect.width
                    elif self.text_pos == "right":
                              self.text_rect.centerx = self.rect.right + 0.6 * self.text_rect.width

          def is_visible_on_screen(self):
                    screen_rect = self.game.display_screen.get_rect()
                    return self.rect.colliderect(screen_rect)

          def update(self):
                    self.update_value = False
                    target = self.original_pos if self.active else v2(self.starting_pos)
                    distance = (target - self.current_pos).length()
                    speed_factor = min(distance / SETTINGS_BUTTON_FRICTION, 1)

                    direction = (target - self.current_pos).normalize() if distance > 0 else v2(0, 0)
                    movement = direction * self.speed * speed_factor * self.game.dt
                    if movement.length() > distance:
                              self.current_pos = target
                    else:
                              self.current_pos += movement

                    self.update_text()

                    mouse_pos = self.game.correct_mouse_pos
                    if self.game.mouse_state[0]:
                              if self.circle_rect.collidepoint(mouse_pos):
                                        self.is_dragging = True
                              if self.is_dragging:
                                        self.set_value()
                    else:
                              self.is_dragging = False

                    self.rect.center = self.current_pos
                    normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
                    self.circle_rect.centerx = self.rect.left + self.padding + normalized_value * (
                            self.rect.width - 2 * self.padding)
                    self.circle_rect.centery = self.rect.centery

          def changeColor(self):
                    if self.is_dragging or self.circle_rect.collidepoint(self.game.correct_mouse_pos):
                              self.current_colour = self.circle_hovering_color
                    else:
                              self.current_colour = self.circle_base_colour
                    pygame.draw.circle(self.circle_surface, self.current_colour,
                                       (self.circle_radius, self.circle_radius), self.circle_radius)

          def set_value(self):
                    mouse_x = self.game.correct_mouse_pos[0]
                    if mouse_x <= self.rect.left + self.padding:
                              self.value = self.min_value
                    elif mouse_x >= self.rect.right - self.padding:
                              self.value = self.max_value
                    else:
                              normalized_x = (mouse_x - (self.rect.left + self.padding)) / (
                                      self.rect.width - 2 * self.padding)
                              self.value = self.min_value + normalized_x * (self.max_value - self.min_value)
                    self.update_value = True


class SwitchButton(SlidingButtons):
          def __init__(self, game, image, pos, axis, axisl, res=PLAY_BUTTON_RES, speed=SETTINGS_BUTTON_SPEED,
                       text_input=None, font=FONT, base_color=(255, 255, 255), hovering_color=(255, 0, 0), on=False):
                    super().__init__(game, image, pos, axis, axisl, res=res, speed=speed,
                                     text_input=text_input, font=font, base_colour=base_color,
                                     hovering_colour=hovering_color)
                    self.on = on
                    self.cooldown = BUTTON_COOLDOWN
                    self.last_pressed_time = 0

          def update(self):
                    super().update()

          def changeColor(self):
                    self.update_text()

          def can_change(self):
                    return self.rect.collidepoint(self.game.correct_mouse_pos) and pygame.time.get_ticks() / 1000 - self.last_pressed_time > self.cooldown

          def change_on(self):
                    self.on = not self.on
                    self.last_pressed_time = pygame.time.get_ticks() / 1000
                    self.update_text()

          def update_text(self):
                    if self.has_text:
                              color = self.hovering_color if self.on else self.base_color
                              self.text = self.font.render(self.text_input, False, color)
                              self.text_rect = self.text.get_rect(center=self.rect.center)

          def draw(self):
                    if self.is_visible_on_screen():
                              self.game.ui_surface.blit(self.image, self.rect)
                              if self.has_text:
                                        self.game.ui_surface.blit(self.text, self.text_rect)
