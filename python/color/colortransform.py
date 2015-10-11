# -*- coding: utf-8 -*-
"""
Functions for transforming between color spaces.

Change log:
  2015/10/09 -- compand, inverse_compand added; nloomis@gmail.com
"""
import copy
import numpy

import imageutils
import whitepoint

#
# module constants
#
_lab_epsilon = 0.008856
_lab_kappa = 903.3


#
# module utilities
#

def _safe_divide(num, denom, replace=0):
    """Safe division when elements in the denominator might be zeros.

    Returns the division of the numerator by the denominator, but replaces
    results which have a zero in the denominator by a specified value. The
    default is to replace bad divisions with zeros.
    """
    #consider moving to a utility module; copy over tests from colorunittests.py
    num = _to_npa(num)
    denom = _to_npa(denom)
    assert(num.shape == denom.shape)
    zero_flag = denom == 0.0
    if zero_flag.any():
        denom_copy = copy.copy(denom)
        denom_copy[zero_flag] = 1.0
        div = num / denom_copy
        div[zero_flag] = replace
    else:
        div = num / denom
    return div

def _to_npa(value):
    """Converts a scalar or list to a numpy array."""
    #consider moving to a utility module; copy over tests from colorunittests.py
    if isinstance(value, numpy.ndarray):
        return value
    elif isinstance(value, (list, tuple)):
        #note: any /ordered/ iterable should be allowed to work, as long as it
        #is numeric
        #TODO: include checks for other numeric iterables
        return numpy.array(value)
    elif isinstance(value, (int, float)):
        return numpy.array([value])
    else:
        raise TypeError

def _bilevel_func(x, func_a, func_b, threshold, thresh_var=None):
    """Applies two different functions to an input depending on a threshold.

    For inputs larger than the threshold value, func_a is applied; it is
    assumed that func_a is a default. Inputs less than or equal to the
    threshold value are then replaced by func_b's outputs.
    """
    x_npa = _to_npa(x)
    if thresh_var is None:
        thresh_var_npa = x_npa
    else:
        thresh_var_npa = _to_npa(thresh_var)
    #if x is a numpy array, _to_npa returns x instead of a new variable
    #constructed from x. in that case, it is possible that func_a or func_b can
    #modify the input. an x.copy() is used to guard against unexpectedly
    #changing x.
    res = func_a(x_npa.copy())
    small_flag = thresh_var_npa <= threshold
    if small_flag.any():
        res[small_flag] = func_b(x_npa[small_flag])
    return res

#
# transforms!
#

def compand(rgb_linear):
    """Compand from linear RGB to sRGB.

    The input is linear RGB, and ranges from [0..1]. The output is a uint8 sRGB
    image.
    """
    assert(isinstance(rgb_linear, numpy.ndarray))
    f_a = lambda x: 1.055 * x ** (1/2.4) - 0.055
    f_b = lambda x: x * 12.92
    sRGB_double = _bilevel_func(rgb_linear, f_a, f_b, 0.0031308)
    return imageutils.float2uint8(sRGB_double)

def inverse_compand(img):
    """Convert from sRGB to linear RGB by inverting the sRGB companding.

    The input image should be uint8. The output is linear and is in the range
    of [0..1].
    """
    assert(isinstance(img, numpy.ndarray))
    assert(img.dtype == numpy.uint8) #TODO: throw a TypeError instead
    sRGB_double = img / 255. #convert to normalized float
    f_a = lambda x: ((x + 0.055) / 1.055) ** 2.4
    f_b = lambda x: x / 12.92
    return _bilevel_func(sRGB_double, f_a, f_b, 0.0405)

def xyz2xy(vec):
    """Calculate the (x,y) chromaticity coordinates from an XYZ triplet."""
    assert(isinstance(vec, numpy.ndarray))
    assert(len(vec) == 3)
    return vec[0:2] / float(numpy.sum(vec))

def xyz2xyy(vector):
    """Convert from XYZ to xyY.

    Note: xyY is sometimes called xyL."""
    assert(isinstance(vector, numpy.ndarray))
    assert(len(vector) == 3)
    #TODO: be careful about the stacking if vector is vert or horiz
    return numpy.hstack((vector[0:2] / float(numpy.sum(vector)), vector[1]))

