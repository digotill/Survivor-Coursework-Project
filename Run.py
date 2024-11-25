from Code.Classes.Game_Class import *
import cProfile

import os
os.environ['SDL_VIDEODRIVER'] = 'opengl'

if PROFILE:
          profiler = cProfile.Profile()
          profiler.enable()


if __name__ == "__main__":
          run = Game().run_game()


if PROFILE:
          profiler.disable()
          profiler.print_stats(sort='cumulative')