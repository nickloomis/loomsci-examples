function dict = make_rotated_halftone_dict(blocks)
% Uses a set of image blocks to build a dictionary of halftones; each block
% is rotated by 90 degrees four times to cover all orientations. The dict
% can be used with halftone_dict() or halftone_using_dict().
%
% Inputs:
%  blocks: a cell array of images to use as halftone patterns. the images
%   need to all have the same size. note that this function assumes that
%   the four rotations of the patterns are unique (ie, it assumes there is
%   no rotational symmetry). image blocks which do have rotational symmetry
%   will result in some patterns being duplicated in the dictionary, and
%   will have slower search/indexing.
%
% Change log:
%  2015/09/10 -- original function written; nloomis@

%build the initial dictionary
dict = make_halftone_dict(blocks);

 %additional 90-degree rotations
for n = 1:3
    for j = 1:numel(blocks)
        dict = halftone_dict(dict, 'add', rot90(blocks{j}, n));
    end
end