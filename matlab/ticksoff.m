function [xticks, yticks, zticks] = ticksoff(h)
% Removes the ticks on the current plot axes.
%
% Change log:
%  2015/08/22 -- copied out of nloomis@gmail.com's personal collection

%grab the current axes if the user didn't specify one
if nargin == 0
    h = gca();
end

%return the current set of ticks so that the user can
%re-instate them if needed.
if nargout > 1
    xticks = get(h, 'xtick');
    yticks = get(h, 'ytick');
    zticks = get(h, 'ztick');
end

%remove the ticks
set(h, 'xtick', [], 'ytick', [], 'ztick', [])