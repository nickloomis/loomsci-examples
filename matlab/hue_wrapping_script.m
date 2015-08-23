%post: "Avoiding Hue Wrapping in Filtered Images"
%
% Copyright nloomis@gmail.com
%
% Change log:
%  2015-08-22 -- original script written; nloomis@
%

t = imread('../images/oaklandlw-zinnias.jpg');
hsv_img = rgb2hsv(t);
hue_angle = hsv_img(:,:,1) * 2 * pi; %convert from [0..1] to radians

%display the original image and the hue angle
figure;
subplot(1,2,1);
myimagesc(t, [], 'Flowers')
subplot(1,2,2);
myimagesc(hue_angle, [0, 2*pi], 'Hue angle (radians)');
colorbar;
colormap(jet);

%hue as a complex number:
hue_complex = exp(1i * hue_angle);

%filtering operations on the complex-valued hue:
h_smoothed = imfilter(hue_complex, fspecial('gaussian', 11, 1.5), ...
    'same', 'replicate');
mean_hue = imfilter(hue_complex, fspecial('gaussian', 23, 7),...
    'same', 'replicate'); %gaussian-weighted local mean
sx = imfilter(h_smoothed, fspecial('sobel'), 'same', 'replicate');
sy = imfilter(h_smoothed, fspecial('sobel')', 'same', 'replicate');
Smag = sqrt(sx .* conj(sx) + sy .* conj(sy));
  %rem: sx, sy are complex-valued; the squared magnitude is either
  %abs(sx).^2 or sx.*conj(sx).

%display a few results
figure; %mean
subplot(1,3,1); myimagesc(t, [], 'Flowers');
subplot(1,3,2); 
myimagesc(angle(mean_hue), [-pi, pi], 'Mean hue angle (rad)'); colorbar;
subplot(1,3,3); 
myimagesc(abs(mean_hue), [], 'Magnitude of mean'); colorbar;
colormap('jet')
figure; %gradient
subplot(1,2,1); myimagesc(t, [], 'Flowers');
subplot(1,2,2);
myimagesc(Smag, [], 'Gradient magnitude');
colorbar;
