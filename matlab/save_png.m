function save_png(basename, fh, reso)
%
% Save the figure as a png file; convenience function.
%
% Inputs:
%  basename: the name of the file to save; a '.png' will be appended if the
%   filename doesn't already contain the png extension
%  fh: figure handle to the window to save as an image; if fh is no
%   supplied or is empty, the current window will be used
%  reso: resolution to use when saving the image; default is 144 (2x higher
%   than the on-screen resolution, typically)
%
% Examples:
%  fh = figure();
%  <plot or display something to fh>
%  save_png('foo.png', fh) (default reso)
%  save_png('path/foo.png') (gcf, default reso)
%  save_png('foo') (saves to foo.png, gcf, default reso)
%  save_png('foo.png', [], 300)
%  save_png('foo', fh, 600)
%
% Change log:
%  2015/09/22 -- original function written; nloomis@gmail.com
%

%defaults
if nargin < 2
    fh = gcf;
elseif isempty(fh)
    fh = gcf;
end
if nargin < 3
    reso = 144;
end

%save figure using png
print(fh, '-dpng', ['-r', num2str(reso)], ...
    check_ext(basename, '.png'))

%note to the intrepid: it'd be easy to use fileparts() to get the
%filename's extension, then look up the matching -d flag for the print()
%function -- so that you could automatically switch to a different image
%type using the extension alone.