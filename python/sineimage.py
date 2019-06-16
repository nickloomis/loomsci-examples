"""
Draws an image using a set of horizontal sinusoids with varying amplitude.

Change log:
  2019/01/19 -- module started; nloomis@gmail.com
  2019/01/27 -- opencv amplitude-intensity lookup finished; nloomis@gmail.com
  2019/06/14 -- contrast stretching working; white or black background;
                nloomis@gmail.com
  2019/06/16 -- fixed number of periods across the width; wait to compute
                lut until draw() for better flexibility to change parameters
                without constructing a new object; nloomis@
"""
__authors__ = ('nloomis@gmail.com',)

import cv2
import cv2utils
import imageutils
import numpy as np

# Example:
#  f = cv2utils.imread('foo.jpg')
#  S = sineimage.Plotter(cv2utils.resize(f, 1.5), 35)
#  r = cv2utils.resize(sineimage.draw(S), 1 / 1.5)
#  cv2utils.imwrite(f, 'foo-squiggle.jpg')

class Plotter(object):
  def __init__(self, source_image, num_strips=40):
    self._source_image = source_image

    # Derived attributes
    self._source_height, self._source_width = self._source_image.shape[:2]
    self._num_channels = imageutils.nchannels(self._source_image)

    # Independent Parameters
    self.num_strips = num_strips
    self.num_periods = 95;
    self.linewidth = 2
    # Percentile of peak/shadow to over/under expose
    self.constrast_stretch_percentile = 10
    # Set background to be black (0), white (255), or somewhere in between
    self.background_color = 255
    # Set the line color to be either fully dark (0), fully bright (255), or
    # somewhere in between
    self.line_color = 0

  @property
  def num_strips(self):
    return self._num_strips
  
  @num_strips.setter
  def num_strips(self, num_strips):
    self._num_strips = int(num_strips)

  @property
  def _frequency(self):
    """Returns the spatial frequency of the sine, sin(w*x)."""
    period = self._source_width / self.num_periods
    return 2 * np.pi / period

  @property
  def _strip_height(self):
    """Returns the height in pixels of each pixel strip used to draw a sine."""
    return self._source_height / self.num_strips  

  def _reshape_source(self):
    scale = float(self.num_strips) / self._source_height
    low_res_width = scale * self._source_width
    low_res_image = cv2.resize(self._source_image, (int(low_res_width), self.num_strips), interpolation=cv2.INTER_AREA);
    reshaped_image = cv2.resize(low_res_image, (self._source_width, self.num_strips), interpolation=cv2.INTER_CUBIC);
    return reshaped_image

  def _amplitude_map(self, source_image):
    """
    Calculates the amplitude of the sine waves needed to reproduce the provided
    source image.
    """
    intensity_map = self._fast_gamma(source_image)

    # Build the look-up table for intensity-to-sine-amplitude.
    amplitude_lut = SineIntensityLut(self._strip_height, self._frequency, self.linewidth, self.background_color, self.line_color)

    high_pctl = 100 - self.constrast_stretch_percentile
    scaled_intensity_map = imageutils.contrast_stretch(intensity_map, self.constrast_stretch_percentile, high_pctl, amplitude_lut.minimum_intensity(), amplitude_lut.maximum_intensity())
    return amplitude_lut.apply(scaled_intensity_map)
    
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
    reshaped_image = self._reshape_source()
    amplitude_map = self._amplitude_map(reshaped_image)
    phase = np.linspace(0, 2*np.pi, self._num_channels + 1)
    sine_image = np.zeros(self._source_image.shape, dtype='uint8')
    for ch in range(self._num_channels):
      sine_image[:, :, ch] = self._draw_opencv_one_channel(amplitude_map[:,:,ch], phase[ch]);
    return sine_image

  def _draw_opencv_one_channel(self, amplitude_map, phase_offset):
    num_rows, width = amplitude_map.shape[:2]
    y_centers = self._strip_center_y()
    x = np.linspace(0, width - 1, width)
    sine_image = np.full((self._source_height, self._source_width), self.background_color, dtype='uint8')
    for i in range(num_rows):
      y = amplitude_map[i, :] * np.sin(self._frequency * x + phase_offset) + y_centers[i]
      sine_image = plot_to_opencv(sine_image, x, y, self.line_color, self.linewidth)
    return sine_image

  def _strip_center_y(self):
    return np.linspace(0.5 * self._strip_height, (self.num_strips - 0.5) * self._strip_height, self.num_strips)


# Look-up table for the amplitude of a sine wave needed to produce a particular
# intensity.
class SineIntensityLut(object):
  def __init__(self, strip_height, frequency, linewidth, background_color, line_color):
    self.strip_height = strip_height
    self.omega = frequency
    self.background_color = background_color
    self.line_color = line_color
    # Derived attributes
    self.max_amplitude = np.floor(0.5 * self.strip_height)
    self.lut_size = self.max_amplitude + 1
    self.period = 2 * np.pi / frequency
    # Finally, construct the LUT.
    self.amplitude_lut, self.intensity_lut = self._build_table(linewidth)

  def apply(self, intensity_map):
    intensity = self.intensity_lut;
    amplitude = self.amplitude_lut;
    if intensity[-1] < self.intensity_lut[0]:
      # numpy.interp expects the independent variable to be monotonically
      # increasing.
      flip_axis = 0
      intensity = np.flip(intensity, flip_axis)
      amplitude = np.flip(amplitude, flip_axis)
    amplitude_map = np.reshape(np.interp(np.ravel(intensity_map), intensity, amplitude), intensity_map.shape)
    return amplitude_map

  def minimum_intensity(self):
    return np.min(self.intensity_lut)

  def maximum_intensity(self):
    return np.max(self.intensity_lut)

  def _build_table(self, linewidth):
    """Creates a look-up table of amplitude vs intensity."""
    num_cycles = 5  # number of cycles to plot; >>1 to limit edge effects
    bkg = np.full((int(self.strip_height), round(self.period * num_cycles)), self.background_color, dtype='uint8')
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
      plotted_image = plot_to_opencv(bkg, x, y, self.line_color, linewidth)
      intensity_image = Plotter._fast_gamma(plotted_image)
      intensity[i] = np.sum(intensity_image[:]) / max_total_intensity
    return amplitudes, intensity

def plot_to_opencv(img, x, y, color, linewidth):
  """Uses OpenCV to plot a set of connected (x,y) points."""
  cv_points = [np.int32(np.vstack((x, y)).T)]
  cv2.polylines(img, cv_points, False, color, int(linewidth), cv2.LINE_AA)
  return img

# TODO(nloomis): modify the frequency, either as an option or f(intensity) or f(image detail)
# TODO(nloomis): option to set low_res_width using a different scale -- eg,
#                preserve more lateral detail
# TODO(nloomis): limit the maximum amplitude to be some fraction of the strip height
#                for a better appearance
# TODO(nloomis): allow line-drawing color to vary if amplitude=0 is a significant
#                approximation error

