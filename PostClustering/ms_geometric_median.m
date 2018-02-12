function [mm,changes]=ms_geometric_median(X,num_iterations)
%MS_GEOMETRIC_MEDIAN - estimate the geometric median of a collection of
%points in n dimensions using a fixed number of iterations of the
%weiszfeld algorithm
%
% Useful for extracting a template or representative waveform from a
% collection of features derived from event clips in a single cluster.
%
% Syntax:  [mm,changes]=ms_geometric_median(X,num_iterations)
%
% Inputs:
%    X - nxL array of points in n dimensions
%    num_iterations - fixed number of iterations for the weiszfeld
%    algorithm
%
% Outputs:
%    mm - nx1 vector, the approximate geometric median
%    changes - optional output for convergence monitoring
%
% Other m-files required: none
%
% See also: mscmd_features, ms_event_features

% Author: Jeremy Magland
% Jan 2015; Last revision: 15-Feb-2106
if nargin<2, num_iterations=10; end;

[M,N]=size(X);
if (N==1) 
    mm=X;
    changes=[0];
    return;
end;
weights=ones(1,N);
changes=[];
for it=1:num_iterations
    weights=weights/sum(weights);
    mm=X*weights';
    if (it>1)
        changes=[changes,sqrt(sum((mm-mm_old).^2))];
    end;
    mm_old=mm;
    diffs=X-repmat(mm,1,N);
    weights=sqrt(sum(diffs.^2,1));
    inds=find(weights~=0);
    weights(inds)=1./weights(inds);
end;

end

