"""
Basic geometric optics equations.

Change log:
  2015/09/20 -- moved from raytracing.py so that the functions could be used
                more generally; nloomis@gmail.com
"""

import numpy


def refraction_angle(ni, theta_i, nt):
    """Angle of refraction through an interface (Snell's law).

    ni: index of refraction in incident media
    theta_i: incidence angle
    nt: index of refraction in transmitting media

    If the angle theta_i is beyond TIR, returns numpy.nan.
    """
    return numpy.arcsin(ni * numpy.sin(theta_i) / float(nt))

def tir_angle(ni, nt):
    """Incidence angle where total internal reflection (TIR) occurs.

    Angles greater than the TIR angle will be reflected; lower angles will
    experience some transmission. If there is no TIR angle, pi/2 is returned,
    the maximum ray-surface angle possible (this makes testing for whether a
    ray exceeds TIR easier).
    """
    if ni < nt:
        return numpy.pi / 2.0
    else:
        return numpy.arcsin(nt / ni)

def brewsters_angle(ni, nt):
    """Returns Brewster's angle for light passing between two media.

    ni: index of refraction in incident media
    nt: index of refraction in transmitting media
    """
    #https://en.wikipedia.org/wiki/Brewster%27s_angle
    return numpy.arctan(nt / float(ni))

def fresnel_amplitude_coefs(ni, theta_i, nt):
    """Computes Fresnel reflection and transmission amplitude coefficients.

    Note that these give the amplitude of the wave for the s- and p-polarized
    waves.
    """
    theta_t = refraction_angle(ni, theta_i, nt)
    ci = numpy.cos(theta_i)
    ct = numpy.cos(theta_t)
    rs = (ni * ci - nt * ct) / (ni * ci + nt * ct)
    ts = 2.0 * ni * ci / (ni * ci + nt * ct)
    rp = (nt * ci - ni * ct) / (ni * ct + nt * ci)
    tp = 2.0 * ni * ci / (ni * ct + nt * ci)
    return rs, rp, ts, tp

def fresnel_coefs(ni, theta_i, nt):
    """Computes Fresnel reflection and transmission intensity coefficients.

    The average reflection coefficient is returned, which assumes unpolarized
    light.
    """
    rs, rp, ts, tp = fresnel_amplitude_coefs(ni, theta_i, nt)
    R_avg = 0.5 * (rs**2 + rp**2)
    T_avg = 1.0 - R_avg
    return R_avg, T_avg
    #TODO: verify that T_avg is related to n2*ct/(ni*ci)*t**2

def slab_fresnel_reflectance(ni, theta_i, n_slab):
    """Total reflection from a slab surface, neglecting interference effects.

    This is the total reflection from all beams bouncing back and forth from
    either side of the slab. It is assumed that the slab has the same index
    on either side, ni.
    """
    R, _ = fresnel_coefs(ni, theta_i, n_slab)
    return 2.0 * R / (1.0 + R)

def schlicks_approximation(ni, theta_i, nt):
    """Returns the reflection coefficient using Schlick's approximation.

    Schlick's is from the computer graphics world. See
    https://en.wikipedia.org/wiki/Schlick%27s_approximation
    for more information.
    """
    R_zero = ((ni - nt) / float(ni + nt))**2
    return R_zero + (1.0 - R_zero) * (1.0 - numpy.cos(theta_i))**5
