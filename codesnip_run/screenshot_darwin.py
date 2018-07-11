import sys

from AppKit import NSWorkspace
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID
)

def active_window_info(event_window_num):
    app = NSWorkspace.sharedWorkspace().frontmostApplication()
    active_app_name = app.localizedName()

    options = kCGWindowListOptionOnScreenOnly
    windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    windowTitle = 'Unknown'
    for window in windowList:
        windowNumber = window['kCGWindowNumber']
        ownerName = window['kCGWindowOwnerName']
        geometry = window['kCGWindowBounds']
        windowTitle = window.get('kCGWindowName', u'Unknown')
        if windowTitle and (event_window_num == windowNumber or
                            ownerName == active_app_name):
            # log.debug(
            #     'ownerName=%s, windowName=%s, x=%s, y=%s, '
            #     'width=%s, height=%s'
            #     % (window['kCGWindowOwnerName'],
            #        window.get('kCGWindowName', u'Unknown'),
            #        geometry['X'],
            #        geometry['Y'],
            #        geometry['Width'],
            #        geometry['Height']))
            break

    return _review_active_info(active_app_name, windowTitle)
