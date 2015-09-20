function HT = halftone_using_dict_fast(image, dict)
% Halftone an image using a dictionary of halftone patches using a fast
% look-up table implementation. The matching is based on finding the
% halftone with the smallest luminance error (the nearest-neighbor look-up
% in linear luminance space).
%
% Inputs:
%  image: an image to halftone; uint8. if the image is rgb, it will be
%   converted to grayscale before halftoning. to generate color halftones,
%   process each color channel separately, then combine using cat().
%  dict: a halftone dictionary. see halftone_dict() or any of the
%   make*_halftone functions for more details.
%
% Example:
%  blocks = make_diagonal_blocks(16);
%  dict = make_halftone_dict(blocks);
%  ht = halftone_using_dict_fast(my_img, dict);
%
%  ht_red = halftone_using_dict_fast(my_img(:,:,1), dict);
%  ht_green = halftone_using_dict_fast(my_img(:,:,2), dict);
%  ht_blue = halftone_using_dict_fast(my_img(:,:,3), dict);
%  ht_color = cat(3, ht_red, ht_green, ht_blue);
% 
% See also:
%  halftone_using_dict, halftone_dict
%
% Change log:
%  2015/09/14 -- original function written, nloomis@
%

%build a luminance LUT for the halftones
lum_patches = halftone_dict(dict, 'mean luminance'); %luminance of halftone patches
[lum_sorted, lum_idx] = sort(lum_patches); %LUT -- but it may not be indexable by interp1.

%check that a LUT can be built in the first place
if numel(unique(lum_patches)) ~= numel(lum_patches)
    %there are some halftones with the same luminance; look-ups will fail.
    %bail early and notify the user.
    error('halftone_using_dict_fast:HalftoneLuminancesAreNotUnique', ...
        'Some halftone patches have the same luminance; no LUT can be built.');
end
%another approach: only use the unique values in the lum_patches for the
%lut. this would mean a few halftones would never be used, but it would
%mean the lut could always be used.
%another approach: use the unique values for the look-up. for image patches
%that matches against several halftones with the same luminance, cycle
%through the halftones.
%interp1u would be helpful here.

%size of the halftones in the dictionary
ht_size = size(dict{1}.pattern);

%number of halftone blocks to represent the image
image_size = size(image);
nx = round(image_size(2) / ht_size(2));
ny = round(image_size(1) / ht_size(1));

%resize the source luminance image
lum_img = inverse_compand(image);
if size(lum_img, 3) == 3
    %convert to grayscale if rgb:
    lum_img = rgb2gray(lum_img);
end
lum_resized = clamp(imresize(lum_img, [ny, nx]), 0, 1);

%use the LUT to find the nearest halftone in luminance space
ht_idx = interp1(lum_sorted, lum_idx, lum_resized(:), 'nearest', 'extrap');

%reserve space for the halftone image
HT = zeros(ny * ht_size(1), nx * ht_size(2), size(dict{1}.pattern, 3));

%compute indexing
rstart = (0:ny - 1) * ht_size(1) + 1;
cstart = (0:nx - 1) * ht_size(2) + 1;
[Cstart, Rstart] = meshgrid(cstart, rstart);
Rend = Rstart + ht_size(1) - 1;
Cend = Cstart + ht_size(2) - 1;

%build the halftone image
for j = 1:numel(Rstart)
    HT(Rstart(j):Rend(j), Cstart(j):Cend(j), :) = dict{ht_idx(j)}.pattern;
end
