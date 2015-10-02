function dir_contents = dir_by_ext(srcdir, exts)
% Finds the files in a directory which match the list of extensions
% supplied. Useful when there are multiple extensions which have similar
% meanings.
%
% Inputs:
%  srcdir: the directory with files to scan. the string does not need to
%   end with a filesep, but it may.
%  exts: string or cell array of strings specifying which extensions to
%   include in the directory results. extensions do not need to contain a
%   dot as their first character, but may for convenience. the extensions
%   are matched using case-insensitive comparisons.
%
% Outputs:
%  dir_contents: a struct containing a list of all matching files; same
%   struct format as dir() returns. files are in the same order as the
%   extensions in exts.
%
% Examples:
%  tiffs = dir_by_ext(mydir, {'.tif', '.tiff'});
%  images = dir_by_ext(mydir, {'jpg', 'jpeg', 'png', 'bmp'});
%  htmls = dir_by_ext(mydir, {'htm', 'html'});
%  txt_docs = dir_by_ext(mydir, 'txt');
%
% See also:
%  dir_images, check_ext
%
% Change log:
%  2015/09/22 -- original function written; nloomis@gmail.com
%  2015/09/28 -- docstring added; nloomis@
%

srcdir = add_filesep(srcdir);
exts = make_cell(exts);

dir_contents = [];

for j = 1:numel(exts)
    ext = exts{j};
    if ext(1) == '.'
        ext = ext(2:end);
    end
    this_dir = dir([srcdir, '*.', ext]);
    if isempty(dir_contents)
        dir_contents = this_dir;
    else
        dir_contents = [dir_contents; this_dir]; %#ok<AGROW>
    end
end

for j = 1:numel(dir_contents)
    dir_contents(j).name = [srcdir, dir_contents(j).name]; %#ok<AGROW>
end
