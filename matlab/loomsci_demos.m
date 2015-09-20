function loomsci_demos(demo_name)
% Run simple demos of code from loomsci.wordpress.com.
%
% The demo_name is a string which identifies the particular demo to show;
% spaces, capitalization, underscores, dashes, etc don't matter in the
% string. (Hint: validatestring is also used, so you only need the first
% few unambiguous letters in the demo name.)
%
% Demos include:
%  diagonal pixellation : diagonal halftoning (fast approximation)
%  diagonal pixellation color : diagonal halftoning, per color channel
%  land illusion stripes : Land's illusion, using stripes
%  land illusion : Land's illusion using overlapping projections
%  diagonal halftone : halftoning using a dictionary of diagonal wedges
%  fast halftone : halftoning using a look-up table
%
% Change log:
%  2015/09/04 -- started demo function with diagonal_pixellation; nloomis@
%  2015/09/05 -- added diagonal_pixellation color; converted to use
%                short_name() and validatestring() for parsing the input 
%                string; added land's illusion demos; nloomis@
%  2015/09/06 -- added diagonalhalftone; nloomis@
%  2015/09/14 -- added fasthalftone; nloomis@

known_demos = {'diagonalpixellation', ...
    'diagonalpixellationcolor', ...
    'landillusionstripes', ...
    'landillusion', ...
    'diagonalhalftone', ...
    'fasthalftone'};
valid_short = validatestring(short_name(demo_name), known_demos);

switch valid_short
    case 'diagonalpixellation'
        src = fullfile(repo_base(), '..', 'images', 'chicago-small.png');
        t = imread(src);
        T_diag = diagonal_pixellation(t, 8, 40, 16);
        myimagesc(T_diag);
        colormap gray
        title('Demo: diagonal pixellation');
        
    case 'diagonalpixellationcolor'
        src = fullfile(repo_base(), '..', 'images', 'chicago-small.png');
        t = imread(src);
        diag_img = cell(1,3);
        for ch = 1:3
            diag_img{ch} = diagonal_pixellation(t(:,:,ch), 8, 40, 16);
        end
        T_diag = cat(3, diag_img{1}, diag_img{2}, diag_img{3});
        myimagesc(T_diag);
        title('Demo: diagonal pixellation, color');
    
    case 'landillusionstripes'
        src = fullfile(repo_base(), '..', 'images', 'chicago-small.png');
        t = imread(src);
        T = land_illusion_stripes(t);
        myimagesc(T);
        title('Demo: Land''s illusion using stripes')
        if ~isempty(which('truesize'))
            truesize()
        end
    
    case 'landillusion'
        src = fullfile(repo_base(), '..', 'images', 'chicago-small.png');
        t = imread(src);
        T = land_illusion(t);
        myimagesc(T);
        title('Demo: Land''s illusion (original)')

    case 'diagonalhalftone'
        src = fullfile(repo_base(), '..', 'images', 'chicago-small.png');
        t = imread(src);
        blocks = make_diagonal_blocks(16);
        dict = make_halftone_dict(blocks);
        htr = halftone_using_dict(t(:, :, 1), dict);
        htg = halftone_using_dict(t(:, :, 2), dict);
        htb = halftone_using_dict(t(:, :, 3), dict);
        ht3 = cat(3, htr, htg, htb);
        myimagesc(ht3);
        title('Demo: halftoning in a linear color space');
    
    case 'fasthalftone'
        src = fullfile(repo_base(), '..', 'images', 'chicago-small.png');
        t = imread(src);
        blocks = make_diagonal_blocks(16);
        dict = make_halftone_dict(blocks);
        ht = halftone_using_dict_fast(t, dict);
        myimagesc(ht);
        title('Demo: fast halftoning in a linear color space');
        
    otherwise
        error('loomsci_demos:DemoExNameNotKnown', ...
            ['The requested demo, ', demo_name, ', is not known.'])
end