def xyy2xyz(vector):
    """Convert from xyY to XYZ.

    Note: xyY is sometimes called xyL."""
    #x = vector[0], y = vector[1], Y = vector[2]
    assert(isinstance(vector, numpy.ndarray))
    assert(len(vector) == 3)
    return numpy.array([vector[0]*vector[2] / vector[1],
                        vector[2],
                        (1.0 - vector[0] - vector[1]) * vector[2] / vector[1]])

def xy2xyz(vector):
    """Convert (x,y) coordinates to an XYZ triplet, assuming Y=1."""
    assert(isinstance(vector, numpy.ndarray))
    assert(len(vector) == 2)
    return xyy2xyz(numpy.hstack((vector, 1)))

def lab_inverse_compand(v):
    """Inverse companding used when converting XYZ to Lab and Luv.

    Note: this is the cube-root companding used to return the f_xyz functions
    that are then used directly to compute L*a*b*. The input is the X, Y, or Z
    value, normalized against the whitepoint used to encode the XYZ colorspace.
    """
    #values from the CIE standard; Bruce Lindbloom notes that these lead to
    #a discontinuity due to truncation
    f_a = lambda x: x ** (1 / 3.)
    f_b = lambda x: (_lab_kappa * x + 16.) / 116.
    return _bilevel_func(v, f_a, f_b, _lab_epsilon)

def xyz2lab(xyz_img, white_ref=whitepoint.D50):
    """Converts from XYZ to CIELAB (aka, L*a*b*).

    The white_ref is the whitepoint of the XYZ color space, and defaults to
    D50. Use any other whitepoint.WhitePoint object as a reference if needed.
    The whitepoint values whould be on the same order as the XYZ values. For
    example, if XYZ ranges from [0..1], the whitepoint should have values close
    to 1.
    """
    #default is D50 whitepoint for XYZ colors; Lab is device independent
    assert(isinstance(xyz_img, numpy.ndarray))

    #compute the XYZ relative to the whitepoint; note that this assumes the
    #whitepoint and the XYZ have the same scale.
    X, Y, Z = imageutils.split3(xyz_img)
    xr = X / white_ref.X
    yr = Y / white_ref.Y
    zr = Z / white_ref.Z
    #note: xr, yr, zr are scaled so that they are close to [0..1] range;
    #it is possible to have values >1, that's not an error.
    fy = lab_inverse_compand(yr)
    L = 116.0 * fy - 16.0
    a = 500.0 * (lab_inverse_compand(xr) - fy)
    b = 200.0 * (fy - lab_inverse_compand(zr))
    return imageutils.cat3(L, a, b)

def _lab_finv(V):
    f_a = lambda f: f ** 3.0
    f_b = lambda f: (116. * f - 16) / _lab_kappa
    threshold = _lab_epsilon ** (1 / 3.)
    return _bilevel_func(V, f_a, f_b, threshold)

def _lab_yinv(L):
    f_a = lambda x: ((x + 16.) / 116.) ** 3.
    f_b = lambda x: x / _lab_kappa
    threshold = _lab_epsilon * _lab_kappa
    return _bilevel_func(L, f_a, f_b, threshold)

def lab2xyz(lab_img, white_ref=whitepoint.D50):
    """Converts CIELAB's L*a*b* to XYZ.

    The white_ref is the whitepoint of the XYZ color space; use any
    whitepoint.WhitePoint object as a reference if needed. The default is D50.
    """
    assert(isinstance(lab_img, numpy.ndarray))
    L, a, b = imageutils.split3(lab_img)
    fy = (L + 16.) / 116.
    fx = a / 500. + fy
    fz = fy - b / 200.
    xr = _lab_finv(fx)
    zr = _lab_finv(fz)
    yr = _lab_yinv(L)
    return imageutils.cat3(xr * white_ref.X,
                           yr * white_ref.Y,
                           zr * white_ref.Z)

