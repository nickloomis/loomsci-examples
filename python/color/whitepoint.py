# -*- coding: utf-8 -*-
"""
Store white point data for various illuminants.

Change log:
  2015/10/10 -- WhitePoint and illuminants added; nloomis@gmail.com
"""

import collections
import numpy

class WhitePoint(collections.namedtuple('WhitePoint',
                                        ['X', 'Y', 'Z', 'name'])):
    """Store white points for different illuminants."""

    def __mul__(self, other):
        #overridden so that whitepoints can easily be scaled to match the range
        #of an image or transform
        return self._replace(X=self.X * other,
                             Y=self.Y * other,
                             Z=self.Z * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        return self._replace(X=self.X / other,
                             Y=self.Y / other,
                             Z=self.Z / other)

    @property
    def XYZ(self):
        return numpy.array([self.X, self.Y, self.Z])

    @property
    def xy(self):
        return numpy.array([self.X, self.Y]) / (self.X + self.Y + self.Z)

    @property
    def xyy(self):
        sumxyz = numpy.sum(self.XYZ)
        return numpy.array([self.X / sumxyz, self.Y / sumxyz, self.Y])


def whitepoint_from_xy(x,y, name):
    """Create a whitepoint from the (x, y) coordinate (with Y = 1)."""
    #xy->xyz assuming Y = 1:
    xyz = numpy.array([x / y, 1.0, (1.0 - x - y) / y])
    #return the WhitePoint with this XYZ
    return WhitePoint(xyz[0], xyz[1], xyz[2], name)

#whitepoints of standard illuminants from wikipedia:
#https://en.wikipedia.org/wiki/Standard_illuminant
#2-degree uses the 2-degree observer functions to calculate xy; similar for
#10-degree.
A = whitepoint_from_xy(0.44757, 0.40745, 'A 2-degree')
B = whitepoint_from_xy(0.34842, 0.35161, 'B 2-degree')
C = whitepoint_from_xy(0.31006, 0.31616, 'C 2-degree')
D50 = whitepoint_from_xy(0.34567, 0.35850, 'D50 2-degree')
D50_10deg = whitepoint_from_xy(0.34773, 0.35952, 'D50 10-degree')
D55 = whitepoint_from_xy(0.33242, 0.34743, 'D55 2-degree')
D65 = whitepoint_from_xy(0.31271, 0.32902, 'D65 2-degree')
D65_10deg = whitepoint_from_xy(0.31382, 0.33100, 'D65 10-degree')
D75 = whitepoint_from_xy(0.29902, 0.31485, 'D75 2-degree')
E = WhitePoint(1.0, 1.0, 1.0,'E') #2-deg, 10-deg are the same by definition of Illum-E
F1 = whitepoint_from_xy(0.31310, 0.33727, 'F1 2-degree')
F2 = whitepoint_from_xy(0.37208, 0.37529, 'F2 2-degree')