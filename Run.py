import logging
from pstats import Stats
import ctypes
from Code.Utilities.ErrorLogger import *
from Code.Utilities.Functions import *
import traceback

ctypes.windll.shcore.SetProcessDpiAwareness(2)

rename_files_recursive(r"C:\Users\digot\PycharmProjects\Survivor-Coursework-Project\Assets")

from Code.Game_Class import *
from Code.Variables.Variables import Performance_Profile
import cProfile, os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if sys.version_info < (3, 7):
          logger.error("This script requires Python 3.7 or higher.")
          sys.exit(1)

os.environ['SDL_VIDEODRIVER'] = 'opengl'

if __name__ == "__main__":
          profiler = None
          if Performance_Profile:
                    profiler = cProfile.Profile()
                    profiler.enable()

          try:
                    Game()
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

sys.exit(1)
