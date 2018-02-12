function [r]=calcspeedscore(post,spiketimes,speed);
%calculate speedscore  (need to check that this is correct Jan 2018)

edges(2:length(post))=post(2:end)-diff(post)/2;
edges(1)=post(1)-(post(2)-post(1))/2;
edges(length(post)+1)=post(end)+(post(end)-post(end-1))/2;

[N,~] = histcounts(spiketimes,edges); % N=instantaneous Firing rate
%N=N./mean(diff(post)); % will put FR in Hz
N(isnan(speed))=[];
speed(isnan(speed))=[];
[r,p]=corrcoef(speed,N);
r=r(2);
p=p(2);
