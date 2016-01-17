"""
Ray-tracing functions.

Change log:
  2015/09/01 -- begin writing module in order to find power and angle of rays
                as they hit spheres of water, ie, rainbows; nloomis@gmail.com
  2015/09/20 -- copied out geometric objects to raytracinggeometry.py, math
                utilities to utilmath.py, and geometric optics functions to
                geometricoptics.py; nloomis@
  2016/01/16 -- Ray updated to have property setters, which makes it easier to
                specify the position and direction using simple lists, ie, 
                ray.position = [0, 1, 2]; nloomis@
"""
__authors__ = ('nloomis@gmail.com',)

import copy
import numpy
import geometricoptics as geo
import utilmath as umath


#
# define physical objects
#

class Ray(object):
    def __init__(self, point=[0, 0, 0], direction=[0, 0, 1],
                 wavelength=1, intensity=1, payload=None, is_active=True):
        """Defines a ray based on a reference point and a direction.

        Additional descriptors, like wavelength, amplitude, or a specific
        payload can be added.
        """
        self.point = point
        self.direction = direction
        self.wavelength = wavelength
        self.intensity = intensity
        self.payload = payload

    @property
    def point(self):
        return self._point
    
    @point.setter
    def point(self, value):
        self._point = umath.nparray(value)

    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value):
        self._direction = umath.norm_vec(umath.nparray(value))

    def propagate(self, distance):
        """Propagates forward by a distance along the ray direction."""
        self.point = self.point + self.direction * distance

    def propagate_to_plane(self, plane):
        """Propagates forward until the ray intersects the plane."""
        dist = plane.ray_intersect_dist(self)
        self.propagate(dist)


#class TracedRays(object):
#    history of where rays go as they interact with some surfaces, and
#    drawing functions for showing the rays
#good use of lists for final result, queues for the rays in the working copy?


#
# optics-raytracing functions
#

def angle_of_incidence(direction, s_norm):
    """Find the angle of incidence for a ray direction and a surface normal.
    
    direction and s_norm are numpy arrays."""
    return numpy.arccos(numpy.dot(direction, s_norm))
    #TODO: check this

def reflect_ray(ray, normal):
    """Reflect a ray from a surface with a given normal.

    Modifies the ray direction in-place. Additionally returns the ray. Note
    that no modifications are made in the payload or amplitude at this time.
    The normal is a numpy array."""
    ndots = numpy.dot(ray.direction, normal)
    ray.direction = ray.direction - 2.0 * ndots * normal
    return ray

def refract_ray(ray, normal, ni, nt):
    #TODO: docstring
#normal is a numpy array.
    #assumption: normal is pointed towards ni (the incoming rays)
    eta = ni / nt #ratio of indices
    c1 = -numpy.dot(ray.direction, normal)
    cs2 = 1 - eta**2 * (1 - c1**2)
    if cs2 > 0:
        #ray is transmitted
        trans_ray = copy.copy(ray)
        trans_ray.direction = eta * ray.direction +\
                              (eta * c1 - numpy.sqrt(cs2)) * normal
        theta_i = -numpy.arccos(c1)
        R, T = geo.fresnel_coefs(ni, theta_i, nt)
        trans_ray.intensity *= T
    else:
        #TIR occurs in this case
        R = 1.0
        trans_ray = None
    ray = reflect_ray(ray, normal) #note: modified in-place
    ray.intensity *= R
    return trans_ray, ray #transmitted, reflected

def refract_ray_sphere(ray, sphere):
    #TODO: docstring
    #decide if the ray is starting inside or outside the sphere, and set the
    #indices correctly:
    if sphere.is_inside(ray.point):
        ni, nt = sphere.n_sphere, sphere.n_outside
    else:
        ni, nt = sphere.n_outside, sphere.n_sphere
    #move the ray forward to where it hits the sphere
    dist = sphere.ray_intersect_dist(ray)
    ray.propagate(dist)
    #find the surface normal at the intersection and its angle
    s_norm = umath.norm_vec(ray.point - sphere.center) #outwards-facing surface normal
    trans_ray, refl_ray = refract_ray(ray, s_norm, ni, nt) #TODO: check the sign of the normal! should point towards the ray.
    return trans_ray, refl_ray