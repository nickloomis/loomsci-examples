function ret_val = halftone_dict(dict, operation, varargin)
% Manage a halftone dictionary.
%
% Inputs:
%  dict: dictionary of halftones to perform operations on; if dict is
%    empty, a new dictionary will be created.
%  operation: what operation to perform on the dictionary (see below). note
%    that punctuation and capitalization don't matter for operation names.
%  other inputs may follow, depending on the operation.
%
% Operations:
%  'add': append a new image to the dictionary. this will calculate all
%    values needed to represent the halftone and store them with the entry.
%    the third function argument should be an image as a uint8.
%  'delete': removes an entry from the dictionary. specify the index of the
%    halftone to delete as the third input.
%  'mean luminance': return a list of the average luminance values for each
%    halftone pattern, in the same order as the halftone appears in the
%    dictionary. no third function argument is used.
%  'get halftone': finds the halftone which is the closest match to the
%    luminance in the image patch in the third function argument. the image
%    patch is expected to be uint8, and can be either two-channel or
%    three-channel. the halftone image is returned.
%  'get halftone index': finds the halftone in the dictionary which is the
%    closest luminance match to an image patch supplied in the third
%    function argument (see 'get halftone'). instead of returning the
%    halftone, this will return the index of the halftone in the
%    dictionary.
%  'get halftone NxN': finds the halftone in the dictionary which is
%    the closest spatial and luminance match at the scale of NxN pixels.
%    the image patch is supplied in the third function argument, and the
%    number of pixels, N, is in the fourth argument. the halftone image is
%    returned.
%  'get halftone index NxN': finds the halftone in the dictionary which is
%    the closest spatial and luminance match at the scale of NxN pixels.
%    the image patch is supplied in the third function argument, and the
%    number of pixels, N, is in the fourth argument. this will return the
%    index of the halftone in the dictionary.
%  'get halftone sRGB': same as 'get halftone', but the mean of the
%    image patch's sRGB values is used to match the mean value of the
%    halftone. this is primarily for experimentation, or for doing matching
%    on images which are not in sRGB space (but are in some other linear
%    space).
%
% Change log:
%  2015/09/04 -- original version written; nloomis@
%  2015/09/07 -- added matching in sRGB for experimentation; nloomis@
%  2015/09/12 -- added NxN halftone matching; nloomis@
%

if isempty(dict)
    dict = {};
end

switch short_name(operation)
    case 'add'
        %varagin{1}: image to use as a halftone; will be added to the dict
        %returns a dict with the pattern appended to it
        ret_val = add_to_halftone_dict(dict, varargin{1});
    case 'delete'
        %varargin{1}: index of the halftone to remove
        %returns a dict without the halftone
        ret_val = remove_halftone(dict, varargin{1});
    case 'meanluminance'
        %returns a list of the luminance for each halftone in the dict
        ret_val = get_mean_luminance(dict);
    case 'gethalftone'
        %varargin{1}: image patch to match against a halftone
        %returns the halftone image with the closest luminance match
        ret_val = get_nearest_halftone(dict, varargin{1});
    case 'gethalftoneindex'
        %varagin{1}: image patch to match against a halftone
        %returns the index in the dict with the closest luminance match
        ret_val = get_nearest_halftone_idx(dict, varargin{1});
    case 'gethalftonenxn'
        %varagin{1}: image patch to match against a halftone
        %varagin{2}: sub-sampling size (number of pixels)
        %returns the halftone with the closest luminance + spatial match
        ret_val = get_nearest_halftone_NxN(dict, ...
            varargin{1}, varargin{2});
    case 'gethalftoneindexnxn'
        %varagin{1}: image patch to match against a halftone
        %varagin{2}: sub-sampling size (number of pixels)
        %returns the index in the dict with the closest luminance + spatial
        %match
        ret_val = get_nearest_halftone_idx_NxN(dict, ...
            varargin{1}, varargin{2});
    case 'gethalftonesrgb'
        %varargin{1}: image patch to match against a halftone
        %returns the halftone image with the closest mean(srgb_img(:))
        %match
        %note: using the mean srgb value doesn't work well for halftones,
        %but this case is here for you to experiment with, intrepid people
        %of the interwebs!
        ret_val = get_nearest_halftone_srgb(dict, varargin{1});
    %case to write: get nearest 2x2, 3x3, etc halftone
    %case to write: display all halftones in the dict
    otherwise
        error('halftone_dict:UnknownOperation', ...
            ['The requested operation, ', operation, ', is not known.']);
