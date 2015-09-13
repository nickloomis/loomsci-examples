function sRGB = compand(rgb_linear)
% Convert from linear rgb to sRGB.
% sRGB is used to represent image pixels. Linear rgb is related to the
% energy in each pixel. Since (incoherent) light energy adds linearly, it
% is easier to get good results by doing math in the linear rgb space.
%
% Equation from Bruce Lindbloom:
% http://www.brucelindbloom.com/index.html?Eqn_XYZ_to_RGB.html
%
% Change log:
%  2015/09/06 -- copied from Bruce Lindbloom's website; nloomis@
%

sRGB_double = 1.055 * rgb_linear .^ (1 / 2.4) - 0.055;
low_flag = rgb_linear <= 0.0031308;
if any(low_flag(:))
    sRGB_double(low_flag) = 12.92 * rgb_linear(low_flag);
end
sRGB = uint8(255 * sRGB_double);