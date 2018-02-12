function [occh frh] = polar_hist(occ_hds, spk_hds, smooth, angles,sampling_rate)

% a HD of -200 was assigned as a substitute for NaN value
ind = find(occ_hds > -200);
occ_hds = occ_hds(ind);
ind = find(spk_hds > -200);
spk_hds = spk_hds(ind);

for a = 1:length(angles)
  upper = angles(a) + smooth;
  lower = angles(a) - smooth;
	
  overflow = 0;
  s_overflow = 0; 
  if (upper > angles(end)+1)
    upper2 = angles(1) + upper-(angles(end)+1);
    overflow = length(find(spk_hds < upper2));
    s_overflow = length(find(occ_hds < upper2));
  end
      	
  underflow = 0;
  s_underflow = 0;
  if (lower < angles(1))
    lower2 = (angles(end)+1) - (angles(1) - lower);
    underflow = length(find(spk_hds >= lower2));
    s_underflow = length(find(occ_hds >= lower2));
  end
      	
  flow = length(find((spk_hds >= lower).*(spk_hds < upper) == 1));
  s_flow = length(find((occ_hds >= lower).*(occ_hds < upper) == 1));
  spkh(a) = flow + overflow + underflow;
  occh(a) = s_flow + s_overflow + s_underflow;
end

occh = occh/sampling_rate; % each occupancy means 20ms stay is in 20ms
frh = spkh./occh;

