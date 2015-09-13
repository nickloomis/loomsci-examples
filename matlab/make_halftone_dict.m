function dict = make_halftone_dict(blocks)
% Utility to build a halftone dictionary from a cell array of halftone
% images.
%
% Inputs:
%  blocks: cell array of halftone images to add to the dictionary. all
%   images should have the same size, and should be 
%
dict = [];
for j = 1:numel(blocks)
    dict = halftone_dict(dict, 'add', blocks{j});
end