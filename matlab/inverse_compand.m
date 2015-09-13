function rgb = inverse_compand(sRGB)
% Convert from sRGB to linear rgb.
% sRGB is used to represent image pixels. Linear rgb is related to the
% energy in each pixel. Since (incoherent) light energy adds linearly, it
% is easier to get good results by doing math in the linear rgb space.
%
% Equation from Bruce Lindbloom:
% http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
%
% Change log:
%  2015/09/06 -- copied from Bruce Lindbloom's website; nloomis@
%

sRGB_double = double(sRGB) / 255; %scale to be [0..1]
rgb = ((sRGB_double + 0.055) / 1.055).^2.4;
low_flag = sRGB_double <= 0.04045;
if any(low_flag(:))
    rgb(low_flag) = sRGB_double(low_flag) / 12.92;
end