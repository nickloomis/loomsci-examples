function [xticks, yticks] = myimagesc(img, limits, im_title)
% Convenience function for displaying images using appropriate settings.
%
% Change log:
%  2015/08/22 -- hacked together; nloomis@gmail.com
%

%defaults
default_limits = [];

%if the user passed one arg, assume that limits should be the default.
if nargin < 2
    limits = default_limits;
end

%display the image using imagesc
if isempty(limits)
    imagesc(img);
else
    imagesc(img, limits)
end

%set the rest of the display elements
[xticks, yticks] = ticksoff();
axis image
if nargin >= 3
    title(im_title)
end