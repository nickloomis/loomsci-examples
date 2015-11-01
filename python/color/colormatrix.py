# -*- coding: utf-8 -*-
"""
Module to store matrices for linear transforms between color spaces.

When adding new matrices, use the @propoerty decorator, and name the property
using the format of
  origin2destination_addl_qualifiers
The property method name should be in all lower case.
Please add a note or a link for the source of the values.

Change log:
  2015/10/09 -- module started; xyz2lms matrices added; nloomis@gmail.com
  2015/10/10 -- added adapt_whitepoint; nloomis@
  2015/10/11 -- one2one transform added for use in testing; nloomis@
"""

import numpy

class ColorMatrix(object):

    def __init__(self):
        self._forward_transform_names = self._forward_transforms()
        self._inverse_transform_names = self._inverse_transforms()
        self.transforms = self._forward_transform_names + \
                          self._inverse_transform_names

    def _forward_transforms(self):
        """Generates a list of forward transforms in this class.

        NB: the property decorator is used to denote the forward transforms."""
        #code for this function from
        #stackoverflow.com/questions/5876049/
        #in-a-python-object-how-can-i-see-a-list-of-properties-that-have-been-
        #defined-wi
        class_items = self.__class__.__dict__.iteritems()
        return list(k for k, v in class_items if isinstance(v, property))

    def _inverse_transforms(self):
        """Generate a list of inverse transforms in this class.

        The list of inverse transforms is generated from the list of forward
        transforms, since all transforms are linear matrices."""
        return map(self._invert_transform_name, self._forward_transforms())

    def _invert_transform_name(self, fwd_name):
        """Returns the name of the inverse transform for the forward transform.

        NB: transforms are exptected to follow the format of
          src2dst_addl_qualifiers
        The '2' and '_' characters are used specifically to split the name.
        """
        tform_qual = fwd_name.split('_', 1)
        src, dst = tform_qual[0].split('2', 1)
        inv_tform = '2'.join((dst, src))
        if len(tform_qual) == 1:
            return inv_tform
        else:
            return '_'.join((inv_tform, tform_qual[1]))

    def matrix(self, transform_name):
        """Returns the color transform matrix requested.

        The transform_name is a string, and can be any matrix stored in the
        class. The ColorMatrix.transforms list has all available transforms.
        The matrix() function serves as a common accessor method for all
        available transforms, not just the forward transforms. (Note that the
        forward transforms can be accessed using ColorMatrix.fwd_tform in a
        direct way if desired.)
        """
        #note: for now, the transform_name needs to exactly match one of the
        #transforms. [later, i might change this so that the direction and
        #qualifiers can be named in a more flexible way, like
        #matrix('xy2lms', 'von kries D65'). that's why the method names need
        #to be lower case and qualifiers sep'd by understores.]
        if transform_name in self._forward_transform_names:
            return getattr(self, transform_name)
        elif transform_name in self._inverse_transform_names:
            fwd_name = self._invert_transform_name(transform_name)
            return numpy.linalg.inv(getattr(self, fwd_name))
        else:
            raise KeyError('%s is not a known transform.' % transform_name)


    def adapt_whitepoint(self, source_wp, dest_wp):
        """Returns the XYZ(source_wp) -> XYZ(dest_wp) conversion matrix.

        The source and destination whitepoints are whitepoint.WhitePoint
        objects, and should have the same scale.
        """
        vonkries = numpy.diag(dest_wp.XYZ / source_wp.XYZ)
        return numpy.dot(self.matrix('lms2xyz'),
                         numpy.dot(vonkries, self.matrix('xyz2lms')))
                         #TODO: utility to multiply matrices, this is silly.


    #
    # color transform matrices
    #

    @property
    def one2one(self):
        """Unitary matrix which doesn't change the color.

        The one2one mapping is for testing purposes, since the color should
        not be affected."""
        return numpy.eye(3)

    @property
    def xyz2lms(self):
        """Default XYZ->LMS transform (Bradford)."""
        return self.xyz2lms_bradford

    @property
    def xyz2lms_von_kries(self):
        """Original von Kries transform using an equal-energy illuminant (E)."""
        #data from wikipedia: LMS color space
        return numpy.array([[0.38971, 0.68898, -0.07868],
                            [-0.22981, 1.18340, 0.04641],
                            [0.0, 0.0, 1.0]])

    @property
    def xyz2lms_von_kries_d65(self):
        """von Kries transform, normalized to D65."""
        #data from wikipedia: LMS color space
        return numpy.array([[0.4002, 0.7076, -0.0808],
                            [-0.2263, 1.1653, 0.0457],
                            [0.0, 0.0, 0.9182]])

    @property
    def xyz2lms_bradford(self):
        """Bradford transform matrix for XYZ->LMS."""
        #data from wikipedia: LMS color space; also available from Bruce Lindbloom.
        return numpy.array([[0.8951, 0.2664, -0.1614],
                            [-0.7502, 1.7135, 0.0367],
                            [0.0389, -0.0685, 1.0296]])

    @property
    def xyz2lms_ciecam97s(self):
        """CIECAM97s color appearance model for XYZ->LMS."""
        #data from wikipedia: LMS color space
        return numpy.array([[0.8562, 0.3372, -0.1934],
                            [-0.8360, 1.8327, 0.0033],
                            [0.0357, -0.0469, 1.0112]])

    @property
    def xyz2lms_ciecam02(self):
        """CIECAM02 color appearance model transform for XYZ->LMS."""
        #data from wikipedia: LMS color space
        return numpy.array([[0.7328, 0.4296, -0.1624],
                            [-0.7036, 1.6975, 0.0061],
                            [0.0030, 0.0136, 0.9834]])

    @property
    def srgb2xyz(self):
        """Linear sRGB to XYZ default transform."""
        return self.srgb2xyz_d50

    @property
    def srgb2xyz_d50(self):
        """Linear sRGB to XYZ, adapted to D50 using Bradford."""
        #source: Bruce Lindbloom
        return numpy.array([[0.4360747, 0.3850649, 0.1430804],
                            [0.2225045, 0.7168786, 0.0606169],
                            [0.0139322, 0.0971045, 0.7141733]])

    @property
    def srgb2xyz_d65(self):
        """Linear sRGB to XYZ, adapted to D65."""
        #source: Bruce Lindbloom
        return numpy.array([[0.4124564, 0.3575761, 0.1804375],
                            [0.2126729, 0.7151522, 0.0721750],
                            [0.0193339, 0.1191920, 0.9503041]])
