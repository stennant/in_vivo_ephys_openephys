function [lightscore_p,lightscore_I,lightlatency,percentresponse]=plotoptohist(LEDons,LEDoffs,cluspiketimes,subplots);
                windowstart=-0.01; %start of histogram relative to light onset in seconds
                windowend=0.02;    %end of histogram relative to light onset in seconds
                testwindow=0.01; % test window for statistical test of light responsiveness in seconds
                basestart=0.8; % window start for baseline for statistical test of light responsiveness
                srate=0.0002; % sampling rate for discretized binary raster 
                binspktimes=[];
                pulselength=mean(LEDoffs-LEDons);
                response=NaN(1,length(LEDons));
%find spiketimes relative to light pulse
for i=1:length(LEDons)
    trialspktimes=cluspiketimes(cluspiketimes>LEDons(i)+windowstart & cluspiketimes<LEDons(i)+windowend);
    trialspktimes=trialspktimes-LEDons(i);
    binspktimes=[binspktimes; trialspktimes];
    
    testspktimes{i}=cluspiketimes(cluspiketimes>=LEDons(i) & cluspiketimes<LEDons(i)+testwindow)-LEDons(i);
    basespktimes{i}=cluspiketimes(cluspiketimes>=LEDons(i)-basestart & cluspiketimes<LEDons(i)-testwindow)-(LEDons(i)-basestart);
    
    responsespikes=cluspiketimes(cluspiketimes>LEDons(i) & cluspiketimes<LEDons(i)+0.005);
    response(i)=length(responsespikes);
end
% make histogram
width=0.0005;
edges=windowstart:width:windowend;
[N,edges] = histcounts(binspktimes,edges);
centers = (edges(1:end-1) + edges(2:end))/2;
N=N./length(LEDons);
subplot(subplots(1),subplots(2),subplots(3:end));
patch([0 pulselength pulselength 0],[0 0 max(N)+0.05 max(N)+0.05],'cyan','FaceAlpha',0.2,'LineStyle','none');
hold on
bar(centers, N,1,'k')
ylabel('Spikes/Trial');
xlabel('Time (s)')
axis([windowstart windowend 0 max(N)+0.05]);
totalspikes=length(binspktimes);

%% calculate output variables
spt_baseline=zeros(length(LEDons),basestart/srate); % create discretized binary raster baseline
spt_test=zeros(length(LEDons),testwindow/srate);    % create discretized binary raster test
for i=1:length(LEDons)
if basespktimes{i}>0; ind=round(basespktimes{i}/srate); ind=ind(ind>0); spt_baseline(i,ind)=1; end
if testspktimes{i}>0; ind=round(testspktimes{i}/srate); ind=ind(ind>0); spt_test(i,ind)=1; end
end
[lightscore_p,lightscore_I] = SALT(spt_baseline,spt_test,srate,testwindow); % from Kvitsiani et al 2013

N=N(centers>0);
centers=centers(centers>0);
lightlatency=centers(N==max(N)); lightlatency=lightlatency(1);
percentresponse=sum(response>0)/length(response)*100;
title({sprintf('SALT p =  %.3f , SALT statistic = %.3f',lightscore_p,lightscore_I),sprintf('Mode latency =  %.f ms Light response = %.f %% trials',lightlatency*1000,percentresponse)});