end

%
% sub-functions
%

function dict = add_to_halftone_dict(dict, pattern)
%compute useful metrics on the pattern and add it to the dictionary
entry.pattern = pattern;
entry.size = size(pattern);
entry.mean = mean(pattern(:));
lum_img = luminance_image(pattern);
entry.total_lum = sum(lum_img(:));
entry.mean_lum = mean(lum_img(:)); %same as lum1x1
for N = 2:8
    entry.(lumNxN_field_name(N)) = imresize(lum_img, [N, N]);
end
%note: the lumNxN structures are for use when you're trying to match both
%luminance and spatial structure
dict_count = numel(dict);
dict{dict_count + 1} = entry;

function field_name = lumNxN_field_name(N)
%name for the field that an N x N downsampled luminance is saved into
field_name = ['lum', num2str(N), 'x', num2str(N)];

function dict = remove_halftone(dict, idx)
%removes a specific halftone entry from the dictionary (by index)
all_idx = 1:numel(dict);
all_idx(idx) = [];
dict = {dict{all_idx}};

function the_list = get_property_list(dict, field_name)
%builds an in-order list of the values of a property
dict_count = numel(dict);
the_list = zeros(dict_count, 1);
for j = 1:dict_count
    the_list(j) = dict{j}.(field_name);
end

function mean_lum_list = get_mean_luminance(dict)
%return a vector of the mean luminances of each pattern
mean_lum_list = get_property_list(dict, 'mean_lum');

function lum_img = luminance_image(srgb_img)
%returns a luminance image from an srgb input
lin_img = inverse_compand(srgb_img);
if size(lin_img, 3) == 3
    lum_img = rgb2gray(lin_img);
else
    lum_img = lin_img;
end

function pattern = get_nearest_halftone(dict, srgb_img)
%find the pattern whose luminance most closely matches that of the supplied
%image; return the pattern itself
pattern_idx = get_nearest_halftone_idx(dict, srgb_img);
pattern = dict{pattern_idx}.pattern;

function pattern_idx = get_nearest_halftone_idx(dict, srgb_img)
%find the pattern whose luminance most closely matches that of the supplied
%image; return the index of the pattern
lum_img = luminance_image(srgb_img);
mean_lum_img = mean(lum_img(:)); %mean luminance of the image patch
mean_lum_list = halftone_dict(dict, 'mean luminance');
lum_err = abs(mean_lum_list - mean_lum_img);
[~, pattern_idx] = min(lum_err);

function pattern = get_nearest_halftone_NxN(dict, srgb_img, N)
%finds the pattern whose luminance is the closest match to the supplied
%image patch when both are downsampled to size (N x N); returns the 
%halftone patch.
pattern_idx = get_nearest_halftone_idx_NxN(dict, srgb_img, N);
pattern = dict{pattern_idx}.pattern;

function pattern_idx = get_nearest_halftone_idx_NxN(dict, srgb_img, N)
%finds the pattern whose luminance is the closest match to the supplied
%image patch when both are downsampled to size (N x N).
%metric: combines absolute luminance error and the mean dot product between
%the image patch and the halftone patch. could be explored/optimized
%futher!
lum_img = imresize(luminance_image(srgb_img), [N, N]);
field_name = lumNxN_field_name(N);
ndict = numel(dict);
raw_similarity = zeros(ndict, 1);
for j = 1:ndict
    raw_similarity(j) = dot(lum_img(:), dict{j}.(field_name)(:));
end
mean_lum_list = get_mean_luminance(dict);
lum_err = abs(mean_lum_list - mean(lum_img(:)));
shape_sim = raw_similarity ./ (N^2 * mean_lum_list);
shape_sim(isnan(shape_sim)) = 0;
similarity = lum_err - shape_sim;
[~, pattern_idx] = min(similarity);

function pattern_idx = get_nearest_halftone_idx_srgb(dict, srgb_img)
%find the pattern whose mean srgb value most closely matches that of 
%the supplied image; return the index of the pattern
mean_img = mean(srgb_img(:));
means = get_property_list(dict, 'mean');
mean_err = abs(means - mean_img);
[~, pattern_idx] = min(mean_err);

function pattern = get_nearest_halftone_srgb(dict, srgb_img)
%find the pattern whose mean srgb value most closely matches that of 
%the supplied image; return the halftone pattern
pattern_idx = get_nearest_halftone_idx_srgb(dict, srgb_img);
pattern = dict{pattern_idx}.pattern;