function is_figure = is_figure_handle(fh)
% Checks to see if an input is a figure handle. Returns true if it is a
% figure handle, false if it is not a handle or is not a figure handle.
%
% Change log:
%  2015/09/28 -- hacked together; nloomis@gmail.com
%

is_figure = false;
if ishandle(fh)
    if strcmp(get(fh, 'type'), 'figure')
        is_figure = true;
    end
end