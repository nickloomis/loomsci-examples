function d = test_image_dir()
% Returns the directory where test images are stored in the repo; a
% convenience function.
%
% Change log:
%  2015/09/28 -- simple hack written; nloomis@gmail.com
%

d = fullfile(repo_base(), '..', 'images');