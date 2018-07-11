import sys

#https://stackoverflow.com/questions/28815863/how-to-get-active-window-title-using-python-in-mac
if sys.platform == "darwin":
    from .screenshot_darwin import active_window_info
elif sys.platform == "win":
    from .screenshot_win import active_window_info

