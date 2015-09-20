function dict = make_thickline_halftone_dict(block_size)
%
% Make a halftone dictionary whose halftone image patches are horizontal
% lines of varying thicknesses. The line is bright, and the background is
% dark.
%
% Input:
%  block_size: the size of the halftone block in pixels. the block_size
%   paramter determines the number of halftones generated, making one line
%   width from 1 up to block_size(1) and a black patch (for block_size(1)+1
%   total halftones). block_size can be a scalar or a vector. if block_size
%   is a scalar, the same scalar size is used for both the x and y
%   directions of the halftone block. if block_size is a vector, it
%   specifies the number of vertical and horizontal pixels as
%     [y_pix, x_pix] = [block_size(1), block_size(2)].
%   note that if x_pix is less than y_pix, images generated using the
%   dictionary will have a higher imaging resolution in the horizontal 
%   direction than the vertical direction. (in other words, there will be
%   more discernable detail in the x direction.) conversely, x_pix > y_pix
%   will have more detail in the vertical direction.
%
% Output:
%  dict, a halftone dictionary.
%
% See also:
%  halftone_using_dict, halftone_using_dict_fast, make_*halftone_dict
%
% Change log:
%  2015/09/19 -- original function written; nloomis@
%

%convert from a scalar size value to a vector size (as [y_pix, x_pix])
if numel(block_size) == 1
    block_size = [1, 1] * block_size;
end

%reserve memory
blocks = cell(block_size(1) + 1, 1);

%make an all-zero block (black)
blocks{1} = zeros(block_size, 'uint8');

%create blocks with different horizontal line widths
for lw = 1:block_size(1)
    start_idx = floor(block_size(1) / 2 - lw / 2) + 1;
    end_idx = start_idx + lw - 1;
    block = zeros(block_size, 'uint8');
    block(start_idx:end_idx, :) = 255;
    blocks{lw + 1} = block;
end

%build the dictionary using the halftone blocks
dict = make_halftone_dict(blocks);