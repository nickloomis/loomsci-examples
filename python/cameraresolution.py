"""Print and camera visual resolution tools.

Simple utilities to calculate the number of camera pixels required to achieve
printed photos which are limited in their detail by the human visual system.

Change log:
  2016/09/24 -- module started; nloomis@gmail.com
  2016/09/27 -- documentation added; nloomis@gmail.com
  2016/10/08 -- plotting of camera pixels vs viewing distance added; nloomis@
"""
__authors__ = ('nloomis@gmail.com')

import numpy

def tand(v):
  """Returns the tangent of an angle in degrees."""
  return numpy.tan(v * numpy.pi / 180.)

def PrintDpiVisionLimited(viewing_distance):
  """Returns the number of dots per unit of viewing distance for 20/20 vision.

  The human eye can resolve about one arc-minute of detail (20/20 vision), which
  gives a minimum size that would be necessary to reproduce in a print for a
  certain viewing distance. The inverse of the dot size gives the number of dots
  which would need to be printed per unit length to achieve the maximum visual
  resolution.

  The returned value is the number of dots per unit of viewing distance. For
  example, if the viewing distance is in inches, the returned value is the dots
  per inch (or DPI). Similarly, if the viewing distance is given in millimeters,
  the returned value is dots-per-mm."""
  dot_size = viewing_distance * tand(1.0 / 60)
  return 1.0 / dot_size

def CameraSbpInMpx(print_width, print_height, viewing_distance):
  """Returns the number of megapixels in a camera for acuity-limited prints.

  The print width, print height, and viewing distance should all be in the same
  units.

  SBP stands for 'space-bandwidth product', and is the total number of samples
  (ie, pixels) that the image covers on the camera sensor."""
  print_dpi = PrintDpiVisionLimited(viewing_distance)
  # Camera sensors use (typically) Bayer filters, where the red and blue
  # channels are sampled once every two pixels, laterally.
  camera_dpi = 2.0 * print_dpi
  camera_sbp = print_width * print_height * camera_dpi**2.0
  mpx_conversion = 1024**2
  return camera_sbp / mpx_conversion

def TypicalViewingDistance(print_width, print_height):
  """Returns the typical viewing distance, about 1.5x the image diagonal."""
  diagonal = numpy.sqrt(print_width**2.0 + print_height**2.0)
  return 1.5 * diagonal

def CameraSbpFromRatios(aspect_ratio, viewing_distance_ratio):
  """Returns the number of camera pixels using an aspect ratio and view ratio.

  The aspect ratio is the width/height ratio of the printed image. The viewing
  distance ratio is the distance of the viewer from the print compared to the
  diagonal of the print.

  The raw number of camera pixels is returned. Divide by 1024**2 to convert to
  megapixels."""
  denom = viewing_distance_ratio**2.0 * \
         (1 + aspect_ratio**2.0) * \
         tand(1./60)**2.0
  return 4.0 * aspect_ratio / denom

def PlotCameraSbpVsK():
  """Plots the camera SBP as a function of the viewing distance multiplier, k"""
  import matplotlib.pyplot as plt
  sbp_at_unity = CameraSbpFromRatios(4/3., 1.0);
  k = numpy.linspace(1, 1.8, 100)
  sbp = sbp_at_unity / k**2.0 / 1024**2
  plt.plot(k, sbp)
  plt.xlabel('viewing distance multiplier, k')
  plt.ylabel('camera MPx')
  plt.title('Camera pixels vs viewing distance')
  plt.grid('on')
  plt.show()
