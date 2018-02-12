function [postb,posx,posy,hd,HDint]= GetPosSyncedCorr(pname)
if ~exist('pname','var')
pname='*.csv';
pname=dir(pname);
try
pname=pname(posind).name;
disp(pname);
catch
    pname=[];
    disp('no pos file present')
end
end
%% Get Bonsai data

[post,posx,posy,hd,HDint,light]= readbonsai(pname,440);

%% Get OE Pulse data
try
    [Sync, LEDtime, ~] = load_open_ephys_data('100_ADC1.continuous');
catch
try
    [Sync, LEDtime, ~] = load_open_ephys_data('105_CH20_0.continuous');
catch
    [Sync, LEDtime, ~] = load_open_ephys_data('105_ch20_0.continuous');
end
end

%% find the average offset by crosscorrelating the two signals
disp('cross correlating');
FsB=1/mean(diff(post)); % avg sampling rate Bonsai
FsO=1/mean(diff(LEDtime)); % avg sampling rate OE
[P,Q]=rat(FsB/FsO); % rational fraction of sampling rates
downsampleOE=resample(Sync,P,Q); % create downsampled OE data

[C,lag]=xcorr(light,downsampleOE); % cross correlate the two signals
offset=lag(C==max(C))/FsB; % find lag of best correlation

postb=post-min(post)+min(LEDtime)-offset; % correct post to match openephys time

%% plot to check alignment
% plot(postb,light)
% hold on
% scatter(OEpulse,ones(size(OEpulse))*5000)


