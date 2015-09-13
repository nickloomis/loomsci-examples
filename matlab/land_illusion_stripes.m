function T = land_illusion_stripes(t)
% Returns an image which uses Land's illusion to give a sense of color -- 
% but without all colors present in the output image.
% This version uses alternating red and gray stripes to approximate the
% combination of gray + red-filter which Land used originally, an idea from
% Justin Lee of 1337arts.
%
% originally posted to
% https://loomsci.wordpress.com/2013/08/15/color-perception-illusions/
%
% Inputs: 
%  t: source image, of type uint8
%
% Change log:
%  2015/09/05 -- copied back from website, cleaned up; nloomis@
%

%get a grayscale approximation
g = rgb2gray(t);

%create storage for the output image
T = zeros(size(t), 'uint8');

%copy gray lines into the output image in the odd lines
T(1:2:end, :, :) = repmat(g(1:2:end, :), [1, 1, 3]);

%copy only the red channel into the even-indexed lines
T(2:2:end, :, 1) = t(2:2:end, :, 1);