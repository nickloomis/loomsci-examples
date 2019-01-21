"""
TODO(nloomis): describe package

Change log:
  2019/01/19 -- module started; nloomis@gmailcom
"""
__authors__ = ('nloomis@gmail.com',)

import cv2
import cv2utils
import matplotlib.pyplot as plt
import numpy as np

class Plotter(object):
  def __init__(self, filename, num_strips):
    self.source_image = cv2utils.imread(filename, cv2.IMREAD_GRAYSCALE)
    self.source_height, self.source_width = self.source_image.shape
    self.num_strips = int(num_strips)
    self.strip_height = self.source_height / self.num_strips

  def _reshape_source(self):
    scale = float(self.num_strips) / self.source_height
    low_res_width = scale * self.source_width
    low_res_image = cv2.resize(self.source_image, (int(low_res_width), self.num_strips), interpolation=cv2.INTER_AREA);
    reshaped_image = cv2.resize(low_res_image, (self.source_width, self.num_strips), interpolation=cv2.INTER_CUBIC);
    return reshaped_image

  def _strip_center_y(self):
    return np.linspace(0.5 * self.strip_height, (self.num_strips - 0.5) * self.strip_height, self.num_strips)

  @classmethod
  def _fast_gamma(cls, reshaped_image):
    return np.power(reshaped_image / 255, 2.2) * 255

  def draw(self):
    reshaped_image = self._reshape_source()
    num_rows, width = reshaped_image.shape
    y_centers = self._strip_center_y()
    x = np.linspace(0, width - 1, width)
    omega = 0.65   # spatial frequency
    # intensity_image = self._fast_gamma(reshaped_image)
    intensity_image = reshaped_image  # when amplitude ~intensity, this "version" looks better
    for i in range(num_rows):
      amplitude = self.strip_height * 0.5 * intensity_image[i, :] / 255
      plt.plot(x, amplitude * np.sin(omega * x) + y_centers[i], color='black')
    plt.axis('off')
    plt.gca().invert_yaxis()  # like axis(ij)
    plt.show()
    # to save out, don't show the plot. also, may need to resize it? or use linewidth=...
#    plt.savefig("foo.png", bbox_inches='tight', dpi=200)

# TODO(nloomis): option to scale to max intensity
# TODO(nloomis): save out image
# TODO(nloomis): options for diff't color scheme
# TODO(nloomis): modify the frequency, either as an option or f(intensity) or f(image detail)
# TODO(nloomis): option to set low_res_width using a different scale -- eg,
#                preserve more lateral detail
# TODO(nloomis): amplitude so that sine's coverage has about the right intensity on average over the region
# TODO(nloomis): options for RGB plots, with phase offsets in the sines between each color
