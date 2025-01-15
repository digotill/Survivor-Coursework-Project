import sys
import logging
from pstats import Stats
import ctypes
from Code.Utilities.ErrorLogger import *
import traceback

ctypes.windll.shcore.SetProcessDpiAwareness(2)

from Code.Classes.Game_Class import *
from Code.Variables.Variables import PF
import cProfile, os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if sys.version_info < (3, 7):
          logger.error("This script requires Python 3.7 or higher.")
          sys.exit(1)

os.environ['SDL_VIDEODRIVER'] = 'opengl'

if __name__ == "__main__":
          profiler = None
          if PF:
                    profiler = cProfile.Profile()
                    profiler.enable()

          try:
                    Game().run_game()
          except Exception as e:
                    error_message = str(e)
                    error_traceback = traceback.format_exc()
                    log_error(error_message, error_traceback)
                    print_error_message(error_message, error_traceback)
          finally:
                    if profiler:
                              profiler.disable()
                              stats = Stats(profiler)
                              stats.sort_stats('time').reverse_order().print_stats()
