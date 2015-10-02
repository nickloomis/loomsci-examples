function cform = colorblind_matrix(lms_sensitivities)
% Generates the color transform matrix to represent a colorblind
% individual's perception. The transform matrix takes linear rgb as input,
% and outputs in linear rgb space.
%
% Inputs:
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
% See also:
%  colorblind_image, apply_color_matrix, inverse_compand, compand
%
% Change log:
%  2015/09/24 -- copied out of colorblind_image; nloomis@gmail.com
%

%create the transform matrices from rgb->LMS->limited_LMS->rgb
rgb2lms = color_matrix('rgb2lms');
lms2rgb = inv(rgb2lms);
lms_sense = diag(lms_sensitivities);
cform = lms2rgb * lms_sense * rgb2lms; %#ok<MINV>
row_sum = sum(cform, 2);
cform = cform ./ repmat(row_sum, [1, 3]);
%note: division by the row_sum means that the sum of each row will be
%unity, and neutral colors will keep the same balance. the effect is that a
%white color will still look white to a three-cone observer after the
%transform, instead of having a color cast (due to a missing cone).
%
%there are some situations where the row sum is extremely small (for
%example, lms=[1, 1, 0.1]), and the division leads to strong bands of 
%colors as the white balance suddenly shifts.
%
%i'd be interested to know if colorblind individuals can detect the
%difference between images that have been processed with and without row
%normalization.