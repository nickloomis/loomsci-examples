function dir_img = dir_images(srcdir)
% Returns a directory listing containing only image files. The images are
% recognized based on their extensions; it is up to the user to determine
% that they are valid image files (eg, by reading using imread).
%
% Inputs:
%  srcdir: string specifying the directory to search for images. note that
%   only the initial level of the directory is searched; directories
%   contained within the srcdir are not searched recursively.
%
% Outputs:
%  dir_img: a directory structure of the same form as dir(), with all image
%   files.
%
% Only a few of the more popular formats which imread() can read are
% searched. To add additional extensions, modify the image_exts variable in
% the code.
%
% See also:
%  dir_by_ext, dir, imread
%
% Change log:
%  2015/09/23 -- original function written; nloomis@gmail.com
%  2015/09/28 -- added 'jpeg' extension; nloomis@
%

%more popular formats:
image_exts = {'jpg', 'jpeg', 'png', 'tif', 'tiff', 'bmp', 'gif', 'ppm'};

%build the directory listing using these extensions:
dir_img = dir_by_ext(srcdir, image_exts);