%%% Steven Huang<s.huang@ed.ac.uk> %%% Warning this may all be incorrect
%%% see line 11
% sparsity is calculated based on what was described in Jung et. al. 1994 J Neurosci.
function info = sparsity(frmap,posmap)
ind = ~isnan(posmap)&~isnan(frmap);

frmap = frmap(ind);
posmap = posmap(ind);

total_bins = length(posmap);

pi = 1/total_bins; % for simplicity, authors assumed uniform distribution for the exploration. do they?
frmap = reshape(frmap, [], 1);
info = (sum(frmap .* pi))^2 / sum(frmap.^2 .* pi);
