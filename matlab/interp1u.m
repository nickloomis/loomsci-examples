function [yi, idx] = interp1u(x, y, xi, varargin)
% 1D interpolation on the unique values of the input.
%
% Interpolation requires unique values of the independent variable. This
% function finds the unique inputs and uses only those data points for
% interpolation. The interpolation is done through interp1. Additional
% arguments are passed on to interp1 directly.
%
% Inputs:
%  x: independent variable source data
%  y: dependent variable source data
%  xi: vector of where to interpolate the (x,y) data
%  varargin: other variables to pass on to interp1(), such as the
%   interpolation method and extrapolation options.
%
% Outputs:
%  yi: interpolated data points
%  idx: the indices from (x,y) used for interpolation
%
% Change log:
%  2015/09/14 -- rewritten from old code; nloomis@
%

[xu, idx] = unique(x);
yi = interp1(xu, y(idx), xi, varargin{:});
