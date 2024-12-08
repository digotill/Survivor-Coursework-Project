from Code.Utilities.Utils import *
from Code.Variables.Variables import *


class Button:
          def __init__(self, game, image, pos, axis, axisl, res=General_Settings['buttons_res'],
                       speed=General_Settings["buttons_speed"],
                       text_input=None, font=General_Settings['font'], base_colour=(255, 255, 255),
                       hovering_colour=(255, 0, 0),
                       text_pos="center", hover_slide=True, hover_offset=10, hover_speed=20):
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
                    self.has_text = text_input is not None
                    self.text_input = text_input
                    self.font_path = font
                    self.base_color = base_colour
                    self.hovering_color = hovering_colour
                    self.text_pos = text_pos
                    self.hover_offset = hover_offset
                    self.hover_speed = hover_speed
                    self.current_hover_offset = 0
                    self.hover_slide = hover_slide
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
                    self.font_size = int(self.rect.height / General_Settings['font_size'])
                    self.font = pygame.font.Font(self.font_path, self.font_size)
                    self.text = self.font.render(self.text_input, False, self.base_color)
                    self.text_rect = self.text.get_rect(center=self.rect.center)

          def update_text_position(self):
                    if self.text_pos == "top":
                              self.text_rect = self.text.get_rect(midbottom=(self.rect.centerx, self.rect.top - 5))
                    elif self.text_pos == "bottom":
                              self.text_rect = self.text.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 5))
                    elif self.text_pos == "left":
                              self.text_rect = self.text.get_rect(midright=(self.rect.left - 5, self.rect.centery))
                    elif self.text_pos == "right":
                              self.text_rect = self.text.get_rect(midleft=(self.rect.right + 5, self.rect.centery))
                    else:
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
                    speed_factor = min(distance / General_Settings["buttons_friction"], 1)

                    if self.rect.collidepoint(self.game.correct_mouse_pos) and self.hover_slide:
                              self.current_hover_offset = min(
                                        self.current_hover_offset + self.hover_speed * self.game.dt, self.hover_offset)
                              target.x = min(self.current_pos.x + self.current_hover_offset,
                                             self.starting_pos[0] + self.hover_offset)
                    else:
                              self.current_hover_offset = max(
                                        self.current_hover_offset - self.hover_speed * self.game.dt, 0)
                              target.x = max(self.current_pos.x - self.current_hover_offset,
                                             self.starting_pos[0])

                    direction = (target - self.current_pos).normalize() if distance > 0 else v2(0, 0)
                    movement = direction * self.speed * speed_factor * self.game.dt
                    if movement.length() > distance:
                              self.current_pos = target
                    else:
                              self.current_pos += movement

                    self.rect.center = self.current_pos

                    if self.has_text:
                              self.update_text_position()

          def check_for_input(self):
                    return self.rect.collidepoint(self.game.correct_mouse_pos)

          def changeColor(self):
                    if self.has_text:
                              color = self.hovering_color if self.rect.collidepoint(
                                        self.game.correct_mouse_pos) else self.base_color
                              self.text = self.font.render(self.text_input, False, color)


class Slider(Button):
          def __init__(self, game, image, pos, axis, axisl, res=General_Settings['buttons_res'], circle_radius=None,
                       speed=General_Settings["buttons_speed"], initial_value=0.5, min_value=0,
                       max_value=1, circle_base_colour=(255, 255, 255), circle_hovering_color=(255, 0, 0),
                       text_input=None, font=General_Settings['font'], text_base_color=(255, 255, 255),
                       text_pos="center", hover_slide=False):
                    super().__init__(game, image, pos, axis, axisl, res=res, speed=speed,
                                     text_input=text_input, font=font, base_colour=text_base_color,
                                     hovering_colour=text_base_color, text_pos=text_pos)

                    self.circle_radius = circle_radius if circle_radius is not None else 0.3 * self.rect.height
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
                    self.line_color = (100, 100, 100)
                    self.line_thickness = 2
                    self.update_value = False
                    self.is_dragging = False
                    self.update_text()
                    self.hover_slide = hover_slide

          def draw(self):
                    if self.is_visible_on_screen():
                              self.game.ui_surface.blit(self.image, self.rect)

                              line_start = (self.rect.left + self.padding, self.rect.centery)
                              line_end = (self.rect.right - self.padding, self.rect.centery)
                              pygame.draw.line(self.game.ui_surface, self.line_color, line_start, line_end,
                                               self.line_thickness)

                              self.game.ui_surface.blit(self.circle_surface,
                                                        (self.circle_rect.x, self.circle_rect.y + 1))
                              self.game.ui_surface.blit(self.text,
                                                        self.text_rect)

          def update_text(self):
                    self.text = self.font.render(self.text_input + str(int(self.value)), False, self.base_color)
                    self.update_text_position()

          def update(self):
                    super().update()
                    self.update_value = False

                    if self.game.mouse_state[0]:
                              if self.circle_rect.collidepoint(self.game.correct_mouse_pos):
                                        self.is_dragging = True
                              if self.is_dragging:
                                        self.set_value()
                    else:
                              self.is_dragging = False

                    normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
                    self.circle_rect.centerx = self.rect.left + self.padding + normalized_value * (
                            self.rect.width - 2 * self.padding)
                    self.circle_rect.centery = self.rect.centery

                    self.update_text()

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


class Switch(Button):
          def __init__(self, game, image, pos, axis, axisl, res=General_Settings['buttons_res'],
                       speed=General_Settings["buttons_speed"],
                       text_input=None, font=General_Settings['font'], base_color=(255, 255, 255),
                       hovering_color=(255, 0, 0), on=False, text_pos="left"):
                    super().__init__(game, image, pos, axis, axisl, res=res, speed=speed,
                                     text_input=text_input, font=font, base_colour=base_color,
                                     hovering_colour=hovering_color, text_pos=text_pos)
                    self.on = on
                    self.cooldown = Cooldowns['buttons']
                    self.last_pressed_time = 0

          def changeColor(self):
                    if self.has_text:
                              color = self.hovering_color if self.on else self.base_color
                              self.text = self.font.render(self.text_input, False, color)

          def can_change(self):
                    return self.rect.collidepoint(
                              self.game.correct_mouse_pos) and pygame.time.get_ticks() / 1000 - self.last_pressed_time > self.cooldown

          def change_on(self):
                    self.on = not self.on
                    self.last_pressed_time = pygame.time.get_ticks() / 1000

          def draw(self):
                    if self.is_visible_on_screen():
                              self.game.ui_surface.blit(self.image, self.rect)
                              if self.has_text:
                                        self.game.ui_surface.blit(self.text, self.text_rect)
