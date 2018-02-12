function plotspktimeautocor(spiketimes,window,subplots)
width=1;
subplot(subplots(1),subplots(2),subplots(3:end));                   
[corr,tms] = spktimeautocor(spiketimes,width,window*2);
corr=corr/width;
bar(tms,corr,1,'k');
v1 = axis;
axis([tms(1) tms(end) v1(3) v1(4)]);
xlabel('Time Lag (ms)');

%% optional stylistic things
% set(gca,'LineWidth',2,'layer','top');
% set(gca, 'FontSize', 6);
% xlabel('Time Lag (ms)', 'FontSize', 6);