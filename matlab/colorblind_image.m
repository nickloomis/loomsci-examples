function cblind_img = colorblind_image(image, lms_sensitivities)
%
% Simulate what a colorblind individual would see given an image and a
% vector of LMS sensitivities.
%
% Inputs:
%  image: an image with uint8 data type.
%  lms_sensitivities: a vector specifying the sensitivities of the [L,M,S]
%   cones in the simulated observer. L corresponds roughly to red, M
%   roughly to green, and S to blues. the sensitivities should be between 0
%   and 1, with 0 meaning that the cone is missing, 1 meaning that the cone
%   is functioning at full efficiency, and values between 0 and 1 meaning
%   that the cone is functioning at reduced efficiency. for example, if the
%   L (red) cone is not present in the simulated observer, set
%    lms_sensitivities = [0, 1, 1].
%   to simulate common types of colorblindness:
%    protanopia: [0, 1, 1] (L cone absent; 1% of males)
%    deuteranopia: [1, 0, 1] (M cone absent; 1% of males)
%    tritanopia: [1, 1, 0] (S cone absent; rare, both genders)
%    protanomaly: [x, 1, 1] (L cone shifted; x < 1; 1% of males)
%    deuteranomaly: [1, x, 1] (M cone shifted; x < 1; 6% of males, 
%                              0.4% females)
%    tritanomaly: [1, 1, x] (S cone shifted; x < 1; rare, both genders)
%   statistics are from wikipedia's
%   https://en.wikipedia.org/wiki/Color_blindness
%
% Outputs:
%  img: a uint8 image of the input image as seen by the simulated
%   colorblind observer
%
% The lms_sensitivities vector is the von Kries adaptation coefficients, so
% this function can also be used to simulate what an image might look like
% under different illuminants. Note that the transform isn't exact, but
% does get close.
%
% Change log:
%  2015/09/21 -- original function written; nloomis@gmail.com
%  2015/09/24 -- copied out the code to generate color transform matrices
%                using the lms_sensitivities to colorblind_matrix; nloomis@
%

%convert the image to linear rgb
lin_rgb = inverse_compand(image);

%get the matrix to convert the linear rgb colors to colorblind limited rgb
cform = colorblind_matrix(lms_sensitivities);

%apply the transform to the lin_rgb image
lin_rgb_lms = apply_color_matrix(lin_rgb, cform);

%compand back into sRGB for display
cblind_img = compand(lin_rgb_lms);