def _uprime(X, Y, Z):
    """Calculates the u' value used in XYZ<->Luv."""
    return _safe_divide(4. * X, X + 15. * Y + 3. * Z)

def _vprime(X, Y, Z):
    """Calculates the v' value used in XYZ<->Luv."""
    return _safe_divide(9. * Y, X + 15. * Y + 3. * Z)

def xyz2luv(xyz_img, white_ref=whitepoint.D50):
    """Converts XYZ to CIELUV (aka, L*u*v*).

    A whitepoint reference of D50 is assumed for the XYZ values. Any other
    whitepoint, as a whitepoint.WhitePoint object, can be used -- and should
    have the same scale as the XYZ values.
    """
    assert(isinstance(xyz_img, numpy.ndarray))
    X, Y, Z = imageutils.split3(xyz_img)
    yr = Y / white_ref.Y
    uprime = _uprime(X, Y, Z)
    vprime = _vprime(X, Y, Z)
    uprime_ref = _uprime(*white_ref.XYZ)
    vprime_ref = _vprime(*white_ref.XYZ)
    f_a = lambda y: 116. * y ** (1 / 3.) - 16.
    f_b = lambda y: y * _lab_kappa
    L = _bilevel_func(yr, f_a, f_b, _lab_epsilon)
    u = 13.0 * L * (uprime - uprime_ref)
    v = 13.0 * L * (vprime - vprime_ref)
    return imageutils.cat3(L, u, v)

def luv2xyz(luv_img, white_ref=whitepoint.D50):
    """Converts CIELUV to XYZ.

    The white_ref is the whitepoint of the XYZ colorspace, and defaults to D50.
    Use any other whitepoint.WhitePoint object as needed.
    """
    #equation from wikipedia->CIELUV
    assert(isinstance(luv_img, numpy.ndarray))
    L, u, v = imageutils.split3(luv_img)
    f_a = lambda x: ((x + 16.) / 116.) ** 3.
    f_b = lambda x: x / _lab_kappa
    threshold = _lab_kappa * _lab_epsilon
    Y = white_ref.Y * _bilevel_func(L, f_a, f_b, threshold)
    u_ref = _uprime(*white_ref.XYZ)
    v_ref = _vprime(*white_ref.XYZ)
    uprime = _safe_divide(u, 13. * L) + u_ref
    vprime = _safe_divide(v, 13. * L) + v_ref
    X = Y * _safe_divide(9. * uprime, 4. * vprime)
    Z = Y * _safe_divide(12. - 3. * uprime - 20. * vprime, 4. * vprime)
    return imageutils.cat3(X, Y, Z)

def uv2xy(vector):
    assert(len(vector) == 2)
    u = vector[0]
    v = vector[1]
    denom = 6. * u - 16. * v + 12.
    x = _safe_divide(9. * u, denom)
    y = _safe_divide(4. * v, denom)
    return numpy.array([x, y]).flatten()

def xy2uv(vector):
    assert(len(vector) == 2)
    x = vector[0]
    y = vector[1]
    denom = -2. * x + 12. * y + 3.
    u = _safe_divide(4. * x, denom)
    v = _safe_divide(9. * y, denom)
    return numpy.array([u, v]).flatten()

def luv2lch(luv_img):
    """Converts CIELUV to a LCh representation.

    L: luminance
    C: chroma
    h: hue (in radians)
    """
    assert(isinstance(luv_img, numpy.ndarray))
    L, u, v = imageutils.split3(luv_img)
    C = numpy.sqrt(u**2 + v**2)
    h = numpy.arctan2(v, u)
    return imageutils.cat3(L, C, h)

#TODO: this function isn't strictly related to color transforms; could easily
#move to another module which computes color quantities (aka, "correlates")
def lch_saturation(lch_img):
    """Calculates the saturation correlate for an LCh image."""
    assert(isinstance(lch_img, numpy.ndarray))
    L, C, _ = imageutils.split3(lch_img)
    return C / L


#TODO: add other non-linear transforms
#TODO: add simple method to do linear transforms given an image and a matrix
#TODO: add class that provides metadata tracking for different transforms
