import sys
import logging
# alternative: pyscreenshot, Xlib
import mss
import mss.tools

if sys.platform == "darwin":
    from .screenshot_darwin import active_window_info
elif sys.platform == "win":
    from .screenshot_win import active_window_info
#elif sys.platform == 'linux':
#    from .screenshot_linux import active_window_info
else:
    raise RuntimeError('screenshot not supported')


LOGGER = logging.getLogger(__name__)


def grab(top, left, width, height, monitor_number, output):
    with mss.mss() as sct:
        screen_part = {
            'top': top,
            'left': left,
            'width': width,
            'height': height,
            'mon': monitor_number,
        }
        sct_img = sct.grab(screen_part)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        LOGGER.debug(output)
