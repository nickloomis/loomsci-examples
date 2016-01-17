"""
Geometric objects, and how to trace rays through those objects.

Change log:
  2015/09/20 -- copied out of raytracing.py for clarity; nloomis@gmail.com
  2016/01/17 -- removed spurious ellipsoid definition; fixed bugs; added a
                conic object; nloomis@
"""
__authors__ = ('nloomis@gmail.com',)

import numpy
import utilmath as umath


#constants
npzero = numpy.zeros((1, 3)) #row vector; 3 zeros


class Plane(object):
    def __init__(self, point, normal):
        self.point = umath.nparray(point)
        self.normal = umath.norm_vec(umath.nparray(normal))

    def RayIntersectDist(self, ray):
        """Returns the distance along the ray where it hits the plane."""
        #https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
        ldotn = numpy.dot(ray.direction, self.normal)
        if ldotn == 0:
            #ldotn: the line and plane are parallel; if num==0, then the line is
            #in the plane (and ldotn will consequently also be zero). it's thus
            #sufficient to check that ldotn is zero.
            return None
        num = numpy.dot(self.point - ray.point, self.normal)
        return num / ldotn

class Conic(object):
    """Rotationally-symmetric conic shape: ellipsoid, paraboloid, hyperboloid.
    (Spheres are special cases of ellipsoids.)
    The z-axis is the axis of symmetry. The radius uses the optical sign
    convention to determine opening direction.
    """
    def __init__(self, radius=1, conic=0, vertex=npzero):
        self.radius = radius
        self.conic = conic
        self.vertex = vertex

    @property
    def vertex(self):
        return self._vertex

    @vertex.setter
    def vertex(self, value):
        self._vertex = umath.nparray(value)

    def RayIntersectDist(self, ray):
        """The distance along the ray to the first intersection with the conic.

        If the distance is a complex number, it indicates that the ray does
        not intersect the conic; the real part gives the closest approach.
        Only positive distances are returned (ie, only distances in the same
        direction of the ray).
        """
        t1, t2 = umath.quadratic_solution(*self._IntersectQuadraticTerms(ray))
        return umath.min_positive([t1, t2], 1e-12)

    def _IntersectQuadraticTerms(self, ray):
        """Returns the coeffs of a quadratic for a ray-object intersect.

        Uses Murphy's 'Simple Three-D Raytrace Algorithm'. The coefficients are
        passed to a quadratic solver to find the intersection distances, up
        to two for a conic.
        """
        #shift the ray's point by sutracting the vertex location of the conic
        ray_point = ray.point - self._vertex
        A = ray.direction[0]**2 + ray.direction[1]**2 + \
            (self.conic + 1.) * ray.direction[2]**2
        B = 2. * ray_point[0] * ray.direction[0] + \
            2. * ray_point[1] * ray.direction[1] + \
            2. * (self.conic + 1.) *ray_point[2] * ray.direction[2] - \
            2. * self.radius * ray.direction[2]
        C = ray_point[0]**2 + ray_point[1]**2 + \
            (self.conic + 1.) * ray_point[2]**2 - 2.*self.radius * ray_point[2]
        return A, B, C

    def Sag(self, x, y):
        """Calculates the sag at the specific radial point (x,y).

        The vertex position is used to shift the conic as needed. The returned
        sag is then the distance from the xy plane to the conic at the specified
        point.
        """
        xv = x - self._vertex[0]
        yv = y - self._vertex[1]
        rho2 = xv**2 + yv**2
        c = 1. / self.radius
        conic_sag = c * rho2 / \
          (1 + numpy.sqrt(1 - (1 + self.conic) * c**2 * rho2))
        return conic_sag + self._vertex[2]