# -*- coding: utf-8 -*-
"""
Utility functions for interfacing with cv2 library.

Change log:
  2010/08/16 -- module started; nloomis@gmail.com
  2010/10/10 -- copied generic tools out to imageutils.py, so that only the
                code specific to cv2 is in this module; nloomis@
"""
#stdlib imports
import os.path

#local imports
import cv2

# list of key bindings which are useful for GUIs
ESC = 27
#arrows; other special keys;... see also ord('a') for converting letters->int

# image read/write
def imread(filename, read_mode=cv2.IMREAD_COLOR):
    """Read an image from disk using cv2.

    Checks that the file exists on disk, and attempts more permissible
    read-in settings if the original method doesn't work.
    read_mode defaults to cv2.IMREAD_COLOR; can also take cv2.IMREAD_GRAYSCALE
    or cv2.IMREAD_UNCHANGED.
    """
    #thought: should we auto-convert BGR->RGB for color images?
    read_modes = [cv2.IMREAD_COLOR, cv2.IMREAD_GRAYSCALE, cv2.IMREAD_UNCHANGED]
    assert (read_mode in read_modes)
    if not os.path.exists(filename):
        raise IOError('The file %s was not found.' % filename)
    img = cv2.imread(filename, read_mode)
    if img is None:
        if read_mode == cv2.IMREAD_UNCHANGED:
            raise IOError('Image %s could not be read in.' % filename)
        else:
            #try reading again, but with the most permissible settings
            print 'Re-trying a read using cv2.IMREAD_UNCHANGED...'
            img = imread(filename, cv2.IMREAD_UNCHANGED)
    return img


def flip_channels_cv2(img):
    """Changes from BGR<->RGB, flipping the order of color channels.

    Uses the built-in method in OpenCV, cvtColor, and can be implemented easily
    in an OpenCV-only code. The flip_channels() function is preferred: it is
    faster and is independent on the number of channels.
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
