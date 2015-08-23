%number of points to generate
npts = 8500;

%make phi points (over [0..pi/2] range)
phi = pi/2 * rand(npts, 1);

%uniform sampling in theta (over [0..pi/2])
theta = pi / 2 - pi/2 * rand(npts, 1);

%inverse sampling in theta (over [0..pi/2])
theta_unif = pi / 2 - acos(rand(npts, 1));
%this name is strange: the theta distribution is non-uniform, but the
%resulting distribution on the sphere <is> uniform

%convert the random spherical coordinates to cartesian for plotting
[x, y, z] = sph2cart(phi, theta, ones(npts, 1));
[x_unif, y_unif, z_unif] = sph2cart(phi, theta_unif, ones(npts, 1));

%coordinates describing a sphere
[x_sph, y_sph, z_sph] = sphere();

%plot the sphere
subplot(1,2,1);
sp = surf(x_sph, y_sph, z_sph);
set(sp, 'facealpha', 0.5); 
colormap(gray);

%plot (phi, theta)
hold on;
dot_plot = plot3(x, y, z, 'r.');
hold off;
view(150, 25);
axis equal;
set(dot_plot, 'markersize', 9);
title('Uniform theta; non-uniform sphere');

%plot the sphere in another subpot
subplot(1,2,2);
sp = surf(x_sph, y_sph, z_sph);
set(sp, 'facealpha', 0.5); 
colormap(gray);

%plot (phi, theta_unif)
hold on;
dot_plot = plot3(x_unif, y_unif, z_unif, 'r.');
hold off;
view(150, 25);
axis equal;
set(dot_plot, 'markersize', 9);
title('Non-uniform theta; uniform sphere');

%adjust the figure window size
set(gcf, 'pos', [20, 200, 1100, 500]);

%plot the frequencies
figure();
nbins = 30; %number of bins to use
subplot(1,2,1);
hist(theta, nbins);
title('Uniform theta sampling');
set(gca, 'xlim', [0, pi/2]);
xlabel('angle (rad)');
ylabel('counts');
subplot(1,2,2);
hist(theta_unif, nbins);
title('Inverse theta sampling');
set(gca, 'xlim', [0, pi/2]);
xlabel('angle (rad)');
ylabel('counts');
