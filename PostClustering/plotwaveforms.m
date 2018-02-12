function [max_amp,max_channel,spk_width,ori]=plotwaveforms(waveforms,subplots,ori)
% waveforms:  4*40*number_of_waveforms matrix of waveforms
% subplots: location to plot output in format 
% [numberofrows numberofcolumns [plot locations x 4]]
% optional input specifying orientation of depolarisation -1 or +1

rand_index=rand(50,1);
rand_index = ceil(rand_index*length(waveforms(1,1,:)));
mean1=mean(waveforms,3);
std1=std(waveforms,0,3);
maxwav=mean1+(std1.*2);
minwav=mean1-(std1.*2);
maxwav=max(max(maxwav));
minwav=min(min(minwav));
if ~exist('ori','var') % use assigned waveform orientation if given
if abs(maxwav)<abs(minwav); ori=-1;else; ori=1; end % find sign of spikes
end
wavtime=-300:100/3:1000; % x-axis labels

for i=1:4
subplot(subplots(1),subplots(2),subplots(i+2))
plot(wavtime,squeeze(waveforms(i,:,rand_index)),'k','Color',[0.5 0.5 0.5]);
hold on;
plot(wavtime,squeeze(mean1(i,:))+squeeze(std1(i,:)),'r--','LineWidth',1);
plot(wavtime,squeeze(mean1(i,:))-squeeze(std1(i,:)),'r--','LineWidth',1);
plot(wavtime,squeeze(mean1(i,:)),'r','LineWidth',1);
axis([-300 1000 minwav maxwav]);
set(gca, 'FontSize', 6);
if ori==-1; set(gca, 'YDir','reverse'); end
handle = get(gca, 'ylabel');
set(handle, 'FontSize', 6);
end

max_amp=max(max(mean1.*ori)); % find peak amplitude
[max_channel,peaktime]=find(mean1==ori*max_amp); % channel of max amplitude
meanwave=mean1(max_channel,peaktime:end)*ori;
spk_width=find(meanwave==min(meanwave))-1; % peak-trough (samples) of mean waveform

