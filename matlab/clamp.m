function v = clamp(v, min_val, max_val)
% Clamps the values in the input vector so that values less than min_val
% are replaced by min_val, and values greater than max_val are replaced by
% max_val.
%
% Examples:
%  clamp([-1, 0, 0.2, 0.5, 1, 2], 0, 1) --> [0, 0, 0.2, 0.5, 1, 1]
%  clamp(5, -2, 20) --> 5 %no clamping is applied
%  clamp(-.2, 0, 1) --> 0 %clamps -.2 to 0
%
% Change log:
%  2015/09/05 -- convenience function; nloomis@
%

v(v < min_val) = min_val;
v(v > max_val) = max_val;