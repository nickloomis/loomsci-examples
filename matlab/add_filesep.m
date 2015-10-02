function pathstr = add_filesep(pathstr)
%
% If the input string does not end with a filesep character, the system's
% filesep is added. Otherwise, the string is returned as-is. This is a
% convenience function.
%
% Change log:
%  2015/09/22 -- original function written; nloomis@gmail.com
%  2015/09/23 -- added check that pathstr is not empty; nloomis@

if ~isempty(pathstr)
    if pathstr(end) ~= filesep
        pathstr = [pathstr, filesep];
    end
end