import logging
import sys

from AppKit import NSWorkspace
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID
)

LOGGER = logging.getLogger(__name__)


def active_window_info():
    app = NSWorkspace.sharedWorkspace().frontmostApplication()
    active_app_pid = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier']
    #active_app_pid = app['NSApplicationProcessIdentifier']
    active_app_name = app.localizedName()

    options = kCGWindowListOptionOnScreenOnly
    windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    windowTitle = 'Unknown'
    for window in windowList:
        pid = window['kCGWindowOwnerPID']
        #windowNumber = window['kCGWindowNumber']
        ownerName = window['kCGWindowOwnerName']
        geometry = window['kCGWindowBounds']
        windowTitle = window.get('kCGWindowName', u'Unknown')
        if windowTitle and (pid == active_app_pid or
                            ownerName == active_app_name):
            LOGGER.debug(
                'ownerName=%s, windowName=%s, x=%s, y=%s, '
                'width=%s, height=%s',
                window['kCGWindowOwnerName'],
                window.get('kCGWindowName', u'Unknown'),
                geometry['X'],
                geometry['Y'],
                geometry['Width'],
                geometry['Height'])
            break

    #return _review_active_info(active_app_name, windowTitle)
