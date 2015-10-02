The matrices in this directory are for simulating specific types of colorblindness:
 prot: protanopia, or no red cones ([0,1,1] cone sensitivities)
 deut: deuteranopia, or no green cones ([1,0,1] cone sensitivities)
 trit: tritanopia, or no blue cones ([1,1,0] cone sensitivities)
 blue: blue-only monopia ([0,0,1] cone sensitivities)

The matrices convert from linear-RGB to linear-RGB using a simple multiplication:

  [ cb_red ]   [a11 a12 a13][ lin_red ]
  [cb_green] = [a21 a22 a23][lin_green]
  [cb_blue ]   [a31 a32 a33][lin_blue ]

The [lin_red; lin_green; lin_blue] vector is a color in linear-RGB space, and is what a trichomatic viewer would see. The [cb_red; cb_green; cb_blue] vector is a color in linear-RGB space, and is what a colorblind viewer would see (ie, the response for the missing cones has been removed from the color). The [aij] matrix is the color-conversion matrix of your choice.

The matrices were generated using matlab/colorblind_matrix.m. See documentation in the function for more details.
The matrices can be used to convert images using matlab/apply_color_matrix.m or by doing your own matrix multiplication.

NB: the term "linear-RGB" refers to the linearized RGB values -- not the pixel values in an image! The pixel values need to be inversely companded from the compressed sRGB space to a linear RGB space. See matlab/inverse_compand.m and matlab/compand.m, or the sRGB specs on wikipedia.