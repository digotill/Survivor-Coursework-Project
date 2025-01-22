import pygame


class Timer:
          def __init__(self, duration, start_time, func=None):
                    self.duration = duration
                    self.func = func
                    self.active = True
                    self.start_time = start_time
                    self.current_time = self.start_time

          def reactivate(self, start_time):
                    self.active = True
                    self.start_time = start_time
                    self.current_time = self.start_time

          def update(self, current_time):
                    if self.active:
                              self.current_time = current_time
                              if self.current_time - self.start_time >= self.duration:
                                        if self.func:
                                                  self.func()
                                        self.active = False
                                        return True
                    return False

          def check(self, current_time):
                    return current_time - self.start_time >= self.duration

          @property
          def elapsed(self):
                    if not self.active:
                              return 0
                    return self.current_time - self.start_time

          @property
          def remaining(self):
                    if not self.active:
                              return self.duration
                    return max(0, self.duration - self.elapsed)

          @property
          def is_finished(self):
                    return not self.active
