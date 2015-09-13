function W = land_illusion(t)
% Returns an image which uses Land's illusion to give a sense of color -- 
% but without all colors present in the output image.
% This version approximates what Land's original illusion did, by
% projecting the red channel and the gray image onto the same screen. It
% uses the image processing toolbox to combine the colors
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

%check for the ipt... or another function by the same name which can return
%the necessary transforms.
if ~exist('makecform', 'file')
    error('land_illusion:MissingIPToolbox', ...
        'Requires color transforms in the image processing toolbox.');
end

%create an red-channel-only image and scale to [0..1]
R = zeros(size(t));
R(:,:,1) = double(t(:,:,1)) / 255;

%create grayscale image and scale to [0..1]
G = repmat(rgb2gray(double(t) / 255), [1, 1, 3]);

%convert to XYZ colorspace
crgb2xyz = makecform('srgb2xyz');
cxyz2rgb = makecform('xyz2srgb');
rxyz = applycform(R, crgb2xyz);
gxyz = applycform(G, crgb2xyz);

%combine the gray and red images as if they were projected on top of the
%same screen, with 40% strength in the red image and 60% strength in the
%gray image
wxyz = 0.4 * rxyz + 0.6 * gxyz;

%convert back to RGB space and cast to uint8
W = uint8(255 * applycform(wxyz, cxyz2rgb));
