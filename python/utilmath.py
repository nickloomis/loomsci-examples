"""
Utilities related to mathematics operations.

Change log:
  2015/09/20 -- copied out from raytracing.py so that the functions could be
                used by other codes; nloomis@gmail.com
  2016/01/17 -- quadratic solver added; nloomis@
"""
__authors__ = ('nloomis@gmail.com',)

import numpy



def norm_vec(v):
    """Returns a unity-length vector in the same direction as the input."""
    return v / norm(v)

def norm(v):
    """Convenience function for vector 2-norm."""
    return numpy.linalg.norm(v)

def min_nonneg(s):
    """Returns the smallest value which is also non-negative."""
    return min(nonneg(s))

def min_positive(s, thr=0):
    """Returns the smallest value which is also positive."""
    return min(positive(s, thr))

def nonneg(s):
    """Returns all non-negative values."""
    return filter(lambda x: x>=0, s)

def positive(s, thr=0):
    """Returns all positive values.

    The optional threshold can be used to set a different comparison value;
    by default, the threshold is zero. Due to numerical round-off, it may be
    helpful in some cases to set the threshold to be a small positive number,
    or a small negative number, such as 10*eps.
    """
    return filter(lambda x: x > thr, s)

def quadratic_solution(a, b, c):
    """Solves the quadratic equation.

    This version has improved precision by avoiding cancellation.
    Returns two roots (one or both of which may be None) in all cases.
    """
    if a == 0:
        if b == 0:
            # This is saying 0x^2 + 0x + c = 0, which has no solution for x.
            return None, None
        else:
            # THis set of conditions gives a linear equation.
            return -c/b, None
    discr = b**2 - 4. * a * c
    if discr == 0:
        # Two equal real roots
        return -b / (2. * a), None
    elif discr < 0:
        # The roots are imaginary; convert to complex numbers.
        root_discr = numpy.sqrt(discr + 0J)
    else:
        root_discr = numpy.sqrt(discr)
    x1 = (-b - numpy.sign(b) * root_discr) / (2. * a)
    x2 = c / (a * x1)
    return numpy.min([x1, x2]), numpy.max([x1, x2])

def nparray(arg):
    """Converts the argument to a numpy array."""
    if isinstance(arg, numpy.ndarray):    
        return arg
    elif isinstance(arg, list):
        return numpy.array(arg)
    elif isinstance(arg, (float, int)):
        return numpy.array([arg])
    else:
        raise TypeError(\
            'Not sure how to convert arg (tpye: %s) to a numpy array.'\
            % type(arg))
