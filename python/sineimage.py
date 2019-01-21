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


def reshape_source(filename, num_rows_final):
  source_image = cv2utils.imread(filename, cv2.IMREAD_GRAYSCALE)
  height, width = source_image.shape
  scale = float(num_rows_final) / height
  strip_height = height / num_rows_final
  low_res_width = scale * width
  low_res_image = cv2.resize(source_image, (int(low_res_width), int(num_rows_final)), interpolation=cv2.INTER_AREA);
  reshaped_image = cv2.resize(low_res_image, (width, int(num_rows_final)), interpolation=cv2.INTER_CUBIC);
  return reshaped_image, strip_height;

def strip_center_y(num_rows, strip_height):
  return np.linspace(0.5 * strip_height, (num_rows - 0.5) * strip_height, num_rows)

def fast_gamma(reshaped_image):
  return np.power(reshaped_image / 255, 2.2) * 255

def draw_sinusoids(reshaped_image, strip_height):
  num_rows, width = reshaped_image.shape
  y_centers = strip_center_y(num_rows, strip_height)
  x = np.linspace(0, width - 1, width)
  omega = 0.5
  intensity_image = fast_gamma(reshaped_image)
  for i in range(num_rows):
    amplitude = strip_height * 0.5 * intensity_image[i, :] / 255
    plt.plot(x, amplitude * np.sin(omega * x) + y_centers[i], color='black')
  plt.box(False)
  plt.show()

# TODO(nloomis): convert sRGB grayscale->linear intensity
