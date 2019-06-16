# -*- coding: utf-8 -*-
"""
Generic utilities for working with images.

Note that images are read in by cv2utils to be numpy arrays.

Change log:
  2015/10/07 -- repo_dir, image_dir, dir_by_ext, test_image written;
                nloomis@gmail.com
  2015/10/10 -- added channel management methods; nloomis@
  2016/01/24 -- added __authors__ variable; fixed order of imports; nloomis@
  2017/02/05 -- added image resize/scaling functions; nloomis@
"""
__authors__ = ('nloomis@gmail.com',)

import cv2
import cv2utils

import matplotlib.pyplot as plt
import numpy
import os
import scipy.ndimage
#try:
#    from skimage import filters
#except ImportError:
#    # handles the case where skimage is v0.10 (the filter module was renamed
#    # to filters in v0.11)
#    from skimage import filter as filters

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
        print('Available images are: %s' % available_images)
        return None
    #find the matching image names
    assert(isinstance(image_name, str))
    matches = [file_name for file_name in available_images
               if file_name.startswith(image_name)]
    if len(matches) == 0:
        print('No name match found for %s.' % image_name)
        return None
    elif len(matches) > 1:
        print('Multiple matches found for %s: %s.' % (image_name, matches))
        return None
    else:
        #load the matching image
        filename = os.path.join(test_image_dir, matches[0])
        print('loading: %s' % filename)
        return cv2utils.imread(filename)

#
# image channels
#

def flip_channels(img):
    """Flips the order of channels in an image; eg, BGR <-> RGB.

    This function assumes the image is a numpy.array (what's returned by cv2
    function calls) and uses the numpy re-ordering methods. The number of
    channels does not matter.
    If the image array is strictly 2D, no re-ordering is possible and the
    original data is returned untouched.
    """
    if len(img.shape) == 2:
        return img;
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

#
# resize
#

def scale_to_width(image, width_pixels):
    """Rescales an image so that its width has the specified pixel count."""
    image_size = image.shape
    scale_factor = float(width_pixels) / image_size[1]
    target_height = round(scale_factor * image_size[0])
    target_size = (int(target_height), int(width_pixels))
    interp_method = scaling_interpolation_method(image_size, target_size)
    return cv2.resize(image, target_size, interpolation=interp_method)

def scale_to_height(image, height_pixels):
    """Rescales an image so that its height has the specified pixel count."""
    image_size = image.shape
    scale_factor = float(height_pixels) / image_size[0]
    target_width = round(scale_factor * image_size[1])
    target_size = (int(target_width), int(height_pixels))
    interp_method = scaling_interpolation_method(image_size, target_size)
    return cv2.resize(image, target_size, interpolation=interp_method)

def scale_to_min_size(image, min_pixels):
    """Rescale image so that its minimum dimension is a given pixel count."""
    image_size = image.shape
    if image_size[0] < image_size[1]:
        # The height is the smaller of the two dimensions.
        return scale_to_height(image, min_pixels)
    return scale_to_width(image, min_pixels)

def scaling_interpolation_method(original_size, destination_size):
    """Returns a preferred high-quality interpolation method for resizing.

    The preferred method depends on whether the image is decreasing in size or
    expanding in size.
    """
    height_scale = float(destination_size[0]) / original_size[0]
    width_scale = float(destination_size[1]) / original_size[1]
    mean_scale = 0.5 * (height_scale + width_scale)
    if mean_scale <= 1:
        return cv2.INTER_AREA
    return cv2.INTER_CUBIC

#
# filters
#

def imfilter():
    """Filters an image using a kernel."""
    pass
    # TODO(nloomis): make sure that the number of channels in the image and
    # the kernel match! May need to repmat the filter. If the filter has too
    # many channels or can't be repmat'd without uncertainty about what is
    # happening, throw an error.

