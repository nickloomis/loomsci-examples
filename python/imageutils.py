# -*- coding: utf-8 -*-
"""
Generic utilities for working with images.

Note that images are read in by cv2utils to be numpy arrays.

Change log:
  2015/10/07 -- repo_dir, image_dir, dir_by_ext, test_image written;
                nloomis@gmail.com
  2015/10/10 -- added channel management methods; nloomis@
"""

import matplotlib.pyplot as plt
import numpy
import os

import cv2utils


#
# file handling
#

#constants
#extensions for images recognized by cv2
IMAGE_EXT = ('jpg', 'jpeg', 'jp2', 'tif', 'tiff', 'png', 'bmp',
              'ppm', 'pbm', 'pgm', 'sr', 'ras')

def repo_dir():
    """Path to the base of the repository."""
    #nb: this function assumes that the file is in <repo>/python
    file_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.split(file_path)[0]

def image_dir():
    """Path to the directory of repo test images."""
    return os.path.join(repo_dir(), 'images')

def dir_by_ext(srcdir, ext):
    """Finds files in a source directory that end with the given extensions.

    The ext variable can either be a string with a single extension, or a tuple
    of extension strings to try matching; any match will succeed. The extension
    should NOT contain a period ('.'), only the extension letters, and the
    extensions should be in lower case.
    Examples:
    dir_by_ext('some/path', ('jpg', 'jpeg'))
    dir_by_ext('some/path', 'txt')
    """
    #convert the ext to a tuple if it isn't already
    if not isinstance(ext, tuple):
        ext = tuple(ext)
    files = os.listdir(srcdir)
    matches = [file_name for file_name in files
               if len(file_name.split('.')) > 1 and \
                 file_name.split('.')[1].lower().endswith(IMAGE_EXT)]
    #the logical test pulls out the extension, converts it to lowercase, and
    #checks to see if it matches any of the supplied extensions. note that if
    #there is no extension, the test will fail before it bothers checking for
    #the match.
    return matches

def test_image(image_name=None):
    """Loads a test image with the closest match to the supplied name."""
    test_image_dir = image_dir()
    available_images = dir_by_ext(image_dir(), IMAGE_EXT)
    if image_name is None:
        print 'Available images are: %s' % available_images
        return None
    #find the matching image names
    assert(isinstance(image_name, basestring))
    matches = [file_name for file_name in available_images
               if file_name.startswith(image_name)]
    if len(matches) == 0:
        print 'No name match found for %s.' % image_name
        return None
    elif len(matches) > 1:
        print 'Multiple matches found for %s: %s.' % (image_name, matches)
        return None
    else:
        #load the matching image
        filename = os.path.join(test_image_dir, matches[0])
        print 'loading: %s' % filename
        return cv2utils.imread(filename)

#
# image channels
#

def flip_channels(img):
    """Flips the order of channels in an image; eg, BGR <-> RGB.
    
    This function assumes the image is a numpy.array (what's returned by cv2
    function calls) and uses the numpy re-ordering methods. The number of
    channels does not matter.
    """
    return img[:,:,::-1]    

def cat3(*channels):
    """Concatenate channels in the supplied order.
    
    Convenience function."""
    #numpy.dstack() is 40% faster than cv2.merge()
    return numpy.dstack(channels)

def split2(img):
    """Splits a 2-channel image into its constituent channels.
    
    Convenience function using numpy slices, ~300x faster than cv2.split()."""
    assert(isinstance(img, numpy.ndarray))
    assert(nchannels(img) == 2)
    return img[:, :, 0], img[:, :, 1]
    #TODO: split into column vectors if a 2D array
    
def split3(img):
    """Splits a 3-channel image into its constituent channels.
    
    Convenience function using numpy slices, ~300x faster than cv2.split()."""
    assert(isinstance(img, numpy.ndarray))
    assert(nchannels(img) == 3)
    return img[:, :, 0], img[:, :, 1], img[:, :, 2]
    #TODO: split into column vectors if a 2D array

def nchannels(img):
    """Returns the number of channels in an image."""
    assert(isinstance(img, numpy.ndarray))
    if img.ndim < 3:
        return 1
    else:
        return img.shape[2]

#
# data types
#

def datatype(img):
    """The type of the data used in the image: img.dtype."""
    assert(isinstance(img, numpy.ndarray))
    return img.dtype
    
def float2uint8(img):
    """Converts a float array to a uint8 type.
    
    The float values are expected to be in the range [0..1]. uint8 values are
    returned in the range [0..255]."""
    assert(isinstance(img, numpy.ndarray))
    #TODO: img.view() may be faster, but isn't giving the right conversions?
    return numpy.rint(img * 255).astype('uint8')
    
#
# display
#

def imshow(img, figure_name='image'):
    """Wrapper for matplotlib.pyplot.imshow()."""
    #using matplotlib for now: (which expects RGB channel ordering)
    plt.imshow(flip_channels(img))
    #note that flip_channels() is MUCH faster than
    #cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#rem: when using cv2.imshow(), the waitkey needs to get masked! use
#waitKey(0) & 0xFF in 64-bit

#def mydisp(img, clim)
#see plt.imshow() for helpful args; vmin and vmax for min/max values, norm for
#normalizing the values; check for int vs float, though!
