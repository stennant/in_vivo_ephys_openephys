function [LEDons,LEDoffs,LEDtime]=GetOpto

%% get LED data
try
    [LED, LEDtime, ~] = load_open_ephys_data('105_CH22_0.continuous');
catch
    try
    [LED, LEDtime, ~] = load_open_ephys_data('105_ch22_0.continuous');
    catch
    [LED, LEDtime, ~] = load_open_ephys_data('100_ADC3.continuous');
    end
end

LED=LED-min(LED);
%% identification of LED pulses
onindex=LED>0.1;
flip=diff(onindex);
mintimes=find(flip==1); mintimes=mintimes+1;
maxtimes=find(flip==-1);

if maxtimes(1)<mintimes(1); maxtimes(1)=[];end % correct for light on at start of session
if length(mintimes)>length(maxtimes); mintimes(length(mintimes))=[];end %correct for light on at end of session


disp(strcat('there are_ ', num2str(length(mintimes)), ' light events'));
%% discard theta pulses
interval=maxtimes-mintimes;
index=zeros(size(interval));
index(interval>90)=1;
index(interval<89)=1;
mintimes(index==1)=[];
maxtimes(index==1)=[];

%% calculate times of pulses
LEDons=LEDtime(mintimes);
LEDoffs=LEDtime(maxtimes);
disp(strcat('there are_ ', num2str(length(mintimes)), ' identification pulses'));
