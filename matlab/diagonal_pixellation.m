function T = diagonal_pixellation(t, nlevels, nblocks, nppb)
% Draws an image using a triangular halftone.
% The original image is divided into blocks, and each block is converted
% into a diagonal halftone based on its grayscale level. The output image
% is binary, but looks like the original from a distance.
%
% Inputs:
% t: input image (type: uint8 assumed)
% nlevels: number of discrete gray levels to target (default is nppb * 0.4;
%          if the default nppb is used, this is 8 gray levels)
% nblocks: number of blocks in the vertical direction in the output image
%          (default is 60)
% nppb: number of pixels per block in the output image (default is 20)
%
% originally posted to
% https://loomsci.wordpress.com/2013/09/09/diagonal-halftones-on-square-grids/
%
% Change log:
%  2013/09/09 -- original function written, copy-pasted to website;
%                nloomis@
%  2015/09/04 -- copied back to matlab, cleaned up a bit; nloomis@
%

%super-quick arg parsing: set some defaults
if nargin < 4
    nppb = 20;
end
if nargin < 3
    nblocks = 60;
end
if nargin < 2
    nlevels = round(nppb * 0.4);
end

%convert to grayscale if input is RGB
if size(t, 3) == 3
    t = rgb2gray(t);
end

%scale the image, enforce clipping limits (important if t is not uint8)
st = size(t);
tsm = imresize(t, [nblocks, round(nblocks * st(2) / st(1))]);
st = size(tsm); %redefine the size of t
tsm = clamp(tsm, 0, 255); %TODO: imresize should keep uint8 limits...

%find the number of lines to add or subtract from a half-fill
tsm = round(-(double(tsm) / 255 - 0.5) * 2 * nlevels); 
  %convert to nearest discretized gray level from the number of levels
  %specified by the user

%storage for final product
T = zeros(size(tsm) * nppb);
r = (0:st(1) - 1) * nppb + 1;
c = (0:st(2) - 1) * nppb + 1;
[C, R] = meshgrid(c, r);

%build the image
for j = 1:numel(tsm)
    block = fillUT(nppb, tsm(j));
    T(R(j):R(j) + nppb - 1, C(j):C(j) + nppb - 1) = block;
end

%create a diagonally-filled block to use for drawing
function B = fillUT(nppb, k)
k = min(nppb - 1, k); %limit k
B = zeros(nppb);
for j = k:nppb
    dB = nppb - abs(j);
    B = B + diag(ones(dB, 1), j);
end