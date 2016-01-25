"""
Demos for using the modules and packages in loomsci-examples/python.

To run a demo, type the name (with or without 'demo_' preceeding it) at the
python command line. For example, to run demo_awesomeness(), use
  $ python loomsci_demos.py awesomeness
or
  $ python loomsci_demos.py demo_awesomeness

Naming: all demo functions should start with "demo_".

Functions: Demos are meant to provide a simple and complete example of how to
use the code. They are expected to be self-contained, including all the
necessary imports and inputs; the user should only have to run the function
to see an example. The demo does not need to print output at each step: it only
needs to be documented within the code itself.

Change log:
  2015 -- module started; nloomis@gmail.com
  2016/01/18 -- self-inspection added to find demo_* functions; nloomis@
"""
__authors__ = ('nloomis@gmail.com',)

import inspect
import sys

#
# demo functions for modules and packages
#

def demo_digitalholography():
    """Reconstruct a sample digital hologram."""
    import digitalholography as dhi
    holo = dhi.Hologram(658e-6, 9e-3)
    holo.load('../images/godzillaholo.bmp')
    holo.show_intensity(54) #z = [50, 54, 58, 108]

def demo_steerablederiv():
    """Display the kernel of a steerable derivative filter."""
    import imageutils
    S = imageutils.steerable_deriv(sigma=14.1, n_pix=61)
    imageutils.imshow(S)
    imageutils.plt.xlabel('x pixel')
    imageutils.plt.ylabel('y pixel')
    imageutils.plt.title('Steerable derivative; sigma = 14.1, 61 pixels')
    imageutils.plt.colorbar()
    imageutils.plt.show()

#
# functions to run different demos
#

def _find_demos():
    """Return a dictionary of functions in this file starting with 'demo_'."""
    # Example borrowed from
    #https://bytes.com/topic/python/answers/25264-list-all-functions-defined-current-module
    self_reference = __import__(inspect.getmodulename(__file__))
    demo_funcs = {k: v for k, v in self_reference.__dict__.items() 
                  if isinstance(k, basestring) and k.startswith('demo_')}
    #TODO(nloomis): remember to check also that it's a function! import types.
    return demo_funcs

def demo_test():
    """Simple test demo to make sure inspection works."""
    print "Demo tester: works!"

def _print_demo_names(demo_funcs_dict):
    """Print a list of available demo names. Uses the short name form."""
    print "There are %d demos available:" % len(demo_funcs_dict)
    for long_name in demo_funcs_dict.keys():
        short_name = long_name[5:]
        print "  %s" % short_name

def run_demo(demo_name=None):
    """Runs a specific demo, or else lists the available demos.

    The demo name can be with or without the 'demo_' string: both 'awesomeness'
    and 'demo_awesomeness' will run the demo_awesomeness() function if it is
    available in this file.
    If the demo name doesn't match, or is None, a list of available demo
    functions is printed to the terminal instead.
    """
    demo_funcs_dict = _find_demos();
    if not demo_name:
        _print_demo_names(demo_funcs_dict)
        return
    if not demo_name.startswith('demo_'):
        demo_name = 'demo_' + demo_name
    if not demo_funcs_dict.has_key(demo_name):
        print "The function %s can't be found!" % demo_name
        _print_demo_names(demo_funcs)
        return
    demo_funcs_dict[demo_name]()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_demo()
    else:
        run_demo(sys.argv[1])
