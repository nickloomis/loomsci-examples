This directory contains Python code used for examples on loomsci.wordpress.com.
The codes use the repo's default license unless otherwise noted in the files or
subdirectories themselves.

Some examples may require additional modules to be installed. It is assumed that
the reader has the appropriate skills to locate and install the module for their
particular Python setup. Notes are generally included in the code examples about
where to source the modules. Specifically, notes of the form
  "apt-get install some-package-name"
refer to Ubuntu's package manager and its naming scheme for the packages which
contain the module.

Recurring packages:
import cv2 -- both cv and cv2 are installed as part of opencv, use
  apt-get install opencv

Style Guide
=================
- See PEP0008, https://www.python.org/dev/peps/pep-0008/, for Python formatting
  fundies. While these won't be strictly followed, they're a good reference.

- Use two or four spaces for indenting. Keep the indentation consistent in each
  file.

- Start the module with a description of its contents or use. Include a
  change log directly in the module, with a date and notes about the changes,
  followed by an email or signature.

   Example:
    """Tools for working with OpenCV images through numpy.
    Various utilities, including color transforms, are implemented using
    numpy for speed.

    Change log:
      2016/01/24 -- module started with imports; nloomis@gmail.com
      2016/02/10 -- perceptual color models added; simpler api for color-to-
                    gray compression; nloomis@
    """

- After the initial module documentation, start with a hidden tuple named
  "__authors__". If the module already exists, please add your e-mail to the
  authors list when you contribute!

   Example:
   """This module does amazing things."""
   __authors__ = ('adampretiss@physics.raman.edu',)

- When listing imports, start with the local imports, followed by the system-
  wide imports. Separate the two sections with a single blank line. Put the
  imports in alphabetical order within each section.

   Example:
    import mymodule
    import secondlocalmodule
    import thirdlocalmodule as third

    import matplotlib.pyplot as plt
    import numpy

- Please don't import into the base namespace to avoid name collision. You are
  welcome to use a short import-as name to limit your typing.

    OK:
      import numpy
      import numpy as np

    Bad:
      from numpy import *

- Every function should include a one-line doc string, followed by additional
  explanation as needed.
