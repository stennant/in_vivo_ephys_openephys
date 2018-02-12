function plotspikehist(spiketimes,total_time,subplots)
width=5; % what bin width to use - in seconds or whatever units spiketimes is in
[N,edges] = histcounts(spiketimes,'BinWidth',width);
centers = (edges(1:end-1) + edges(2:end))/2;
N=N./width;
subplot(subplots(1),subplots(2),subplots(3:end));
bar(centers, N,1,'k')
ylabel('FiringRate(Hz)');
xlabel('Time (s)')
axis([min(spiketimes) max(spiketimes) 0 max(N)]);
totalspikes=length(spiketimes);
meanFR=totalspikes/total_time;
h = title(sprintf('Total Spikes =  %.f Mean FR= %.f Hz',totalspikes,meanFR));
%% optional stylistic things
%set(gca,'YAxisLocation','right');
% ylabel('FontSize', 6);
% xlabel('FontSize', 6)
% set(gca,'LineWidth',2,'layer','top')