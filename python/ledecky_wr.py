"""
Fits an exponential curve to Katie Ledecky's world record swims in the 800m
freesyle through the 2016 Rio Olympics.

Change log:
  2016/08/13 -- module started; nloomis@gmail.com
  2016/08/14 -- documentation added; nloomis@gmail.com
"""
__authors__ = ('nloomis@gmail.com',)

import datetime
import matplotlib.pyplot as plt
import numpy
from scipy.optimize import curve_fit

def WorldRecordData():
  """Returns Kate Ledecky's world record times for the 800m freestyle."""
  wr = {}
  wr[datetime.date(2013, 8, 3).toordinal()] = datetime.time(0, 8, 13, 860000)
  wr[datetime.date(2014, 6, 22).toordinal()] = datetime.time(0, 8, 11, 0)
  wr[datetime.date(2015, 8, 8).toordinal()] = datetime.time(0, 8, 7, 390000)
  wr[datetime.date(2016, 1, 17).toordinal()] = datetime.time(0, 8, 6, 680000)
  wr[datetime.date(2016, 8, 12).toordinal()] = datetime.time(0, 8, 4, 790000)
  return wr

def TimeToSeconds(time_object):
  """Returns the number of seconds since 0h0m0s for a datetime.time object."""
  return time_object.hour * 3600 + time_object.minute * 60 +\
      time_object.second + time_object.microsecond / 1000000.

def SecondsToTime(sec):
  """Returns a time object representing the number of seconds since 0h0m0s."""
  hour = int(numpy.floor(sec / 3600.))
  sec_rem = sec - hour * 3600
  minute = int(numpy.floor(sec_rem / 60.))
  sec_rem = sec - minute * 60
  second = int(numpy.floor(sec_rem))
  microsecond = int(numpy.round((sec_rem - second) * 1000000))
  return datetime.time(hour, minute, second, microsecond)

def ExponentialWithOffset(x, amp, tau, offset):
  """Exponential with an offset."""
  return amp * numpy.exp(-x / tau) + offset

def Fit():
  """Fit Ledecky's times to an exponential curve w an offset and plot the fit.

  Returns (p_opt, p_cov), the optimized parameter values and covariance 
  matrix. The parameters are in the order of (a, tau, offset) and are the best-
  fit to ExponentialWithOffset(). The initial data point at day=0 is the first
  world record. a and offset are in seconds; tau is in days."""
  wr = WorldRecordData();
  times = numpy.array([TimeToSeconds(t) for t in wr.values()])
  days = numpy.array(wr.keys())
  amp_init = numpy.max(times) - numpy.min(times)
  offset_init = numpy.min(times)
  delta_days = numpy.max(days) - numpy.min(days)
  tau_init = delta_days / amp_init
  ig = [amp_init, tau_init, offset_init]
  popt, pcov = curve_fit(ExponentialWithOffset, days - min(days), times, p0=ig)

  test_days = numpy.linspace(0, 2 * delta_days, 200)
  test_times = ExponentialWithOffset(test_days, *popt)

  plt.plot(days - min(days), times, 'o')
  plt.plot(test_days, test_times)
  plt.xlabel('days since first wr')
  plt.ylabel('world record time (s)')
  plt.title('Katie Ledecky 800m freestyle WR times')
  plt.show()

  return popt, pcov
