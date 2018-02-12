function [onspkind]=plotoptoraster(spiketimes,LEDons,LEDoffs,subplots)
subplot(subplots(1),subplots(2),subplots(3:end));
pulselength=mean(LEDoffs-LEDons); %0.003 usually

LEDons(length(LEDons)+1)=LEDons(length(LEDons))+1;
patch([0 pulselength pulselength 0],[0 0 length(LEDoffs) length(LEDoffs)],'cyan','FaceAlpha',0.2,'LineStyle','none');
hold on

onspkind=[];
for trial=1:length(LEDoffs); % find the index of spikes during light pulses
    onspktimes=spiketimes(spiketimes<LEDoffs(trial) & spiketimes>LEDons(trial));
    trialonspkind=find(spiketimes<LEDoffs(trial)+0.002 & spiketimes>LEDons(trial)); % find spikes during the light and next 2 ms
    prespktimes=spiketimes(spiketimes<LEDons(trial) & spiketimes>(LEDons(trial)-0.05));
    postspktimes=spiketimes(spiketimes<(LEDoffs(trial)+0.1) & spiketimes>LEDoffs(trial));

    % plot the post light spikes
    trials=(ones(length(postspktimes),1))*trial;
    for ii = 1:length(postspktimes) % for every spike
        line([postspktimes(ii)-LEDons(trial) postspktimes(ii)-LEDons(trial)],[trials(ii)-1 trials(ii)],'Color','k');
    end
    % plot the pre light spikes
    trials=(ones(length(prespktimes),1))*trial;
    for ii=1:length(prespktimes);
        line([prespktimes(ii)-LEDons(trial) prespktimes(ii)-LEDons(trial)],[trials(ii)-1 trials(ii)],'Color','k');
    end
    
    trials=(ones(length(onspktimes),1))*trial;
    for ii = 1:length(onspktimes) % for every spike
        line([onspktimes(ii)-LEDons(trial) onspktimes(ii)-LEDons(trial)],[trials(ii)-1 trials(ii)],'Color','r');
    end
    onspkind=[onspkind; trialonspkind];    
end

axis([-0.05 0.1 0 length(LEDoffs)]);
xlabel('Time (s)');
ylabel('Trial');
%set(gca, 'FontSize', 6)

