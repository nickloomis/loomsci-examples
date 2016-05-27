"""
Module to work with digital holography.

Change log:
  2015/10/24 -- module started; nloomis@gmail.com
  2016/01/18 -- minor formatting fixes; nloomis@gmail.com
  2016/05/25 -- documentation work; nloomis@gmail.com
"""
__authors__ = ("nloomis@gmail.com",)

import cv2utils
import cv2color
import imageutils

import numpy
import matplotlib.pyplot as plt


class Hologram(object):
    def __init__(self, wavelength=0.500e-3, pixel_size=0.010):
        # Values related to the physics.
        # _data holds the raw hologram data, if it has been loaded.
        self._data = None
        self.wavelength = wavelength
        self._pixel_size = pixel_size

        # Internal state.
        # nx, ny are the number of samples in the x and y directions.
        self._nx = None
        self._ny = None
        # fft holds the fast Fourier transform of the source _data.
        self.fft = None
        # _freq_R2 = U^2 + V^2, a variable which is used repeatedly when
        # calculating a diffraction kernel.
        self._freq_R2 = None

        # Reset all variables related to reconstruction
        self._reset_reconstruction()

    def _reset_reconstruction(self):
        """Resets reconstruction variables."""
        # field is the reconstructed optical field.
        self.field = None
        self._set_z(None)

    def load(self, data):
        """Loads data into a Hologram object.

        The data can either be a numpy array already in memory or a filename
        to read from disk using opencv.

        If the data is a numpy array, it is assumed to be floating point and
        single channel.

        If the data is a string, it is treated as a file on disk. The file is
        read into an array, converted to grayscale if it is 3-channel, and 
        divided by 255 to convert to floating point."""
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
        """Returns the source data as a floating-point numpy array."""
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self._set_nx_ny_from_data()
        self.fft = None #reset the fft information
        self._reset_reconstruction()

    def _set_nx_ny_from_data(self):
        """Sets the sample counts using shape information in the data array."""
        if not self._data is None:
            self.ny = self.data.shape[0]
            self.nx = self.data.shape[1]

    @property
    def pixel_size(self):
        """Returns the physical size of a pixel."""
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
        """Returns the wavenumber.

        The wavenumber is defined as

          k = 2 * pi / wavelength,

        and is in units of inverse length."""
        return 2.0 * numpy.pi / self.wavelength

    @property
    def z(self):
        """Returns the last reconstruction distance."""
        return self._z

    def _set_z(self, z_dist):
        """Sets the internally-stored value for the reconstruction distance."""
        self._z = z_dist

    def reconstruct(self, z):
        """Reconstruct the optical field at a specific propagation distance.

        The field is returned after the computation completes. The field is also
        accessible from Hologram.field.

        The field is, in general, a complex-valued array."""
        if self.data is None:
            raise ValueError("No data to reconstruct.")
        if self.fft is None:
            self.fft = numpy.fft.fft2(self.data)
        
        self.holokern(z)
        self.field = numpy.fft.ifft2(self.fft * self.kernel)
        self._set_z(z)
        return self.field

    def _make_frequency_grids(self):
        """Constructs u and v grids in the Fourier domain.

        u is the x-direction spatial frequency, while v is the y-direction
        spatial frequency."""
        u = numpy.fft.fftfreq(self.nx, self.pixel_size)
        v = numpy.fft.fftfreq(self.ny, self.pixel_size)
        self._freq_U, self._freq_V = numpy.meshgrid(u, v)
        self._freq_R2 = self._freq_U ** 2.0 + self._freq_V ** 2.0

    def holokern(self, z):
        """Construct the propagation kernel for a specific depth.

        The kernel is stored to Hologram.kernel."""
        if self._freq_R2 is None:
            self._make_frequency_grids()
        a = numpy.pi * self.wavelength * z
        self.kernel = numpy.exp(1j * a * self._freq_R2)
        #TODO: check speed of cos, sin, exp(i) methods

    def holokern_cs(self, z):
        """Construct the propagation kernel; alternate cosine+sine version.

        The kernel is stored to Hologram.kernel. The only difference between
        holokern() and holokern_cs() is that this version uses the Euler
        identity to avoid a complex exponential. It is intended primarily for
        comparing the speed of the two implementations."""
        if self._freq_R2 is None:
            self._make_frequency_grids()
        R2 = self._freq_R2 * numpy.pi * self.wavelength * z
        self.kernel = numpy.cos(R2) + 1j * numpy.sin(R2)

    def plot_intensity(self):
        """Plots the intensity of a reconstructed field.

        The field, F, is complex-valued. Its intensity, I,  is 

          I = F * conj(F)
            = abs(F) ^2 

        This is a convenience function to compute the intensity and display
        the field graphically. Use plt.show() to display the plot window."""
        if not self._is_ready_to_show():
            return
        plt.imshow(numpy.abs(self.field)**2.0)
        plt.title('Intensity; z = %f' % self._z)

    def plot_field(self):
        """Plots reconstructed field components in different subplots.

        plot_field() is a low-level function which plots field components in
        different subplots. The titles, colormapping, or plots themselves can
        be modified before displaying the plots.

        The subplots are arranged as:

        +--------------------+---------------------+
        |                    |                     |
        |     intensity      |         angle       |
        |     (2, 2, 1)      |       (2, 2, 2)     |
        |                    |                     |
        |--------------------+---------------------+
        |                    |                     |
        |     real part      |     imaginary part  |
        |     (2, 2, 3)      |       (2, 2, 4)     |
        |                    |                     |
        +--------------------+---------------------+
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
            _ = self.reconstruct(z)
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

    def aliasing_pixel(self, z):
        """Pixel where aliasing of a kernel occurs.

        The kernel is a chirp function with linearly increasing frequency. At
        some point, the frequency of the kernel surpasses the Nyquist
        frequency of the discretely-sampled hologram. This function returns
        the pixel at which the kernel meets the Nyquist frequency.

        The data should be filtered to only include values below the aliasing
        frequency if aliasing is to be avoided entirely.

        Generalized sampling decribes the additional high-frequency data which
        can be derived from non-filtered, aliased reconstructions (where the
        aliasing is actually used in conjunction with sample aliasing to 
        recover high frequencies).

        The returned value is the floating-point sample where aliasing occurs,
        taking the zero-frequency pixel to be pixel[0, 0] in the Fourier
        domain. Round or floor the value to get the integer pixel to use as a
        Nyquist cut-off, or use the value as a float to construct a mask."""
        df = 1. / (self.nx * self.pixel_size)
        return 1. / (2 * self.wavelength * z * df ** 2)
