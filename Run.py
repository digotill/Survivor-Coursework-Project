from Code.Utilities.ErrorLogger import *
from Code.Game import *
import platform

OS = platform.system()

if OS == "Windows":
          try:
                    ctypes.windll.shcore.SetProcessDpiAwareness(2)
          except Exception as e:
                    print(f"Failed to set DPI awareness on Windows: {e}")
elif OS == "Darwin":  # macOS
          try:
                    import AppKit
                    AppKit.NSApplication.sharedApplication().setActivationPolicy_(1)
          except ImportError:
                    print("AppKit not available. Unable to set activation policy on macOS.")
elif OS == "Linux":
          print("No DPI awareness set for Linux. Please ensure you have the necessary libraries installed.")
else:
          print(f"Unknown operating system: {OS}")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if sys.version_info < (3, 7):
          logger.error("This script requires Python 3.7 or higher.")
          sys.exit(1)

os.environ['SDL_VIDEODRIVER'] = 'opengl'

Performance_Profile = False

if __name__ == "__main__":
          if Performance_Profile:
                    profiler = cProfile.Profile()
                    profiler.enable()

          try:
                    game = Game()
                    game.run_game()

          except Exception as e:
                    error_message = str(e)
                    error_traceback = traceback.format_exc()
                    log_error(error_message, error_traceback)
                    print_error_message(error_message, error_traceback)
          finally:
                    if Performance_Profile:
                              profiler.disable()
                              stats = Stats(profiler)
                              stats.sort_stats('time').reverse_order().print_stats()

sys.exit(1)
