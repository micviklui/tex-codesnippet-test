from codesnip_run import screenshot

def test_screenshot():
    win = screenshot.active_window_info()
    screenshot.grab(win['geometry']['Y'], win['geometry']['X'],
                    win['geometry']['Width'], win['geometry']['Height'],
                    1,
                    'test_screenshot.png')
