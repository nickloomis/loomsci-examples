"""Simple focus detection methods for use with holograms.

Change log:
  2016/01/24 -- module started; nloomis@gmail.com
"""
__authors__ = ('nloomis@gmail.com',)

import digitalholography as dhi

import imageutils
import scipy.ndimage
try:
    from skimage import filters
except ImportError:
    # handles the case where skimage is v0.10 (the filter module was renamed
    # to filters in v0.11)
    from skimage import filter as filters
from skimage.morphology import disk

#scipy.ndimage.filters.convolve

def SobelMetric(self, field, unused_opts):
  # Sobel uses [1, 2, 1; 0, 0, 0; -1, -2, -1]
  #return filters.sobel(numpy.abs(field))
  return scipy.ndimage.sobel(numpy.abs(field))

def PrewittMetric(self, field, unused_opts):
  # Prewitt uses [1,1, 1; 0, 0, 0; -1, -1, -1]
  #return filters.prewitt(numpy.abs(field))
  return scipy.ndimage.prewitt(numpy.abs(field))

def ScharrMetric(self, field, unused_opts):
  # Scharr uses [3, 10, 3; 0, 0, 0; -3, -10, -3]
  return filters.scharr(numpy.abs(field))

def GaussianGradientMetric(self, field, opts):
  # TODO: use the options
  sigma = 2.0
  return scipy.ndimage.gaussian_gradient_magnitude(numpy.abs(field), sigma)

def GaussianLaplaceMetric(self, field, opts):
  """Laplace filter using Gaussian second derivatives."""
  sigma = 2.0
  return scipy.ndimage.gaussian_laplace(numpy.abs(field), sigma)

def LaplaceMetric(self, field, opts):
  #TODO: use the options?
  #return filters.laplace(numpy.abs(field))
  return scipy.ndimage.laplace(numpy.abs(field))

def RobersMetric(self, field, unused_opts):
  return filters.robers(numpy.abs(field))

def EntropyMetric(self, field, opts):
  #TODO: use the options?
  return filters.rank.entropy(numpy.abs(field), disk(5))

def RangeMetric(self, field, opts):
  """Local range within the structuring element."""
  #TODO: use the options
  return filters.rank.gradient(numpy.abs(field), disk(5))

def SteerableDerivativeMetric(self, field, opts):
  steerable_filter = imageutils.steerable_deriv(sigma=1.5)
  S, _, _, _ = imageutils.apply_gradient_filter(numpy.abs(field,
                                                steerable_filter))
  return S



def FocusStack(holo, z_position_list, focus_function, options=None):
  """Builds a stack of focus data through a hologram volume.

  The hologram is reconstructed at each position in the z_position_list, and the
  depth which results in the maximum value of the focus_function at that pixel
  is retained. The focus function should accept a complex-valued reconstruction
  field and should return a scalar for each pixel that indicates the degree of
  focus at that location."""
  max_focus_value = numpy.zeros(holo.data.size)
  max_foxus_pixel = numpy.zeros(holo.data.size)
  for z in z_position_list:
    field = holo.reconstuct(z)
    this_focus = focus_function(field, options)
    max_focus_value = numpy.maximum(max_focus_value, this_focus)
    is_at_max = max_focus_value == this_focus
    max_focus_pixel(is_at_max) = field(is_at_max)
  return max_focus_value, max_focus_pixel