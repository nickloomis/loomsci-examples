# -*- coding: utf-8 -*-
"""
Functions to help with color space conversions using CV2 library calls.

Change log:
  2015/08/15 -- module started; color_mode, color_conversion_names, rgb2gray,
                bgr2rgb, bgr2hsv, rgb2bgr; nloomis@gmail.com
  2015/10/31 -- bgr2gray added; nloomis@
"""
__authors__ = {'nloomis@gmail.com'}

import cv2


def color_mode(conversion_name):
    """Return the CV conversion type const for the named color conversion."""
    flag_name = 'COLOR_' + conversion_name.upper()
    if cv2.__dict__.has_key(flag_name):
        return cv2.__dict__[flag_name]
    else:
        print 'Known color conversions: %s' % color_conversion_names()
        raise KeyError('The conversion %s is not a known type.' % flag_name)

def color_conversion_names():
    """List of all known ccolor conversion mode names."""
    return [i for i in dir(cv2) if i.startswith('COLOR_')]

def rgb2gray(img):
    """Wrapper for RGB to Gray conversion of CV2 images."""
    return cv2.cvtColor(img, color_mode('rgb2gray'))
    #Y =  0.299R + 0.587G + 0.114B

def bgr2gray(img):
    """Wrapper for BGR to Gray conversion of CV2 images."""
    return cv2.cvtColor(img, color_mode('bgr2gray'))

def rgb2bgr(img):
    """Wrapper for RGB to BGR conversion of cv2 images."""
    return cv2.cvtColor(img, color_mode('rgb2bgr'))

def bgr2rgb(img):
    """Wrapper for BGR to RGB conversion of cv2 images."""
    return cv2.cvtColor(img, color_mode('bgr2rgb'))
    
def bgr2hsv(img):
    """Wrapper for BGR to HSV conversion of cv2 images."""
    return cv2.cvtColor(img, color_mode('bgr2hsv'))