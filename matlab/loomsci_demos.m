function loomsci_demos(demo_name)
% Run simple demos of code from loomsci.wordpress.com.
%
% Demos include:
%  diagonal_pixellation : diagonal halftoning
%  diagonal_pixellation color : diagonal halftoning, per color channel
%
% Change log:
%  2015/09/04 -- started demo function with diagonal_pixellation; nloomis@
%  2015/09/05 -- added diagonal_pixellation color; nloomis@

short_name = strtrim(lower(demo_name));
known_demos = {'diagonal_pixellation', ...
    'diagonal_pixellationcolor'};
%TODO: check that short_name is in known_demos, otherwise, throw an error
%early

switch short_name
    case 'diagonal_pixellation'
        src = fullfile(repo_base(), '..', 'images', 'chicago-small.png');
        t = imread(src);
        T_diag = diagonal_pixellation(t, 8, 40, 16);
        myimagesc(T_diag);
        colormap gray
        title('Demo: diagonal pixellation');
        
    case 'diagonal_pixellationcolor'
        src = fullfile(repo_base(), '..', 'images', 'chicago-small.png');
        t = imread(src);
        diag_img = cell(1,3);
        for ch = 1:3
            diag_img{ch} = diagonal_pixellation(t(:,:,ch), 8, 40, 16);
        end
        T_diag = cat(3, diag_img{1}, diag_img{2}, diag_img{3});
        myimagesc(T_diag);
        title('Demo: diagonal pixellation, color');
        
    otherwise
        error('loomsci_demos:DemoExNameNotKnown', ...
            ['The requested demo, ', demo_name, ', is not known.'])
end