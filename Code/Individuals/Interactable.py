from Code.Variables.SettingVariables import *


# Base class for UI elements
class Interactable:
          def set_rect(self):
                    self.rect = pygame.Rect(self.pos.x - self.res[0] / 2, self.pos.y - self.res[1] / 2, self.res[0],
                                            self.res[1])

          def setup_text(self):
                    # Set up the text for the UI element
                    self.font = self.game.assets["font8"]
                    self.text = self.font.render(self.text_input, False, self.base_colour)
                    self.text_rect = self.text.get_rect(center=self.rect.center)
                    self.has_text = True

          def calculate_starting_position(self):
                    # Calculate the starting position of the UI element based on its axis and alignment
                    if self.axis == "x":
                              x = self.game.render_resolution[0] + self.rect.width / 2 + 1 if self.axisl == "max" else -self.rect.width / 2 - 1
                              return x, self.pos.y
                    else:
                              y = self.game.render_resolution[1] + self.rect.height / 2 + 1 if self.axisl == "max" else -self.rect.height / 2 - 1
                              return self.pos.x, y

          def update_text_position(self):
                    # Update the position of the text based on the specified text_pos
                    # (top, bottom, left, right, or center)
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

          def is_visible_on_screen(self):
                    # Check if the UI element is visible on the screen
                    screen_rect = self.game.displayS.get_rect()
                    return self.rect.colliderect(screen_rect)

          def update_text_render(self):
                    # Update the rendered text
                    if self.has_text:
                              self.text = self.font.render(self.text_input, False, self.base_colour)
                              self.update_text_position()

          def check_for_input(self):
                    # Check if the mouse is over the UI element
                    return self.rect.collidepoint(self.game.correct_mouse_pos)


          def draw(self):
                    # Draw the UI element and its text if visible
                    if self.is_visible_on_screen():
                              self.game.uiS.blit(self.image, self.rect)
                              if self.has_text:
                                        self.game.uiS.blit(self.text, self.text_rect)

          def update(self):
                    # Update the position and state of the UI element
                    # Handle hover effects and smooth transitions
                    target = self.pos if self.active else v2(self.starting_pos)

                    distance = (target - self.current_pos).length()
                    speed_factor = min(distance / (self.speed * self.distance_factor), 1)

                    if self.rect.collidepoint(self.game.correct_mouse_pos) and self.hover_slide:
                              self.current_hover_offset = min(
                                        self.current_hover_offset + self.hover_speed * self.game.dt, self.hover_offset)
                    else:
                              self.current_hover_offset = max(
                                        self.current_hover_offset - self.hover_speed * self.game.dt, 0)

                    # Update the target vector
                    target.x = self.starting_pos[0] + self.current_hover_offset if self.hover_slide else self.starting_pos[0]

                    direction = (target - self.current_pos).normalize() if (target - self.current_pos).length_squared() > 0 else v2(0, 0)
                    movement = direction * self.speed * speed_factor * self.game.dt
                    if movement.length() > distance:
                              self.current_pos = target
                    else:
                              self.current_pos += movement

                    temp_pos = round(self.current_pos.x), round(self.current_pos.y)
                    self.rect.center = temp_pos

                    if self.has_text:
                              self.update_text_position()

                    self.update_text_render()

          def init_positions(self):
                    # Initialize the positions and text for the UI element
                    self.set_rect()
                    self.starting_pos = self.calculate_starting_position()
                    self.current_pos = v2(self.starting_pos)
                    self.rect.center = self.current_pos
                    self.setup_text()


# Button class, inherits from UIElement
class Button(Interactable):
          def __init__(self, game, dictionary):
                    # Initialize the button with game instance and attributes from dictionary
                    self.game = game

                    self.game.methods.set_attributes(self, dictionary)

                    self.init_positions()

          def change_colour(self):
                    # Change the color of the button text based on hover state
                    if self.has_text:
                              colour = self.hovering_colour if self.rect.collidepoint(self.game.correct_mouse_pos) else self.base_colour
                              self.text = self.font.render(self.text_input, False, colour)


