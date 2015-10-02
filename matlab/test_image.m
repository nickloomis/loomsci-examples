function img = test_image(varargin)
% Load in a test image from loomsci-examples/images easily.
%
% Inputs:
%  image_name: a string which specifies which image from the images/
%   directory to load. the string can be short -- it only needs to have a
%   unique partial match to the filenames in the directory. (if no unique
%   match can be found, validatestring() will throw an error, however.)
%
%  Note: if no inputs are given, the list of image names is returned.
%
% Outputs:
%  img: the image from the example images directory.
%
% Examples:
%  test_image() --> returns a list of images in the images/ directory
%  test_image('chicago') --> returns chicago-small.png
%  test_image('chicago-small.png') --> returns chicago-small.png
%  test_image('chi') --> returns chicago-small.png if no other file starts
%                        with the letters 'chi'
%  test_image(';;1029i') --> will throw an error; no file has this name
%
% Change log:
%  2015/09/28 -- rewritten from a personal tool; nloomis@gmail.com
%

%get a list of the images in the directory
srcdir = test_image_dir();
images = dir_images(srcdir);
n_img = numel(images);
names = cell(n_img, 1);
for j = 1:n_img
    [~, base, ext] = fileparts(images(j).name);
    names{j} = [base, ext];
end

if nargin == 0
    %return the names of the images in the image/ directory
    img = names;
elseif ischar(varargin{1})
    %search for the named file
    valid_str = validatestring(varargin{1}, names);
    str_idx = logical(strcmp(names, valid_str));
    img = imread(images(str_idx).name);
else
    error('test_image:ExpectedString', 'Expected an image name string.');
end