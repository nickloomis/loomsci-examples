function status = my_make_dir(dir_name)
% Same functionality as mkdir, but checks that directory doesn't already
% exist before trying to create it -- saving on annoying error messages or
% the need to control which error messages are shown. Convenience function.
%
% Inputs: 
%  dir_name: name of the directory to try creating. uses the same arguments
%   as mkdir().
%
% Outputs:
%  status: 1 if the directory was created or already exists; an error code
%   otherwise. same as mkdir().
%
% See also:
%  mkdir
%
% Change log:
%  2015/09/22 -- original function written; nloomis@gmail.com
%


if ~exist(dir_name, 'dir')
    %the directory doesn't exist, so try to make it
    [status, message] = mkdir(dir_name);
    if ~status
        %let the user know that there was an error trying to create this
        %directory by throwing a warning
        warning(message);
    end
else
    %the directory already exists. in that case, return the success status
    %code of 1, the same as mkdir would for success.
    status = 1;
end