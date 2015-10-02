function M = color_matrix(matrix_name)
%
% Returns the color conversion matrix for the named transform. The
% conversion matrix can be used with apply_color_matrix. This function
% differs from Matlab's makecform in a number of ways:
%  - it's simpler, and doesn't have all the bells-and-whistles
%  - only linear transforms are avaiable
%  - it's still getting expanded as new transforms are needed
%  - there are some transforms that makecform doesn't have available as
%    single-step transformations
%  - the image processing toolbox isn't required
%
% 
% brucelindbloom
% TODO: docstring
% note that rgb expects linear

% Change log:
%  2015/09/21 -- original function written; nloomis@gmail.com
%

%Note: trying to use D50 as the reference when not spec'd

matrix_names = {'rgb2xyz', 'xyz2rgb', ...
    'xyz2lms', 'lms2xyz', ...
    'rgb2lms', 'lms2rgb', ...
    'srgb2xyzd50', 'srgb2xyzd65', ...
    'xyz2lmsvonkries', 'xyz2lmsbradford'};
%TODO: if no inputs, print the list of available matrices to the console
mtype = validatestring(short_name(matrix_name), matrix_names);
%TODO: implement cases for the rest of the matrices, or intelligently
%combine matrices!

switch mtype
    case 'rgb2xyz'
        M = srgb2xyz_d50_matrix();
        
    case 'xyz2rgb'
        M = inv(srgb2xyz_d50_matrix());
        
    case {'xyz2lms', 'xyz2lmsbradford'}
        M = xyz2lms_bradford_matrix();
        
    case 'lms2xyz'
        M = inv(xyz2lms_bradford_matrix());
        
    case 'rgb2lms'
        M = xyz2lms_bradford_matrix() * srgb2xyz_d50_matrix();
        
    case 'lms2rgb'
        M = inv(xyz2lms_bradford_matrix() * srgb2xyz_d50_matrix());
        
    case 'srgb2xyzd50'
        M = srgb2xyz_d50_matrix();
        
    case 'srgb2xyzd65'
        M = srgb2xyz_d65_matrix();
        
    case 'xyz2lmsvonkries'
        M = xyz2lms_vonkries_matrix();
end

function M = srgb2xyz_d65_matrix()
%sRGB's RGB2XYZ matrix, D65 adapted
%source: bruce lindbloom
M = [0.4124564  0.3575761  0.1804375; ...
     0.2126729  0.7151522  0.0721750; ...
     0.0193339  0.1191920  0.9503041];

function M = srgb2xyz_d50_matrix()
%sRGB's RGB2XYZ matrix, D50 adapted using the Bradform transform
%source: bruce lindbloom
M = [0.4360747  0.3850649  0.1430804; ...
     0.2225045  0.7168786  0.0606169; ...
     0.0139322  0.0971045  0.7141733];
 
function M = smpte_c_rgb2xyz_d65_matrix()
%SMPTE-C's RGB2XYZ matrix, D65 adapted
%source: bruce lindbloom
M = [0.3935891  0.3652497  0.1916313; ...
     0.2124132  0.7010437  0.0865432; ...
     0.0187423  0.1119313  0.9581563];

function M = cie_rgb2xyz_d50_matrix()
%CIE's RGB2XYZ matrix, D50 adapted using the Bradform transform
%source: bruce lindbloom
M = [0.4868870  0.3062984  0.1710347; ...
     0.1746583  0.8247541  0.0005877; ...
    -0.0012563  0.0169832  0.8094831];

function M = xyz2lms_bradford_matrix()
%XYZ2LMS transform using the Bradford transform (this is what Adobe uses,
%and is considered the better transform)
%source: bruce lindbloom
M = [0.8951000  0.2664000 -0.1614000; ...
    -0.7502000  1.7135000  0.0367000; ...
     0.0389000 -0.0685000  1.0296000];

function M = xyz2lms_vonkries_matrix()
%XYZ2LMS using the von Kries adaptation matrix; this is one of the original
%transforms (Bradford is generally preferred). here for comparison.
%source: bruce lindbloom
M = [0.4002400  0.7076000 -0.0808100; ...
    -0.2263000  1.1653200  0.0457000; ...
     0.0000000  0.0000000  0.9182200];