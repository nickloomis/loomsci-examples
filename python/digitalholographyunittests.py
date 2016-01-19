# -*- coding: utf-8 -*-
"""
Unit tests for digitalholography.py.

Change log:
  2015/10/31: unit tests started; nloomis@gmail.com
  2016/01/18: fixed error in test_du_dv where the wrong variable was checked;
              small formatting changes; nloomis@
"""
__authors__ = ('nloomis@gmail.com',)

import digitalholography as dhi
import imageutils

import numpy
import os.path
import unittest

class HologramTest(unittest.TestCase):
    """Tests for Hologram() objects which don't require data to be loaded."""
    holo = dhi.Hologram()

    def test_init(self):
        self.assertIsNotNone(self.holo)
        self.assertIsNone(self.holo.data)
        self.assertIsNone(self.holo.field)
        self.assertIsNone(self.holo.fft)
        
    def test_wavelength(self):
        #wavelength set to default.
        self.assertEqual(500e-6, self.holo.wavelength)
    
    def test_pixel_size(self):
        #pixel_size set to default:
        self.assertEqual(10e-3, self.holo.pixel_size)
        
    def test_dx_dy(self):
        self.assertEqual(10e-3, self.holo.dx)
        self.assertEqual(10e-3, self.holo.dy)
        
    def test_du_dv(self):
        self.assertEqual(50., self.holo.u_max)
        self.assertEqual(50., self.holo.v_max)


class HologramTestLoad(unittest.TestCase):
    """Tests for Hologram() objects which use loaded-in data."""

    data_path = os.path.join(imageutils.image_dir(), 'godzillaholo.bmp')

    def setUp(self):
        self.holo = dhi.Hologram()
        self.holo.load(self.data_path)
    
    def test_load(self):
        self.assertIsNotNone(self.holo.data)
        self.assertIsInstance(self.holo.data, numpy.ndarray)
        self.assertIsNone(self.holo.fft)
        self.assertIsNone(self.holo.z)
        
    def test_nx_ny(self):
        self.assertEqual(1024, self.holo.nx)
        self.assertEqual(1024, self.holo.ny)

if __name__ == '__main__':
    unittest.main()