def steerable_deriv(n_pix=None, sigma=1.5):
    """Builds a steerable Gaussian derivative filter in the x direction.
    
    Transpose the output array to get the filter in the y direction.
    Based on 'Design and use of steerable filters', Freeman and Adelson, PAMI, 
    1991.
    Inputs:
      n_pix: number of pixels in each side of the output filter. if n_pix is
             not specified, it defaults to 3*sigma. n_pix can be even or odd.
      sigma: amount of smoothing used for the filter; for a wider filter and
             more smoothing, use a large sigma. the sigma value is approximately
             the half-width of the filter in pixels. experiment with different
             values between 1 and 10 for most image processing applications.
             if sigma is not specified, it defaults to 1.5.
    Returns:
      a numpy array of size (n_pix x n_pix) with the weights of the x-direction
      steerable derivative filter.

    """
    if not n_pix:
        n_pix = int(numpy.ceil(3 * sigma))
    x = numpy.linspace(-n_pix / 2., n_pix / 2., int(n_pix))
    X, Y = numpy.meshgrid(x, x)
    norm_factor = sigma**2 * n_pix**2
    S = -2. * X * numpy.exp(-(X**2 + Y**2) / sigma**2) / norm_factor
    return S

def apply_gradient_filter(img, x_dir_filter):
    """Applies the gradient filter in two orthogonal directions.

    Inputs:
      img: image that filters should be applied onto
      x_dir_filter: a filter which, which convolved with the image, returns the
        gradients in the x direction. the filter is transposed for use in the
        y direction. it should be a numpy array, and can have up to the same
        number of channels as the image.
    Returns:
      tuple of (S, O, gx, gy), with
       S: magnitude of the gradient
       O: orientation of the gradient in radians
       gx: x-direction raw gradient data
       gy: y-direction raw gradient data
    """
    gradient_x = scipy.ndimage.filters.convolve(img, x_dir_filter)
    gradient_y = scipy.ndimage.filters.convolve(img, x_dir_filter.transpose())
    S = numpy.sqrt(gradient_x**2 + gradient_y**2)
    O = numpy.atan2(gradient_y, gradient_x)
    return S, O, gradient_x, gradient_y

def local_mean_filter(img, structuring_element):
    """Returns the local average of an image.

    The structuring element is a mask which determines the shape of the local
    area. The structuring element is a 2D numpy array with 0's outside the
    local are and 1's inside the mask. (Alternately, any other weighting value
    can be used within the mask region.)
    Hint: skimage.morphology has a number of pre-defined structuring elements.
    """
    se_shape = structuring_element.shape
    # TODO(nloomis): need to reshape or replicate so that the image and the filter
    # have the same number of channels!
    #...duh, use .ndim for dimensions...
    if structuring_element.ndim != img.ndim:
        pass #TODO: be smart about matching the dims!
#        structuring_element.reshape((se_shape[0], se_shape[1], 1))
    mean_filter = structuring_element / float(structuring_element.sum())
    return scipy.ndimage.filters.convolve(img, mean_filter)

def stdfilt(img, structuring_element):
    """Returns the local standard deviation of an image.

    The structuring element is a mask which determines the shape of the local
    area; see the documentation for local_mean_filter for details. The standard
    deviation is calculated within the local area."""
    local_sq = local_mean_filter(img**2, structuring_element)
    local_mean = local_mean_filter(img, structuring_element)
    return numpy.sqrt(local_sq - local_mean**2)

# TODO(nloomis): check on correlate vs convolve (arguments, and which makes
#                sense)

def contrast_stretch(img, low_percentile, high_percentile, low_target, high_target):
    """Returns a contrast-stretched image.

    An image is linearly stretched so that percentile(img, low_percentile)
    matches low_target in the output, and percentile(img, high_percentile)
    matches high_target. Use low_percentile=0 to stretch to the absolue minimum
    of the input image and high_percentile=100 for the absolute maximum.
    """
    img_low_value = numpy.percentile(numpy.ravel(img), low_percentile)
    img_high_value = numpy.percentile(numpy.ravel(img), high_percentile)
    img_range = img_high_value - img_low_value
    target_range = high_target - low_target
    return (img - img_low_value) / img_range * target_range + low_target
