function plotspeed(speed,spkspeed,sampling_rate,speedscore,subplots)
%% makes a firing rate against speed histogram
%% inputs are 
binsize=1; % in m/s
%histogram of speed
[speedcounts,edges1] = histcounts(speed,[floor(min(speed)):binsize:binsize*ceil((ceil(max(speed))-floor(min(speed)))/binsize)]);
%histogram of spkspeeds
[spkcounts,edges2] = histcounts(spkspeed,[floor(min(speed)):binsize:binsize*ceil((ceil(max(speed))-floor(min(speed)))/binsize)]);
%divide one by other
spkrate=spkcounts./speedcounts;
spkrate=spkrate*sampling_rate;
spkrate(speedcounts<sum(speedcounts)*0.005)=NaN; % only include bins accounting for >0.5% of speed data
centres=(edges1(1:end-1) + edges1(2:end))/2; % find the centres of each bin for bar graph
spkrate=spkrate(1:max(find(~isnan(spkrate)))); % trim to useable data
centres=centres(1:max(find(~isnan(spkrate)))); % trim to useable data
%make plot
subplot(subplots(1),subplots(2),subplots(3:end));
bar(centres, spkrate,1,'k')
h = title(sprintf('Speedscore= %.2f',speedscore));
ylabel('FiringRate(Hz)');
xlabel('Speed (cm/s)')
axis([0 max(centres)+binsize/2 floor(min(spkrate)-range(spkrate)/10) ceil(max(spkrate)+range(spkrate)/10)]);

