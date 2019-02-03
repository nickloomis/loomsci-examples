"""
TODO(nloomis): describe package

Change log:
  2019/01/19 -- module started; nloomis@gmail.com
  2019/01/27 -- opencv amplitude-intensity lookup finished; nloomis@gmail.com
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
  def __init__(self, source_image, num_strips):
    #self.source_image = cv2utils.imread(filename, cv2.IMREAD_GRAYSCALE)
    # TODO(nloomis): hide internal variables
    self.source_image = source_image
    self.source_height, self.source_width = self.source_image.shape[:2]
    self.num_channels = imageutils.nchannels(self.source_image)
    self.num_strips = int(num_strips)
    self.strip_height = self.source_height / self.num_strips
    self.frequency = 0.65 # spatial frequency of sine; fixed for now
    lut_builder = SineIntensityLutBuilder(self.strip_height, self.frequency)
    self.linewidth = 1
    self.amplitude_lut, self.intensity_lut = lut_builder.table(self.linewidth)

  def _reshape_source(self):
    scale = float(self.num_strips) / self.source_height
    low_res_width = scale * self.source_width
    low_res_image = cv2.resize(self.source_image, (int(low_res_width), self.num_strips), interpolation=cv2.INTER_AREA);
    reshaped_image = cv2.resize(low_res_image, (self.source_width, self.num_strips), interpolation=cv2.INTER_CUBIC);
    return reshaped_image

  def _strip_center_y(self):
    return np.linspace(0.5 * self.strip_height, (self.num_strips - 0.5) * self.strip_height, self.num_strips)

  @classmethod
  def _fast_gamma(cls, image):
    """
    Fast estimate for the linear intensity corresponding to a sRGB value. The
    actual sRGB->linRGB inverse companding should be used if better accuracy is
    required; a gamma of 2.2 is an average.
    The input image is in [0, 255]. The output intensity map is [0, 1].
    """
    return np.power(image / 255, 2.2)

  def draw_opencv(self):
    reshaped_image = self._reshape_source()
    phase = np.linspace(0, 2*np.pi, self.num_channels + 1)
    sine_image = np.zeros(self.source_image.shape, dtype='uint8')
    for ch in range(self.num_channels):
      sine_image[:, :, ch] = self.draw_opencv_one_channel(reshaped_image[:,:,ch], phase[ch]);
    return sine_image

  def draw_opencv_one_channel(self, source_image, phase_offset):
    num_rows, width = source_image.shape[:2]
    y_centers = self._strip_center_y()
    x = np.linspace(0, width - 1, width)
    intensity_image = self._fast_gamma(source_image)
    scaled_intensity_image = intensity_image * np.max(self.intensity_lut)
    amplitude_image = np.reshape(np.interp(np.ravel(scaled_intensity_image), self.intensity_lut, self.amplitude_lut), intensity_image.shape)
    sine_image = np.zeros((self.source_height, self.source_width), dtype='uint8')
    for i in range(num_rows):
      y = amplitude_image[i, :] * np.sin(self.frequency * x + phase_offset) + y_centers[i]
      sine_image = plot_to_opencv(sine_image, x, y, 255, self.linewidth)
    plt.imshow(sine_image, cmap='Greys_r')
    plt.show()
    return sine_image

class SineIntensityLutBuilder(object):
  def __init__(self, strip_height, frequency):
    self.strip_height = strip_height
    self.max_amplitude = np.floor(0.5 * self.strip_height)
    self.lut_size = self.max_amplitude + 1
    self.omega = frequency
    self.period = 2 * np.pi / frequency

  def table(self, linewidth):
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
      intensity[i] = np.sum(intensity_image[:]) / max_total_intensity
    return amplitudes, intensity

# TODO(nloomis): options for diff't color scheme (dark on bright, bright on dark)
# TODO(nloomis): modify the frequency, either as an option or f(intensity) or f(image detail)
# TODO(nloomis): scale the frequency as a function of the image size; some fixed
#                number of cycles across the image, for example
# TODO(nloomis): option to set low_res_width using a different scale -- eg,
#                preserve more lateral detail
# TODO(nloomis): amplitude so that sine's coverage has about the right intensity on average over the region
# TODO(nloomis): options for RGB plots, with phase offsets in the sines between each color
# TODO(nloomis): options for line width
# TODO(nloomis): limit the maximum amplitude to be some fraction of the strip height
#                for a better appearance

def plot_to_opencv(img, x, y, color, linewidth):
  cv_points = [np.int32(np.vstack((x, y)).T)]
  cv2.polylines(img, cv_points, False, color, int(linewidth), cv2.LINE_AA)
  return img
