import sys
import logging
from pstats import Stats
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(2)

from Code.Classes.Game_Class import *
from Code.Variables.Variables import PROFILE
import cProfile, os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if sys.version_info < (3, 7):
          logger.error("This script requires Python 3.7 or higher.")
          sys.exit(1)

os.environ['SDL_VIDEODRIVER'] = 'opengl'

os.chdir('C:/Users/digot/PycharmProjects/Survivor')


if __name__ == "__main__":
          profiler = None
          if PROFILE:
                    profiler = cProfile.Profile()
                    profiler.enable()

          try:
                    Game().run_game()
                    sys.exit()
          except Exception as e:
                    logger.exception(f"An error occurred during game execution: {e}")
          finally:
                    if profiler:
                              profiler.disable()
                              stats = Stats(profiler)
                              stats.sort_stats('time').reverse_order().print_stats()
