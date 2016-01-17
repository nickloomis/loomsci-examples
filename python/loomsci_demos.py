#
# Demos for using the modules and packages in loomsci-examples/python.
# 
# Naming: all demo functions should start with "demo_".
# Demo functions should all be listed before the run() function for the sake
# of indexing.
#


import imageutils


#
# helper functions for indexing, showing demos
#

#TODO

#
# demo functions for modules and packages
#

def demo_digitalholography():
	#TODO: docstring
	#TODO: short names for demo added to internal dict
    import digitalholography as dhi
    holo = dhi.Hologram(658e-6, 9e-3)
    holo.load('../images/godzilla.bmp')
    holo.show_intensity(54) #z = [50, 54, 58, 108]

#
# functions to run different demos
#

def run(demo_name=None):
	#TODO(nloomis): index all the demos in this file
	#check that the input matches a demo name, or return the list of possible
	#demos to call
	pass

if __name__ == "__main__":
	run()
#TODO: is this right? check whether sysv passes in args.