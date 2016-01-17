"""
Geometric objects, and how to trace rays through those objects.

Change log:
  2015/09/20 -- copied out of raytracing.py for clarity; nloomis@gmail.com
"""

import numpy
import utilmath as umath


#constants
npzero = numpy.zeros((1,3)) #row vector; 3 zeros


def Plane(object):
    def __init__(self, point, normal):
        self.point = umath.nparray(point)
        self.normal = umath.norm_vec(umath.nparray(normal))

    def ray_intersect_dist(self, ray):
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

class Ellipsoid(object):
    
    def __init__(self, foci1, foci2, focal_parameter=1, 
                 n_inside=1.5, n_outside=1.0):
        self.foci1 = foci1
        self.foci2 = foci2
        self.focal_parameter = focal_parameter
        self.n_inside = n_inside
        self.n_outside = n_outside
        self._s2e_matrix = None #placeholder; None to designate it needs to
        #be calculated later
        
    def is_inside(self, point):
        self.check_set_s2e()
        #TODO: finish this.

    def is_on(self, point):
        self.check_set_s2e()
        #TODO: finish this.
    
    def _s2e_transform(self):
        """Computes the sphere-to-ellipsoid transform matrix."""
        #TODO: where does this matrix come from?
        #fortunately... don't need to compute this often.
        a = self.semimajor
        b = self.semiminor
        #stretch a sphere into an ellipsoid along the axes
        mat_stretch = numpy.diag([a, b, b, 1])
        e1 = umath.norm_vec(self.foci_diff)
        e2 = umath.norm_vec([1, -1, 0] * e1[1,0,2]) #st dot(e1, e2) = 0
        e3 = umath.norm_vec(numpy.corr(e1, e2)) #st dot(e1, e3)=0 and dot(e2, e3)=0
        mat_rotate = numpy.zeros((4,4))        
        mat_rotate[0:3, 0:3] = numpy.vstack((e1, e2, e3)).T
        mat_rotate[3, 3] = 1.0
        #shift the ellipsoid
        mat_shift = numpy.eye(4)
        mat_shift[0:3, 3] = self.center
        #combine the matrices
        return numpy.dot(mat_shift, numpy.dot(mat_rotate, mat_stretch))

    @property
    def foci1(self):
        return self._foci1
        
    @foci1.setter
    def foci1(self, value):
        self._foci1 = umath.nparray(value)
        self._s2e_matrix = None #this will invalidate the transform matrix
    
    @property
    def foci2(self):
        return self._foci2

    @foci2.setter
    def foci2(self, value):
        self._foci2 = umath.nparray(value)
        self._s2e_matrix = None #this will invalidate the transform matrix

    @property
    def center(self):
        return 0.5 * (self._foci1 + self._foci2)

    @property
    def foci_diff(self):
        return self.foci1 - self.foci2

    @property
    def semimajor(self):
        c = numpy.sqrt(sum(self.foci_diff**2))
        return numpy.sqrt(self.focal_parameter * c + c**2)
    
    @property
    def semiminor(self):
        c = numpy.sqrt(sum(self.foci_diff**2))
        return numpy.sqrt(self.semimajor - c**2)

    @property
    def s2e_matrix(self):
        if (not self._s2e_matrix) and self.foci1 and self.foci2:
            self._s2e_matrix = self._s2e_transform()
            self.s2e_inverse = numpy.linalg.inv(self.s2e_matrix)
            #TODO: need better reporting mechanism if s2e_matrix is singular.
            #TOOD: do we actually need the inverse?
            return self._s2e_matrix
    
#    pass
#    define the shape using some transforms on a sphere
#    build intersection codes to find where rays hit
        #thought: a sphere is a special case of an ellipsoid. is it then better
        #for the sphere to inherit from the ellipsoid?


class Sphere(Ellipsoid):
    """Defines a spherical surface."""
    def __init__(self, center=npzero, radius=1, nsphere=1.5, noutside=1.0):
        self.center = umath.nparray(center)
        self.radius = radius
        self.n_sphere = nsphere
        self.n_outside = noutside

#TODO: copy these over to the Ellipsoid class, include the transform and its
#inverse.
#    def is_inside(self, point):
#        """Test for whether the point is inside the sphere."""
#        return norm(point - self.center) < self.radius

#    def is_on(self, point):
#        """Test for whether the point is on the surface of the sphere."""
#        #TODO: give this a threshold
#        return norm(point - self.center) == self.radius

 #   def ray_intersect_dist(self, ray):
 #       """Returns the distance along the ray where it first hits the sphere."""
 #       #https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection
 #       oc = ray.point - self.center
 #       ldotoc = numpy.dot(ray.direction, oc)
 #       det = ldotoc**2 - norm(oc) + self.radius**2
 #       if det < 0:
 #           return None
 #       det_root = numpy.sqrt(det)
 #       #find the first intersection along the positive direction of the ray
 #       return min_positive([-ldotoc + det_root, -ldotoc - det_root])

    #TODO: def drawing function to show the object
