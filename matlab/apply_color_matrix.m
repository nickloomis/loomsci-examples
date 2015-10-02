function cform_img = apply_color_matrix(image, cform)
%
% Use a color transform matrix to convert an image between color spaces.
%
% Inputs:
%  image: a three-channel image to be converted
%  cform: a 3x3 matrix used to convert between two colorspaces.
%
% Outputs:
%  cform_img: a three-channel image after conversion. the data type is the
%   same as the input image.
%
% See also:
%  color_matrix
%
% Change log:
%  2015/09/21 -- original function written, nloomis@gmail.com
%

%reshape the image so that each channel is a row in a matrix
simg = size(image);
abc = reshape(image, [simg(1)*simg(2), 3])';

%apply the transform
abc_prime = cform * abc;

%reshape the results
cform_img = cast(reshape(abc_prime', simg), 'like', image);