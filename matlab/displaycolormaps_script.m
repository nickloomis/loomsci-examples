%list of advertised names; see doc graph3d
colormap_names = {'parula', 'jet', 'hsv', ...
    'hot', 'cool', 'spring', 'summer', 'autumn', 'winter', ...
    'gray', 'bone', 'copper', 'pink', ...
    'flag', 'lines', 'colorcube', 'vga', 'prism', 'white'};
nmaps = numel(colormap_names);

margin = 0.1; %how much to shift the left side of the axes in order
  %to leave room for labels

for j = 1:nmaps
    %set a subplot
    subplot(nmaps, 1, j);
    
    %make an image of the colormap and display it
    cmap = colormap(colormap_names{j});
    cmap_img = ind2rgb(1:size(cmap, 1), cmap);
    image(cmap_img); ticksoff;
    
    %inset the axes to make room for text
    ah = gca;
    pos = get(ah, 'position');
    set(ah, 'position', ...
        [pos(1) + margin, pos(2), pos(3) - margin, pos(4)]);
    
    %plop some text down; i experimented with the positioning to get
    %something that looked OK
    text(-2, .75, colormap_names{j}, 'horizontalalignment', 'right', ...
        'verticalalignment', 'middle', 'fontsize', 12, ...
        'units', 'characters');
end