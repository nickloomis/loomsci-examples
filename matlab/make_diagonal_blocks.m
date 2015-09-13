function blocks = make_diagonal_blocks(nppb)
% Create a set of diagonally-filled block to use for drawing halftones.
% Builds a cell array of image blocks, each block filled up to a different
% diagonal. This forms a wedge shape, like an upper-triangular or
% lower-triangular matrix.
% The cell array can be input into make_halftone_dict() to generate a
% dictionary of halftones using the diagonal block patterns.
%
% Inputs:
%  nppb: number of pixels per block; this defines the size of the blocks,
%   which are nppb by nppb.
%
% Output:
%  blocks{}: a cell array of image blocks; each block is nppb by nppb
%   pixels in size and is of type uint8. the blocks have a single channel.
%   each block is binary, either 0's or 255's.
%
% Example:
%  blocks = make_diagonal_blocks(20);
%
% Change log:
%  2015/09/06 -- hacked together; nloomis@
%

k = (-nppb + 1):(nppb - 1);
nblocks = numel(k) + 1;
blocks = cell(1, nblocks);
for j = 1:nblocks - 1
    blocks{j} = uint8(fillUT(nppb, k(j)) * 255);
end
blocks{end} = zeros(nppb, nppb, 'uint8');

%create a diagonally-filled block to use for later drawing
%note: this code is copied verbatim from diagonal_pixellation
function B = fillUT(nppb, k)
k = min(nppb - 1, k); %limit k
B = zeros(nppb);
for j = k:nppb
    dB = nppb - abs(j);
    B = B + diag(ones(dB, 1), j);
end