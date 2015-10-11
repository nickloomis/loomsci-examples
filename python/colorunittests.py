# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 10:34:43 2015

@author: nloomis
Change log:
  2015/10/09 -- module outlined; nloomis@gmail.com
  2015/10/11 -- colormatrix tests added; nloomis@
"""
import numpy
import unittest

import color

class TestColormatrix(unittest.TestCase):
    cm = color.colormatrix.ColorMatrix()

    def test_init(self):
        self.assertIsNotNone(self.cm._forward_transform_names)
        self.assertTrue(len(self.cm._forward_transform_names) ==
                        len(self.cm._inverse_transform_names))
        self.assertIsNotNone(self.cm.transforms)

    def test_invert_transform_name(self):
        self.assertEqual(self.cm._invert_transform_name('foo2bar'), 'bar2foo')
        self.assertEqual(self.cm._invert_transform_name('foo2bar_qual'),
                         'bar2foo_qual')
        self.assertEqual(self.cm._invert_transform_name('foo2bar_multi_qual'),
                         'bar2foo_multi_qual')

    def test_matrix(self):
        known_transform = 'xyz2lms'
        known_inverse = self.cm._invert_transform_name(known_transform)
        with self.assertRaises(KeyError):
            self.cm.matrix('foo2bar_unknown_transform')
        self.assertIsNotNone(self.cm.matrix(known_transform))
        self.assertIsInstance(self.cm.matrix(known_transform), numpy.ndarray)
        self.assertIsInstance(self.cm.matrix(known_inverse), numpy.ndarray)
        self.assertTrue((self.cm.matrix('one2one') == numpy.eye(3)).all())
        self.assertTrue(numpy.allclose(
                        numpy.dot(self.cm.matrix(known_transform),
                                  self.cm.matrix(known_inverse)),
                        numpy.eye(3)))

    def test_adapt_whitepoint(self):
        d50 = color.whitepoint.D50
        self.assertTrue(numpy.allclose(self.cm.adapt_whitepoint(d50, d50),
                                       numpy.eye(3)))

class TestColortransform(unittest.TestCase):
    ct = color.colortransform
    img = numpy.reshape(range(258), (1,86,3)).clip(0,255).astype('uint8')
    cimg = numpy.reshape(numpy.linspace(0, 257, 258) / 256.,
                         (1,86,3)).clip(0.0, 1.0)
    not_numpy_type = 42
    ones13 = numpy.ones((1,3)).flatten()
    ones12 = numpy.ones((1,2)).flatten()
    ones112 = numpy.reshape(ones12, (1, 1, 2))
    ones113 = numpy.reshape(ones13, (1, 1, 3))

    def test_safe_divide(self):
        with self.assertRaises(AssertionError):
            #inputs must have same shape
            self.ct._safe_divide(self.ones12, self.ones13)
        #should return numpy arrays:
        self.assertIsInstance(self.ct._safe_divide(1, 1), numpy.ndarray)
        #check for correct operation:
        num = numpy.array([1, 1, 1])
        denom = numpy.array([0, 0.0, 1])
        self.assertTrue(numpy.allclose(self.ct._safe_divide(num, denom),
                                       numpy.array([0, 0, 1])))
        self.assertTrue(numpy.allclose(
              self.ct._safe_divide(num, denom, replace=42),
              numpy.array([42, 42, 1])))
        #also useful but not tested here: the dtype should stay the same. ie,
        #you can use safe_divide with both ints or both floats and get back the
        #same dtype.

    def test_to_npa(self):
        #numpy arrays don't change:
        self.assertTrue(numpy.allclose(self.ct._to_npa(self.ones12),
                                       self.ones12))
        #lists and tuples are converted to numpy arrays:
        self.assertTrue(numpy.allclose(self.ct._to_npa([1]),
                                       numpy.array([1])))
        self.assertTrue(numpy.allclose(self.ct._to_npa((1,)),
                                       numpy.array([1])))
        #scalars are converted to numpy arrays:
        self.assertTrue(numpy.allclose(self.ct._to_npa(1),
                                       numpy.array([1])))
        #unknown input type:
        with self.assertRaises(TypeError):
            self.ct._to_npa("foobar")

    def test_bilevel_func(self):
        #check that a conversion to a numpy type is tried on input:x
        with self.assertRaises(TypeError):
            self.ct._bilevel_func('not numpy-convertible', None, None, None)
        #check that a conversion to a numpy type is tried on input:threshold
        with self.assertRaises(TypeError):
            self.ct._bilevel_func(0, None, None, None, 'not numpy-convertible')
        x = numpy.array([0, 1, 2, 3, 4])
        f_a = lambda a: a
        f_b = lambda b: -1
        #check that simple thresholding works
        test_1 = self.ct._bilevel_func(x, f_a, f_b, 2)
        self.assertTrue(numpy.allclose(test_1, 
                                       numpy.array([-1, -1, -1, 3, 4])))
        #more simple thresholding
        test_2 = self.ct._bilevel_func(x, f_a, f_b, 2.5)
        self.assertTrue(numpy.allclose(test_2,
                                       numpy.array([-1, -1, -1, 3, 4])))
        #check that an alternate threshold variable can be used correctly
        alt_thresh_var = numpy.array([5, 6, 0, 0, 0])
        test_3 = self.ct._bilevel_func(x, f_a, f_b, 2, alt_thresh_var)
        self.assertTrue(numpy.allclose(test_3,
                                       numpy.array([0, 1, -1, -1, -1])))
        test_4 = self.ct._bilevel_func(x, f_a, f_b, 5.5, alt_thresh_var)
        self.assertTrue(numpy.allclose(test_4,
                                       numpy.array([-1, 1, -1, -1, -1])))
 
    def test_compand(self):
        with self.assertRaises(AssertionError):
            self.ct.compand(self.not_numpy_type)
        rgb = self.ct.compand(self.ones13)
        self.assertEqual(self.ones13.shape, rgb.shape)
        self.assertTrue(numpy.allclose(numpy.array([255, 255, 255]),
                                       rgb))
        zero10 = numpy.zeros((10,1))
        rgb_zero = self.ct.compand(zero10)
        self.assertEqual(zero10.shape, rgb_zero.shape)
        self.assertTrue(numpy.allclose(zero10, rgb_zero))
        gray_lin = numpy.array([.25, .5, .75])
        gray_nl_correct = numpy.array([137, 188, 225])
        gray_nl = self.ct.compand(gray_lin)
        self.assertTrue(numpy.allclose(gray_nl_correct, gray_nl))

    def test_inverse_compand(self):
        with self.assertRaises(AssertionError):
            self.ct.inverse_compand(self.not_numpy_type)
        self.ct.inverse_compand(self.img)
        #wrong dtype should throw an error
        with self.assertRaises(AssertionError):
            self.ct.inverse_compand(self.cimg)
        #check values, sizes:
        zeros = numpy.zeros((10,1), dtype='uint8')
        gray_nl = numpy.array([0, 1, 50, 100, 200, 255], dtype='uint8')
        zero_lin = self.ct.inverse_compand(zeros)
        self.assertEqual(zeros.shape, zero_lin.shape)
        self.assertTrue(numpy.allclose(zeros, zero_lin))
        gray_lin = self.ct.inverse_compand(gray_nl)
        gray_lin_correct = numpy.array([0.0, 3.03526984e-4, 3.1896033e-2,
                                        1.2743768e-1, 5.775804e-1, 1.])
        self.assertTrue(numpy.allclose(gray_lin_correct, gray_lin))

    def test_companding(self):
        ic_img = self.ct.inverse_compand(self.img)
        inv_img = self.ct.compand(ic_img)
        self.assertTrue(numpy.allclose(self.img, inv_img))

    def test_xyz2xy(self):
        with self.assertRaises(AssertionError):
            self.ct.xyz2xy(self.not_numpy_type)
        with self.assertRaises(AssertionError):
            #wrong length of input arg -- needs three values
            self.ct.xyz2xy(self.ones12)
        xy = self.ct.xyz2xy(self.ones13)
        self.assertEqual(len(xy), 2)
        self.assertTrue(numpy.allclose(xy,
                                       numpy.ones((1, 2)) / 3.0))

    def test_xy2xyz(self):
        with self.assertRaises(AssertionError):
            self.ct.xy2xyz(self.not_numpy_type)
        xyz = self.ct.xy2xyz(self.ones12 / 3.0)
        self.assertEqual(len(xyz), 3)
        self.assertTrue(numpy.allclose(xyz, self.ones13))

    def test_xyz2xyy(self):
        with self.assertRaises(AssertionError):
            self.ct.xyz2xyy(self.not_numpy_type)
        with self.assertRaises(AssertionError):
            #wrong data length
            self.ct.xyz2xyy(self.ones12)
        xyy = self.ct.xyz2xyy(self.ones13)
        self.assertEqual(len(xyy), 3)
        self.assertTrue(numpy.allclose(xyy, numpy.array([1/3., 1/3., 1.])))

    def test_xyy2xyz(self):
        with self.assertRaises(AssertionError):
            self.ct.xyy2xyz(self.not_numpy_type)
        with self.assertRaises(AssertionError):
            #wrong data length
            self.ct.xyy2xyz(self.ones12)
        xyz = self.ct.xyy2xyz(numpy.array([1/3., 1/3., 1.]))
        self.assertEqual(len(xyz), 3)
        self.assertTrue(numpy.allclose(xyz, self.ones13))

    def test_xyz2lab(self):
        with self.assertRaises(AssertionError):
            self.ct.xyz2lab(self.not_numpy_type)
        with self.assertRaises(AssertionError):
            #not a 3-channel image; should actually fail in imageutils.split3
            self.ct.xyz2lab(self.ones112)
        lab_D50 = self.ct.xyz2lab(self.ones113)
        lab_D65 = self.ct.xyz2lab(self.ones113,
                                  white_ref=self.ct.whitepoint.D65)
        lab_known_D50 = numpy.array([[[100., 6.11105974, -13.22869281]]])
        lab_known_D65 = numpy.array([[[100., 8.54592717, 5.59805141]]])
        zeros113 = numpy.zeros((1,1,3))
        self.assertTrue(numpy.allclose(lab_D50, lab_known_D50, atol=1e-5))
        self.assertTrue(numpy.allclose(lab_D65, lab_known_D65, atol=1e-5))
        self.assertTrue(numpy.allclose(self.ct.xyz2lab(zeros113),
                                       zeros113))
        self.assertTrue(lab_known_D50.shape == self.ones113.shape)

    def test_lab2xyz(self):
        with self.assertRaises(AssertionError):
            self.ct.lab2xyz(self.not_numpy_type)
        with self.assertRaises(AssertionError):
            #not a 3-channel image
            self.ct.lab2xyz(self.ones112)
        #these both evaluate to ones113 with the correct white reference
        lab_known_D50 = numpy.array([[[100., 6.11105974, -13.22869281]]])
        lab_known_D65 = numpy.array([[[100., 8.54592717, 5.59805141]]])
        zeros113 = numpy.zeros((1,1,3))
        xyz_D50 = self.ct.lab2xyz(lab_known_D50)
        xyz_D65 = self.ct.lab2xyz(lab_known_D65,
                                  white_ref=self.ct.whitepoint.D65)
        self.assertTrue(numpy.allclose(xyz_D50, self.ones113))
        self.assertTrue(numpy.allclose(xyz_D65, self.ones113))
        self.assertTrue(numpy.allclose(self.ct.lab2xyz(zeros113),
                                       zeros113))
        self.assertTrue(lab_known_D50.shape == self.ones113.shape)

    def test_xyz2lab2xyz(self):
        #check the conversion to lab then back to xyz gives the same values
        lab = self.ct.xyz2lab(self.cimg)
        xyz = self.ct.lab2xyz(lab)
        self.assertTrue(numpy.allclose(self.cimg, xyz))

    def test_uprime(self):
        self.assertEqual(self.ct._uprime(1.0, 1.0, 1.0)[0],
                         4.0 / (1.0 + 15.0 + 3.0))
        self.assertEqual(self.ct._uprime(0.0, 0.0, 0.0)[0], 0.0)
        zero_np = numpy.array([0])
        self.assertEqual(self.ct._uprime(zero_np, zero_np, zero_np)[0], 0.0)

    def test_vprime(self):
        self.assertEqual(self.ct._vprime(1.0, 1.0, 1.0)[0],
                         9.0 / (1.0 + 15.0 + 3.0))
        self.assertEqual(self.ct._vprime(0.0, 0.0, 0.0)[0], 0.0)
        zero_np = numpy.array([0])
        self.assertEqual(self.ct._vprime(zero_np, zero_np, zero_np)[0], 0.0)

    def test_xyz2luv(self):
        with self.assertRaises(AssertionError):
            self.ct.xyz2luv(self.not_numpy_type)
        luv = self.ct.xyz2luv(self.ones113)
        self.assertIsInstance(luv, numpy.ndarray)
        self.assertTrue(numpy.allclose(luv, 
              numpy.array([[[100., 1.7773207, -18.70844332]]])))
        zero113 = numpy.zeros((1,1,3))
        luv_zero = self.ct.xyz2luv(zero113)
        self.assertTrue(numpy.allclose(luv_zero, zero113))

    def test_luv2xyz(self):
        with self.assertRaises(AssertionError):
            self.ct.luv2xyz(self.not_numpy_type)
        luv100 = numpy.array([[[100., 0., 0.]]])
        xyz = self.ct.luv2xyz(luv100)
        self.assertIsInstance(xyz, numpy.ndarray)
        self.assertTrue(numpy.allclose(xyz, 
              numpy.array([0.96421199, 1., 0.82518828])))
        zero113 = numpy.zeros((1,1,3))
        xyz_zero = self.ct.luv2xyz(zero113)
        self.assertTrue(numpy.allclose(xyz_zero, zero113))

    def test_xyz2luv2xyz(self):
        #check that conversions are repeatable in both directions
        luv = self.ct.xyz2luv(self.cimg)
        xyz = self.ct.luv2xyz(luv)
        self.assertTrue(numpy.allclose(xyz, self.cimg))

    def test_luv2lch(self):
        with self.assertRaises(AssertionError):
            self.ct.luv2lch(self.not_numpy_type)
        luv100 = numpy.array([[[100., 0., 0.]]])
        lch100 = self.ct.luv2lch(luv100)
        self.assertIsInstance(lch100, numpy.ndarray)
        #check that, if no chroma, the input matches the output:
        self.assertTrue(numpy.allclose(lch100, luv100))
        #check a known chroma-hue combination
        u = 1.1010101
        v = 2.42
        lch = self.ct.luv2lch(numpy.array([[[100, u, v]]]))
        self.assertTrue(numpy.allclose(lch, 
              numpy.array([[[100, 
                             numpy.sqrt(u**2 + v**2), 
                             numpy.arctan2(v, u)]]])))

    def test_uv2xy(self):
        with self.assertRaises(AssertionError):
            self.ct.uv2xy(self.ones13)
        xy = self.ct.uv2xy(self.ones12)
        self.assertEqual(2, len(xy))
        self.assertIsInstance(xy, numpy.ndarray)
        self.assertTrue(numpy.allclose(xy, numpy.array([4.5, 2.0])))

    def test_xy2uv(self):
        with self.assertRaises(AssertionError):
            self.ct.xy2uv(self.ones13)
        uv = self.ct.xy2uv(self.ones12)
        self.assertEqual(2, len(uv))
        self.assertIsInstance(uv, numpy.ndarray)
        self.assertTrue(numpy.allclose(uv, numpy.array([4/13., 9/13.])))
    
    def test_xy2uv2xy(self):
        uv = self.ct.xy2uv(self.ones12)
        xy = self.ct.uv2xy(uv)
        self.assertTrue(numpy.allclose(xy, self.ones12))


class TestWhitepoint(unittest.TestCase):
    def test_init(self):
        wp = color.whitepoint.WhitePoint(1.0, 1.0, 1.0, 'test')
        self.assertEqual(wp.X, 1.0)
        self.assertEqual(wp.Y, 1.0)
        self.assertEqual(wp.Z, 1.0)
        self.assertEqual(wp.name, 'test')

    def test_whitepoint_XYZ(self):
        wp = color.whitepoint.WhitePoint(1.0, 1.0, 1.0, 'test')
        self.assertEqual(len(wp.XYZ), 3)
        self.assertTrue(numpy.allclose(wp.XYZ,
                                       numpy.ones((1,3))))

    def test_whitepoint_xy(self):
        wp = color.whitepoint.WhitePoint(1.0, 1.0, 1.0, 'test')
        self.assertEqual(len(wp.xy), 2)
        self.assertTrue(numpy.allclose(wp.xy,
                                       numpy.ones((1,2)) / 3.0))

    def test_wp_math(self):
        wp = color.whitepoint.WhitePoint(1.0, 1.0, 1.0, 'test')
        self.assertTrue(numpy.allclose((wp * 2.0).XYZ,
                                       numpy.ones((1, 3)) * 2.0))
        self.assertTrue(numpy.allclose((2.0 * wp).XYZ,
                                       numpy.ones((1, 3)) * 2.0))
        self.assertTrue(numpy.allclose((wp / 2.0).XYZ,
                                       numpy.ones((1,3)) / 2.0))

    def test_illuminant_variables(self):
        expected_illums = ('A', 'B', 'C', 'D50', 'D55', 'D65', 'D75',
                           'E', 'F1', 'F2')
        all_vars = dir(color.whitepoint)
        has_var = [i in all_vars for i in expected_illums]
        self.assertTrue(all(has_var))
        self.assertTrue(numpy.allclose(color.whitepoint.E.XYZ,
                                       numpy.ones((1,3))))

if __name__ == '__main__':
    unittest.main()