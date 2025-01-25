from Code.Variables.SettingsVariables import *

class SoundManager:
          def __init__(self, game):
                    self.game = game
                    self.music_volume = 1.0
                    self.sound_volume = 1.0
                    pygame.mixer.init()
                    self.last_played = {}  # Add this line

          def play_sound(self, name, pitch_variation=0.02):
                    original_sound = self.game.assets[name]
                    original_sound.play()

          @staticmethod
          def resample(sound_array, factor):
                    """Resample the sound array by a given factor."""
                    if factor == 1.0:
                              return sound_array
                    new_length = int(len(sound_array) / factor)
                    return np.array([
                              np.interp(
                                        np.linspace(0, len(channel) - 1, new_length),
                                        np.arange(len(channel)),
                                        channel
                              )
                              for channel in sound_array.T
                    ]).T

          def play_music(self, name, loops=-1):
                              pygame.mixer.music.load(self.game.assets[name])
                              pygame.mixer.music.set_volume(self.music_volume)
                              pygame.mixer.music.play(loops)
                              self.current_music = music_name
