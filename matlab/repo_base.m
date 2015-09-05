function d = repo_base()
% Returns the repository base directory which the Matlab codes use as their
% reference. (Note that this isn't necessarily the base of the git repo.)
% Used to locate specific resources using relative paths without requiring 
% users to run code from specific locations.
%
% Change log:
%  2015/09/04 -- simple hack; nloomis@
%

d = [fileparts(which(mfilename)), filesep];