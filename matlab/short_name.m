function shorts = short_name(str)
% Strips all characters which are not alphanumeric, converts to lowercase,
% and returns the result. This makes it easier to match strings with fewer
% formatting requirements for the user -- they just need to get the letters
% in the right order.
%
% Examples:
%  short_name('foo bar') --> 'foobar'
%  short_name('long-text_underscores') --> 'longtextunderscores'
%  short_name('23 text 56') --> '23text56'
%
% Change log:
%  2015/09/05 -- convenience function; nloomis@
%

shorts = lower(str(isstrprop(str, 'alphanum')));