# Slider class, inherits from UIElement
class Slider(Interactable):
          def __init__(self, game, dictionary):
                    # Initialize the slider with game instance and attributes from dictionary
                    # Set up the slider's visual components (line and circle)
                    self.game = game

                    self.game.methods.set_attributes(self, dictionary)

                    self.init_positions()

                    self.is_dragging = False
                    self.circle_radius = 0.3 * self.rect.height
                    self.padding = self.circle_radius * 2
                    self.circle_surface = pygame.Surface((self.circle_radius * 2, self.circle_radius * 2))
                    self.circle_surface.set_colorkey((0, 0, 0))
                    self.current_colour = self.circle_base_colour
                    pygame.draw.circle(self.circle_surface, self.current_colour,
                                       (self.circle_radius, self.circle_radius), self.circle_radius)
                    self.circle_rect = pygame.Rect(self.rect.x + self.value * self.rect.width - self.circle_radius,
                                                   self.rect.y - self.circle_radius + 0.5 * self.rect.height,
                                                   self.circle_radius * 2, self.circle_radius * 2)

          def draw(self):
                    # Draw the slider, including the line and circle
                    if self.is_visible_on_screen():
                              self.game.uiS.blit(self.image, self.rect)

                              line_start = (self.rect.left + self.padding, self.rect.centery)
                              line_end = (self.rect.right - self.padding, self.rect.centery)
                              pygame.draw.line(self.game.uiS, self.line_colour, line_start, line_end,
                                               self.line_thickness)

                              self.game.uiS.blit(self.circle_surface,
                                                 (self.circle_rect.x, self.circle_rect.y + 1))
                              if self.text_input is not None:
                                        self.game.uiS.blit(self.text, self.text_rect)

          def update(self):
                    # Update the slider's position, value, and handle user interaction
                    target = self.pos if self.active else v2(self.starting_pos)

                    distance = (target - self.current_pos).length()
                    speed_factor = min(distance / (self.speed * self.distance_factor), 1)

                    direction = (target - self.current_pos).normalize() if distance > 0 else v2(0, 0)
                    movement = direction * self.speed * speed_factor * self.game.dt
                    if movement.length() > distance:
                              self.current_pos = target
                    else:
                              self.current_pos += movement

                    self.rect.center = self.current_pos

                    self.update_value = False

                    if self.game.mouse_state[0]:
                              if self.circle_rect.collidepoint(self.game.correct_mouse_pos) and not self.game.interactablesM.grabbing_slider:
                                        self.is_dragging = True
                                        self.game.interactablesM.grabbing_slider = True
                              if self.is_dragging:
                                        self.set_value()
                    else:
                              self.is_dragging = False
                              self.game.interactablesM.grabbing_slider = False

                    normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
                    self.circle_rect.centerx = self.rect.left + self.padding + normalized_value * (
                            self.rect.width - 2 * self.padding)
                    self.circle_rect.centery = self.rect.centery

                    if self.text_input is not None:
                              self.update_text()

          def update_text(self):
                    # Update the text displayed on the slider
                    self.text = self.font.render(self.text_input + str(int(self.value)), False, self.base_colour)
                    self.update_text_position()

          def change_colour(self):
                    # Change the color of the slider's circle based on interaction state
                    if self.is_dragging:
                              self.current_colour = self.circle_hovering_colour
                    else:
                              self.current_colour = self.circle_base_colour
                    pygame.draw.circle(self.circle_surface, self.current_colour,
                                       (self.circle_radius, self.circle_radius), self.circle_radius)

          def set_value(self):
                    # Set the slider's value based on the mouse position
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


# Switch class, inherits from UIElement
class Switch(Interactable):
          def __init__(self, game, dictionary):
                    # Initialize the switch with game instance and attributes from dictionary
                    self.game = game

                    self.game.methods.set_attributes(self, dictionary)

                    self.init_positions()

                    self.cooldown_timer = Timer(GENERAL['cooldowns'][0], self.game.ticks)

          def change_colour(self):
                    # Change the color of the switch text based on its state (on/off)
                    if self.has_text:
                              colour = self.hovering_colour if self.on else self.base_colour
                              self.text = self.font.render(self.text_input, False, colour)

          def can_change(self):
                    # Check if the switch can change its state (based on cooldown and current state)
                    return (self.rect.collidepoint(self.game.correct_mouse_pos) and
                            self.cooldown_timer.check(self.game.ticks) and
                            not self.on)

          def change_on(self):
                    # Toggle the switch's state and reset the cooldown timer
                    self.on = not self.on
                    self.cooldown_timer.reactivate(self.game.ticks)
