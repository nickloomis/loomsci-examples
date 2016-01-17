# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 22:02:55 2015

@author: nloomis
"""

import numpy
import unittest
import geometricoptics as geo
import raytracing
import raytracinggeometry as raygeo

class TestGeometricOptics(unittest.TestCase):
    """Test cases for geometric optics codes."""

    def test_refraction_angle(self):
        self.assertEqual(geo.refraction_angle(1.5, 0, 1.0), 0.0)
        self.assertAlmostEqual(geo.refraction_angle(1.5, 0.1, 1.0), 0.1503155,
                               places=6)
        self.assertTrue(numpy.isnan(geo.refraction_angle(1.5, 0.73, 1.0)))

    def test_tir_angle(self):
        self.assertAlmostEqual(geo.tir_angle(1.0, 1.0), 1.570796, places=6)
        self.assertAlmostEqual(geo.tir_angle(1.0, 1.1), 1.570796, places=6)
        self.assertAlmostEqual(geo.tir_angle(1.5, 1.0), 0.7297276, places=6)

    def test_brewsters_angle(self):
        self.assertAlmostEqual(geo.brewsters_angle(1.5, 1.0), 0.5880026,
                               places=6)

    def test_fresnel_amplitude_coefs(self):
        #TODO
        pass

    def test_fresnel_coefs(self):
        self.assertEqual(geo.fresnel_coefs(1.0, 0, 1.0), (0.0, 1.0))
        R,T = geo.fresnel_coefs(1.6, 0.5, 1.0)
        self.assertAlmostEqual(R, 0.072538667, places=6)
        self.assertAlmostEqual(T, 0.927461332, places=6)

        #angles which exceed TIR should return nans:
        tir_angle = geo.tir_angle(1.6, 1.0)
        self.assertTrue(all(numpy.isnan(geo.fresnel_coefs(1.6,
                                                          tir_angle + 0.01,
                                                          1.0))))

    def test_slab_fresnel_reflectance(self):
        #TODO
    #include a check that this is greater than the fresnel reflection coef, and
    #check for correct values

        #if TIR is exceeded, should return a nan:
        tir_angle = geo.tir_angle(1.6, 1.0)
        self.assertTrue(numpy.isnan(
          geo.slab_fresnel_reflectance(1.6, tir_angle + 0.01, 1.0)))

    def test_schlicks_approximation(self):
        #TODO
        pass


class TestRayTracingGeometry(unittest.TestCase):
    """Test cases for working with geometric objects in ray tracing."""

    def test_Plane(self):
        #TODO
        pass

    def test_Ellipsoid(self):
        #TODO
        pass

    def test_Sphere(self):
        #TODO
        pass


class TestRayTracing(unittest.TestCase):
    """Tests for ray tracing code."""

    def test_Ray(self):
        #TODO
        pass

    def test_angle_of_incidence(self):
        #TODO
        pass

    def test_reflect_ray(self):
        #TODO
        pass

    def test_refract_ray(self):
        #TODO
        pass

    def test_refract_ray_sphere(self):
        #TODO
        pass

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestGeometricOptics)
    #unittest.TextTestRunner(verbosity=2).run(suite)