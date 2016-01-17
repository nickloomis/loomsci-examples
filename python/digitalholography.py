"""
Module to work with digital holography.

CHange log:
  2015/10/24 -- module started; nloomis@gmail.com
"""
__authors__ = {"nloomis@gmail.com"}

#props
#wavelength, pixel size
#total field of view, max freq, delta-freq, nyquist limit

import numpy
import matplotlib.pyplot as plt

import cv2utils
import cv2color
import imageutils

class Hologram(object):
    def __init__(self, wavelength=0.500e-3, pixel_size=0.010):
        #data about the physics
        self._data = None
        self.wavelength = wavelength
        self._pixel_size = pixel_size

        #internal data
        self._nx = None
        self._ny = None
        self.fft = None #fft of the source data
        self._freq_R2 = None #U^2 + V^2, freq domain grid
        self._reset_reconstruction()

    def _reset_reconstruction(self):
        """Resets reconstruction variables."""
        self.field = None
        self._set_z(None)

    def load(self, data):
        """Loads data into the hologram object -- an array or file."""
        if isinstance(data, basestring):
            img = cv2utils.imread(data)
            if imageutils.nchannels(img) == 3:
                print "Converting 3-channel image to grayscale..."
                img = cv2color.bgr2gray(img)
            self.data = img / 255. #converts to float, [0..1] range
        elif isinstance(data, numpy.ndarray):
            self.data = data
        else:
            raise TypeError("Must be a numpy array or a filename.")

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self._set_nx_ny_from_data()
        self.fft = None #reset the fft information
        self._reset_reconstruction()

    def _set_nx_ny_from_data(self):
        """Sets the sample counts using shape information in the data array."""
        if not self._data:
            self.ny = self.data.shape[0]
            self.nx = self.data.shape[1]

    @property
    def pixel_size(self):
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, pixel_size):
        if self._pixel_size != pixel_size:
            self._freq_R2 = None
        self._pixel_size = pixel_size

    @property
    def ny(self):
        """Returns the number of samples in the y-direction."""
        return self._ny

    @ny.setter
    def ny(self, ny):
        if self._ny != ny:
            self._freq_R2 = None
        self._ny = ny

    @property
    def nx(self):
        """Returns the number of samples in the x-direction."""
        return self._nx

    @nx.setter
    def nx(self, nx):
        if self._nx != nx:
            self._freq_R2 = None
        self._nx = nx

    @property
    def dx(self):
        """Returns the physical step size in the x-direction."""
        return self.pixel_size

    @property
    def dy(self):
        """Returns the physical step size in the y-direction."""
        return self.pixel_size

    @property
    def u_max(self):
        """Returns the maximum frequency in the x-direction."""
        return 1. / (2. * self.dx)

    @property
    def v_max(self):
        """Returns the maximum frequency in the y-direction."""
        return 1. / (2. * self.dy)

    @property
    def du(self):
        """Returns the frequency increment in the x-direction."""
        if self.nx:
            return self.u_max / (0.5 * self.nx)
            #TODO: check the logic!
        else:
            return None

    @property
    def dv(self):
        """Returns the frequency increment in the y-direction."""
        if self.ny:
            return self.v_max / (0.5 * self.ny)
            #TODO: check the logic!
        else:
            return None

    @property
    def k(self):
        """Returns the wavenumber."""
        return 2.0 * numpy.pi / self.wavelength

    @property
    def z(self):
        """Returns the last reconstruction distance."""
        return self._z

    def _set_z(self, z_dist):
        """Sets the internally-stored value for the reconstruction distance."""
        self._z = z_dist

    def reconstruct(self, z):
        """Reconstruct the field at a specific propagation distance."""
        if self.data is None:
            raise ValueError("No data to reconstruct.")
        if self.fft is None:
            self.fft = numpy.fft.fft2(self.data)
        
        self.holokern(z)
        self.field = numpy.fft.ifft2(self.fft * self.kernel)
        self._set_z(z)

    def _make_frequency_grids(self):
        """Constructs u and v grids in the Fourier domain."""
        u = numpy.fft.fftfreq(self.nx, self.pixel_size)
        v = numpy.fft.fftfreq(self.ny, self.pixel_size)
        self._freq_U, self._freq_V = numpy.meshgrid(u, v)
        self._freq_R2 = self._freq_U ** 2.0 + self._freq_V ** 2.0

    def holokern(self, z):
        """Construct the propagation kernel."""
        if self._freq_R2 is None:
            self._make_frequency_grids()
        a = numpy.pi * self.wavelength * z
        self.kernel = numpy.exp(1j * a * self._freq_R2)
        #TODO: check speed of cos, sin, exp(i) methods

    def holokern_cs(self, z):
        """Construct the propagation kernel; alternate cosine+sine version."""
        if self._freq_R2 is None:
            self._make_frequency_grids()
        R2 = self._freq_R2 * numpy.pi * self.wavelength * z
        self.kernel = numpy.cos(R2) + 1j * numpy.sin(R2)

    def plot_intensity(self):
        """Plots the intensity of a reconstructed field; convenience."""
        if not self._is_ready_to_show():
            return
        plt.imshow(numpy.abs(self.field)**2.0)
        plt.title('Intensity; z = %f' % self._z)

    def plot_field(self):
        """Adds the reconstruction field compoents to pyplot subplots.

        plot_field() is the low-level function to add the fields to different
        subplots. This makes it easy to change the titles or colormapping
        before displaying the plots.
        """
        plt.subplot(2, 2, 1)
        self.plot_intensity()
        plt.subplot(2, 2, 2)
        plt.imshow(numpy.angle(self.field))
        plt.title('Angle')
        plt.subplot(2, 2, 3)
        plt.imshow(numpy.real(self.field))
        plt.title('Real')
        plt.subplot(2, 2, 4)
        plt.imshow(numpy.imag(self.field))
        plt.title('Imag')

    def _is_ready_to_show(self, z=None):
        """Returns a bool for whether a field is ready to show.
        
        If a z-distance is supplied, a reconstruction at that distance is
        attempted just before checking for the field's existence.
        """
        if z is not None:
            self.reconstruct(z)
        if self.field is None:
            print "No field has been reconstructed."
            return False
        else:
            return True

    def show_field(self, z=None):
        """Display the reconstructed field.

        Plots the components of a reconstructed field in different subplots
        of a figure window, then displays the results. show_field() includes
        checks for valid data.
        If an optional z-distance is supplied, the field is first reconstructed
        at that distance first, then the field is displayed.
        """
        if not self._is_ready_to_show(z):
            return
        self.plot_field()
        plt.show()

    def show_intensity(self, z=None):
        """Display the intensity of the reconstructed field."""
        if not self._is_ready_to_show(z):
            return
        self.plot_intensity()
        plt.show()