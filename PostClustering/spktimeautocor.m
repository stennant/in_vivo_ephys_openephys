function [corr,time] = spktimeautocor(spikes,binsize,window)

no_bins = ceil(spikes(length(spikes))*1000);
train = zeros(no_bins,1);
bins = zeros(length(spikes),1);

for spk = 1:length(spikes)
  
  bin = ceil(spikes(spk)*1000);
  train(bin) = train(bin) + 1;
  bins(spk) = bin; 
  
end

counts = zeros(window+1,1);
counted = 0;

for b = 1:length(bins)
  
  bin = bins(b);
  
  if ((bin > window/2+1) && (bin < length(train)-window/2+1))
    
    counts = counts + train(bin-window/2:bin+window/2);
    counted = counted + sum(train(bin-window/2:bin+window/2)) - train(bin);
    
  end
  
end

counts(window/2+1) = 0;
if(max(counts) == 0 && counted == 0)
  counted = 1;
end
corr = counts ./ counted;
time = -window/2:binsize:window/2;

