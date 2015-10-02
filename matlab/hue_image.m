function img = hue_image(npixels)
%
% Generates an image of a hue circle.
%
% Inputs:
%  npixels: number of pixels on a side in the output image.
%
% Outputs:
%  img: image of a hue circle, with saturation ranging from 0% at the
%   center to 100% at the edge. the image is a uint8 sRGB, and can be
%   written directly to disk or displayed without further modification of
%   the colors.
%
% Change log:
%  2015/09/21 -- original function written; nloomis@gmail.com
%

%compute a radial grid
x = linspace(-1, 1, npixels);
[X, Y] = meshgrid(x, x);
R = sqrt(X.^2 + Y.^2);
Th = atan2(Y, X);
r_max = 0.9;

%create hue, saturation, and value components
hue_comp = (Th + pi) / (2 * pi);
sat_comp = R / r_max; %0 at the center to 1 at R = r_max
val_comp = ones(npixels, npixels);
val_comp(R > r_max) = 0;

%convert from hsv to an sRGB image
hsv_img = cat(3, hue_comp, sat_comp, val_comp);
img = uint8(255 * hsv2rgb(hsv_img));