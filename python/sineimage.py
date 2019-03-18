"""
TODO(nloomis): describe package

Inspired by the following sources:
https://www.evilmadscientist.com/2016/axidraw-v3/
https://github.com/gwygonik/SquiggleDraw

Change log:
  2019/01/19 -- module started; nloomis@gmail.com
  2019/01/27 -- opencv amplitude-intensity lookup finished; nloomis@gmail.com
  2019/02/04 -- reorganized variables so that more could be changed on-the-fly
                without rebuilding the Plotter; nloomis@gmail.com
"""
__authors__ = ('nloomis@gmail.com',)

import cv2
import cv2utils
import imageutils
import matplotlib.pyplot as plt
import matplotlib.colors as mp_color
import numpy as np
import scipy.special as special

class Plotter(object):
  def __init__(self, source_image, num_strips, num_cycles, linewidth=1):
    self._source_image = source_image
    self._source_height, self._source_width = self._source_image.shape[:2]
    self._num_channels = imageutils.nchannels(self._source_image)
    self._num_strips = int(num_strips)
    self._strip_height = self._source_height / self._num_strips
    # the following properties can be changed at any time.
    self.num_cycles = num_cycles
    self.linewidth = linewidth
    self.contrast_percentiles = (2, 98)
    # width_detail: the amount of detail in the x-direction relative to the
    # detail in the y (strip height) direction
    self.width_detail = 2

  def _spatial_frequency(self):
    return 2 * np.pi * self.num_cycles / (self._source_width)

  def amplitude_map(self):
    """Returns the sine wave's amplitudes as a 2d map."""
    reshaped_image = self._reshape_source()
    return self._amplitude_lut(reshaped_image)

  def _reshape_source(self):
    scale = float(self._num_strips) / self._source_height
    low_res_width = scale * self._source_width * self.width_detail
    low_res_image = cv2.resize(self._source_image, (int(low_res_width), self._num_strips), interpolation=cv2.INTER_AREA);
    reshaped_image = cv2.resize(low_res_image, (self._source_width, self._num_strips), interpolation=cv2.INTER_CUBIC);
    return reshaped_image

  def _amplitude_lut(self, source_image):
    """
    Calculates the amplitude of the sine waves needed to reproduce the provided
    source image using a look-up table.
    """
    #intensity_map = self._fast_gamma(source_image)
    intensity_map = source_image/255.0
    lut = SineIntensityLut(self._strip_height, self._spatial_frequency(), self.linewidth)
    scaled_intensity_map = imageutils.contrast_stretch(intensity_map, self.contrast_percentiles[0], self.contrast_percentiles[1], 0.0, lut.maximum_intensity())
    return lut.apply(scaled_intensity_map)
    
  @classmethod
  def _fast_gamma(cls, image):
    """
    Fast estimate for the linear intensity corresponding to a sRGB value. The
    actual sRGB->linRGB inverse companding should be used if better accuracy is
    required; a gamma of 2.2 is an average.
    The input image is in [0, 255]. The output intensity map is [0, 1].
    """
    return np.power(image / 255, 2.2)

  def draw(self):
    amplitude_map = self.amplitude_map()
    phase = np.linspace(0, 2*np.pi, self._num_channels + 1)
    sine_image = np.zeros(self._source_image.shape, dtype='uint8')
    for ch in range(self._num_channels):
      sine_image[:, :, ch] = self._draw_opencv_one_channel(amplitude_map[:,:,ch], phase[ch]);
    return sine_image

  def _draw_opencv_one_channel(self, amplitude_map, phase_offset):
    num_rows, width = amplitude_map.shape[:2]
    y_centers = self._strip_center_y()
    x = np.linspace(0, width - 1, width)
    sine_image = np.zeros((self._source_height, self._source_width), dtype='uint8')
    for i in range(num_rows):
      y = amplitude_map[i, :] * np.sin(self._spatial_frequency() * x + phase_offset) + y_centers[i]
      sine_image = plot_to_opencv(sine_image, x, y, 255, self.linewidth)
    return sine_image

  def _strip_center_y(self):
    return np.linspace(0.5 * self._strip_height, (self._num_strips - 0.5) * self._strip_height, self._num_strips)


class SineIntensityLut(object):
  def __init__(self, strip_height, frequency, linewidth):
    self.strip_height = strip_height
    self.max_amplitude = np.floor(0.5 * self.strip_height)
    self.lut_size = self.max_amplitude + 1
    self.omega = frequency
    self.period = 2 * np.pi / frequency
    self.amplitude_lut, self.intensity_lut = self._build_table(linewidth)

  def apply(self, intensity_map):
    amplitude_map = np.reshape(np.interp(np.ravel(intensity_map), self.intensity_lut, self.amplitude_lut), intensity_map.shape)
    return amplitude_map

  def maximum_intensity(self):
    return np.max(self.intensity_lut)

  def _build_table(self, linewidth):
    """
    Creates a look-up table of amplitude vs intensity.
    """
    num_cycles = 5  # number of cycles to plot (to limit edge effects)
    bkg = np.zeros((int(self.strip_height), round(self.period * num_cycles)), dtype='uint8')
    # The intensity (linear RGB) is scaled to [0, 1] for this module. The
    # maximum intensity occurs when all pixels in the intenstiy map of the
    # plotted image have a value of 1.
    max_total_intensity = bkg.shape[0] * bkg.shape[1]
    amplitudes = np.linspace(0, self.max_amplitude, self.lut_size)
    width = bkg.shape[1]
    x = np.linspace(0, width - 1, width)
    intensity = np.zeros(amplitudes.shape)
    for i, a in enumerate(amplitudes):
      y = self.strip_height * 0.5 + a * np.sin(self.omega * x)
      plotted_image = plot_to_opencv(bkg, x, y, 255, linewidth)
      intensity_image = Plotter._fast_gamma(plotted_image)
      #intensity_image = plotted_image
      intensity[i] = np.sum(intensity_image[:]) / max_total_intensity
    return amplitudes, intensity

# TODO(nloomis): options for diff't color scheme (dark on bright, bright on dark)
# TODO(nloomis): modify the frequency, either as an option or f(intensity) or f(image detail)
# TODO(nloomis): scale the frequency as a function of the image size; some fixed
#                number of cycles across the image, for example
# TODO(nloomis): option to set low_res_width using a different scale -- eg,
#                preserve more lateral detail
# TODO(nloomis): options for line width
# TODO(nloomis): limit the maximum amplitude to be some fraction of the strip height
#                for a better appearance
# TODO(nloomis): allow line-drawing color to vary for parts of the image darker
#                than allowed by a LUT with a line color of 255

def plot_to_opencv(img, x, y, color, linewidth):
  cv_points = [np.int32(np.vstack((x, y)).T)]
  cv2.polylines(img, cv_points, False, color, int(linewidth), cv2.LINE_AA)
  return img
