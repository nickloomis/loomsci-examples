function cell_v = make_cell(v)
% Returns the input as a cell, if it is not already a cell.
% Convenience function. Useful if a cell is expected, but you aren't sure
% what type of data you have.
%
% Change log:
%  2015/09/22 -- hacked together; nloomis@gmail.com
%

if ~iscell(v)
    cell_v = {v};
else
    cell_v = v;
end