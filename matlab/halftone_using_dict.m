function HT = halftone_using_dict(image, dict, method, varargin)
% Use a halftone dictionary to halftone an image.
%
% The image is divided into blocks the same size as the halftones in the
% dictionary, then each block is matched to its best representative
% halftone using the matching method specified by the user (luminance
% matching by default). The matching halftone is saved into the final
% halftone image.
%
% Inputs:
%  image: the image to convert to halftones; uint8. note that halftone
%   matching (through halftone_dict) is done using grayscale patches, so
%   rgb images will be converted by halftone_dict(). to generate halftones
%   for each color channel, run halftone_using_dict() separately for each
%   color channel in the image, then combine the channels using cat().
%  dict: a halftone dictionary; see halftone_dict() for dictionary
%   management tools, or any of the make_*halftone_dict() functions.
%  method: one of the strings recognized by halftone_dict() for selecting
%   halftone patterns:
%        'get halftone' %luminance matching (default)
%        'get halftone srgb' %srgb-mean matching
%        'get halftone nxn' %luminance + NxN spatial matching
%   if method is 'get halftone nxn', the fourth argument into
%   halftone_using_dict should be the spatial match size. for example, to
%   use a 5x5 spatial match,
%    ht = halftone_using_dict(image, dict, 'get halftone nxn', 5);
%   the method string does not have punctuation or capitalization 
%   requirements.
%  varargin: additional arguments used by halftone_dict (if any) for the
%   requested matching method
%
% Example usage:
%  blocks = make_diagonal_blocks(16); %series of halftone patches
%  dict = make_halftone_dict(blocks); %build a halftone dictionary
%  ht = halftone_using_dict(my_img, dict); %use luminance matching to
%                                          %halftone my_img
%
% See also:
%  halftone_using_dict_fast, halftone_dict
%
% Change log:
%  2015/09/05 -- original version written; nloomis@
%  2015/09/10 -- modified for NxN halftones, additional args; nloomis@
%

%quick arg parsing for defaults
if nargin < 3
    method = 'get halftone'; %luminance matching
end

%size of the halftones in the dictionary
ht_size = size(dict{1}.pattern);

%number of halftone blocks to represent the image
image_size = size(image);
nx = floor(image_size(2) / ht_size(2));
ny = floor(image_size(1) / ht_size(1));
%idea: tell the user if the image is not an integer number of multiples of
%the halftone size, and what the next closest size would be; that way, they
%can resize the image to match the halftones if desired.

%reserve space for the halftone image
HT = zeros(ny * ht_size(1), nx * ht_size(2), size(dict{1}.pattern, 3));

%compute indexing
rstart = (0:ny - 1) * ht_size(1) + 1;
cstart = (0:nx - 1) * ht_size(2) + 1;
rend = rstart + ht_size(1) - 1;
cend = cstart + ht_size(2) - 1;

%generate the halftone image
for r = 1:ny
    for c = 1:nx
        patch = image(rstart(r):rend(r), cstart(c):cend(c), :);
        ht = halftone_dict(dict, method, patch, varargin{:});
        HT(rstart(r):rend(r), cstart(c):cend(c), :) = ht;
    end
end