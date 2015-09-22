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
import cv2 -- both cv and cv2 are part of opencv.

Style Guide
=================
- See PEP0008, https://www.python.org/dev/peps/pep-0008/, for Python formatting
  fundies. While these won't be strictly followed, they're a good reference.
- Use two or four spaces for indenting. Keep the indentation consistent in each
  file.
- Every function should include a one-line doc string, followed by additional
  explanation as needed.
- When listing imports, start with the system-wide imports, followed by the local
  imports. Put the imports in alphabetical order within each section.
- Please don't import into the base namespace to avoid name collision. You are
  welcome to use a short import-as name to limit your typing.
    OK:
      import numpy
      import numpy as np
    Bad:
      from numpy import *

