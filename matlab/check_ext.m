function filename = check_ext(filename, ext)
% Checks that a filename ends with the correct extension, and returns the
% corrected filename. The extensions are assumed to be case insensitive, so
% that foo.BAR and foo.bar will both match ext='bar'.
%
% Inputs:
%  filename: the filename which should be checked for the correct
%   extension. the extension can be any case. if the filename has the
%   correct extension, it is returned without modifications. if the
%   filename does not have the right extension, it is adjusted and
%   returned.
%  ext: a string giving the desired file extension. the extension can be
%   given with or without a leading period (ie, '.jpg' and 'jpg' are both
%   acceptable). if the filename does not end with this extension, the ext
%   string as input will be used to replace the filename's extension.
%
% Examples:
%  check_ext('foo.bar', 'bar') --> 'foo.bar' (no changes needed)
%  check_ext('foo.bat', 'bar') --> 'foo.bar' (.bat -> .bar)
%  check_ext('alpha\foo', 'bar') --> 'alpha\foo.bar' (additional path args
%                                     are ok, and no extension is necessary
%                                     on the filename)
%  check_ext('foo.bat', '.BAR') --> 'foo.BAR' (.bat -> .BAR, keeps the ext
%                                    formatting as given on the input)
%  check_ext('foo.JPG', '.jpg') --> 'foo.JPG' (the extension matches, so no
%                                    changes are necessary)
%
% Change log:
%  2015/09/23 -- original function written; nloomis@gmail.com
%

if nargin < 2
    error('check_ext:TooFewArguments', 'Expected filename and extension.');
end

%prepend a dot if needed on the extension
if ext(1) ~= '.'
    ext = ['.', ext];
end

%get the extension on the supplied filename
[path, file_base, file_ext] = fileparts(filename);

%if the user's extension doesn't match the desired extension (case
%insensitive), build the correct filename using the right extension
if ~strcmpi(file_ext, ext)
    filename = [add_filesep(path), file_base, ext];
end