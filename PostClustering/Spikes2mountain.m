%% function spikes2mountain (takes OpenEphys .spikes data and converts to mda format)
%% requires the following scripts
% load_open_ephys_data.m 
% writemda.m

srate=30000; % sampling rate of data
numsamples=40; % number of samples per waveform snippet

tic;
for tetrode=1:4; %1:4
%% get data 
fname=['TT' num2str(tetrode)-1 '.spikes'];

[X, times,~] = load_open_ephys_data(fname); % following this line the array will have size nspikes x numsamples x numchannels
X=-X;
%% find peak times and channels
[peaks,i] = max(X,[],2); % i is the column index of the peak of each channel (which sample of waveform is highest on each channel)
[maxpeak,j] =max(peaks,[],3); % j is the Zdimension index of the peak across channel peaks (which channel is highest 1-4)
% use j to index i, find the index of the peak of each waveform across channels
j = reshape(j,1,size(j,1));
i = reshape(i,4,size(i,1));
peak_inds =  zeros(1,size(i,2));
for q = 1:size(i,2)
    peak_inds(q) = i(j(q),q);
end

%% add padding and concatenate to 2d
event_times=peak_inds+(0:size(X,1)-1)*2*numsamples;
event_times = int32(event_times);

X=padarray(X,[0,numsamples,0],'post'); %following this line the array will have size nspikes x (2*numsamples) x numchannels
X=permute(X,[2 1 3]); % following this line the array will have size (2*numsamples) x nspikes x numchannels
X=reshape(X,size(X,1)*size(X,2),4); % following this line the array will have size (nspikes*2*numsamples) x numchannels

%% write raw.mda files
disp('Writing raw.mda file. Sorry for the delay')
mdaname=['raw.nt' num2str(tetrode) '.mda'];
writemda(X',mdaname,'int16');
clear X;
mdanamet=['event_times.nt' num2str(tetrode) '.mda'];
writemda(event_times,mdanamet,'int32');
clear event_times
clear peak_inds
%% write timestamps file
increments=0:1/srate:(numsamples-1)/srate;
T=times+increments;
T=T*srate;
T=[T zeros(size(T))];
T=reshape(T',1,size(T,1)*size(T,2));
disp('Writing timestamps.mda file')
mdaname2=['timestamps.nt' num2str(tetrode) '.mda'];
writemda(T,mdaname2,'float32');
end
toc
