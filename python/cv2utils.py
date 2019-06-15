# -*- coding: utf-8 -*-
"""
Utility functions for interfacing with cv2 library.

Change log:
  2015/08/16 -- module started; nloomis@gmail.com
  2015/10/10 -- copied generic tools out to imageutils.py, so that only the
                code specific to cv2 is in this module; nloomis@
  2019/06/13 -- added imwrite for convenience; added imshow; nloomis@
  2019/06/14 -- added resize using a scaling factor; nloomis@
"""
__authors__ = {'nloomis@gmail.com'}

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

    NB: OpenCV reads images into memory as BGR, the opposite of numpy and
    matlab. Use flip_channels or flip_channels_cv2 to convert the channels to
    RGB order instead.
    """
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
            print('Re-trying a read using cv2.IMREAD_UNCHANGED...')
            img = imread(filename, cv2.IMREAD_UNCHANGED)
    return img

def imwrite(img_data, filename):
    """Writes an image to disk using cv2.

    Convenience function, included in the module so that both imread + imwrite
    are in contained in the same import. Uses the same argument order as Matlab.
    """
    cv2.imwrite(filename, img_data)

def flip_channels_cv2(img):
    """Changes from BGR<->RGB, flipping the order of color channels.

    Uses the built-in method in OpenCV, cvtColor, and can be implemented easily
    in an OpenCV-only code. The flip_channels() function is preferred: it is
    faster and is independent on the number of channels.
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def imshow(img):
    # TODO[NL]: make this into a class, get a GUID for the figure name or
    # reflect the argument.
    cv2.imshow('image', img)
    keypress = cv2.waitKey(0) & 0xFF
    if keypress == ESC or keypress == ord('q'):
        cv2.destroyAllWindows()
    # Ideally: add a listener for the window's close button.

def resize(img, scale):
    """Resizes an image using a fixed scaling factor."""
    initial_height, initial_width = img.shape[:2]
    final_height = int(initial_height * scale)
    final_width = int(initial_width * scale)
    if scale > 1:
        method = cv2.INTER_CUBIC
    else:
        method = cv2.INTER_AREA
    return cv2.resize(img, (final_width, final_height), method)
