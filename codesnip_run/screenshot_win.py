
def win_active_window_info(event_window_num):
    (active_app_name, windowTitle) = _getActiveInfo_Win32()
    return _review_active_info(active_app_name, windowTitle)

