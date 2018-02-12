%%% Steven Huang<s.huang@ed.ac.uk> %%%
% spatial coherence is calculated based on what was described in Kubie et. al. 1990 J Neurosci., use Fisher r-Z' transform to normalise the correlation +-1.96 are 95% confidence interval
function info = spatial_coherence(frmap,posmap)

[xsize, ysize] = size(frmap);
neighbour_rates = zeros(xsize, ysize);

for ii=1:xsize
  for jj=1:ysize
    rate_now = frmap(ii, jj);
    if ~isnan(rate_now)
      indices = get_neighbour_indices(ii, jj, xsize, ysize);
      li = size(indices, 1);
      occ_sum = 0;
      for kk=1:li
        occ_rate = posmap(indices(kk,1), indices(kk,2));
        if(~isnan(occ_rate))
          occ_sum = occ_sum + occ_rate;
        end
      end
      avg_rate = 0;
      for kk=1:li
        fr_rate = frmap(indices(kk,1), indices(kk,2));
        occ_rate = posmap(indices(kk,1), indices(kk,2));
        if(~isnan(fr_rate) && ~isnan(occ_rate))
          avg_rate = avg_rate + fr_rate*occ_rate/occ_sum;
        end
      end
      neighbour_rates(ii,jj) = avg_rate;    
    end
  end
end



ind = ~isnan(frmap);

frmap = frmap(ind);
neighbour_rates = neighbour_rates(ind);
cor = corr(frmap, neighbour_rates); % spatial coherence as defined by Kubie et. al. 1990

W=0.5*log((1+cor)/(1-cor)); % fisher r-Z transform into a normal distribution 0f N(0, (sqrt(1/(N-3)))^2), as correlation coefficient is not normally distributed, and thus cannot easily calculate confidence intervals
info =(W-0)/sqrt(1/(length(frmap)-3)); % convert to standard normal distribution

