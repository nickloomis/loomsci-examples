function M = mandelbrot(cr, ci, maxiter)
%
% Usage: M = mandelbrot(cr, ci,, maxiter)
%
% Computes the Mandelbrot set for a series of initial points. 
%
% The Mandelbrot set is defined by the equation
%
%   Z_{n+1} = Z_{n}^2 + C
%
% where C is a complex-valued constant and Z_{0} = C. The set is
% traditionally formed by iteratively computing Z_{n+1} and checking to see
% if abs(Z_{n+1}) remains bounded forever or becomes infinitely large (aka,
% "escapes" the bound). The number of iterations before Z_{n} escapes is
% recorded.
%
% The Mandelbrot set is traditionally displayed as a 2D map: the grid
% points are the real and imaginary components of C, and the map value is
% the number of iterations for Z_{n} to escape. The horizontal axis is the
% real component and the vertical axis is the imaginary component. (In
% other words, a map of the iterations given a region of the complex plane
% used for initial seeds.)
%
% Inputs:
%  cr: vector of the real-valued parts of C
%  ci: vector of the imaginary-valued parts of C
%
%    Note: cr and ci are used with a meshgrid, [Cr,Ci] = meshgrid(cr,ci), to
%    form a 2D map of C values with those real and imaginary parts.
%
%  maxiter: maximum number of iterations to try before deciding that Z_{n}
%      remains bounded (the "bail-out") [defaults to 200]
%
% Output:
%  M: map of the number of iterations required before the Z_{n} sequence
%      escapes to infinity. The map is the same size as C and represents
%      each of the C values used to seed the Z_{n} sequences. It has
%      numel(cr) columns and numel(ci) rows. Use imagesc(cr,ci,M) to
%      display the map as an image.
%
% Example usage:
%
% cr = linspace(-2,1,600);
% ci = linspace(-1,1,400);
% M = mandelbrot(cr, ci, 1200);
% imagesc(cr, ci, M);
% colormap(hot); colorbar;
% xlabel('\Re(c)');
% ylabel('\Im(c)');
%

% Nick Loomis, nloomis@gmail.com
% 
% Change log:
%  2013/12/31 -- original function written (NL)
%


%constants
escapevalue = 1e42;

%default arguments
if nargin<3
    maxiter = 200;
end

%form the grid of initial points
[Cr, Ci] = meshgrid(cr,ci);
C = Cr + 1i*Ci;

%zero-out the storage space
M = zeros(size(Cr));

%step through the initial points
for m=1:numel(M)
    
    znp1 = C(m); %set the initial z value
    itercount = 0; %reset the number of iterations
    
    %iterate until the z value escapes to "infinity" or there's been enough
    %iterations to be reasonably happy that the z remains bounded
    while (abs(znp1)<escapevalue) && (itercount<maxiter)
        znp1 = znp1^2 + C(m); %the mandelbrot iterate
        itercount = itercount + 1; %increase the iteration count
    end
    
    %record how many iterations were required before the z escaped to
    %infinity
    if itercount~=maxiter
        M(m) = itercount;
    end
    
end

%done.

