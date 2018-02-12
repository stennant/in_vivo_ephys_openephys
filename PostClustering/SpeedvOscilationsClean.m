%% Spontaneous Theta Processing
% splits all data into time windows 
% calculates avg speed per bin
% calculates theta and gamma power in each bin
% calculates PSD in each bin
% saves these numbers
% creates plots to show power of gamma at each speed
electrodeoverride=10; % if you want to run on one specific electrode only

%% Initial Variables
CreateFolders % creates the /Data and /Figures folders
format='png'; % what format to save the output figures (matlab figure saved anyway)
axona=0; % is it axona 1 or bonsai 0?
srate=3000;
GSQ=1; % 1= 1GSQ 0=HRB
speedbinsize=0.5; % size of speed bins in m/sec
epochlength=0.5; % size of epoch in seconds

%% automatic dead-channel detection
if exist('dead_channels.txt','file')
    fileID = fopen('dead_channels.txt','r');
    deadchannels = fscanf(fileID,'%f')
else
    deadchannels=0;
end
%% bands for power calculations
T1=4; T2=12; % theta band
LG1=30; LG2=60; % low gamma band
MG1=60; MG2=120; % mid gamma band
HG1=120; HG2=180; % high gamma band
N1=47; N2=53; % notch band
%% don't bother analysing dead channels
electrodes=1:16; % set as 0 if using all tetrodes
for i=1:length(deadchannels)
    electrodes(electrodes==deadchannels(i))=[];
end
if electrodeoverride>0
    electrodes=electrodeoverride;
end
[filenames]=findfilenames('continuous');
filenames=filenames(electrodes);
%% get session name
str = pwd; %full path to this directory
idx = strfind(str,'\') ;
foldername = str(idx(end)+1:end);
idx=strfind(foldername,'_');
try
    animal=foldername(1:idx(1)-1); % if foldername starts with an animal id, find it
    date=foldername(idx(1)+1:idx(2)-1); % find the date from the foldername
catch
    animal='unknown'; %else if no animal id set it to unknown
    date=foldername(1:idx(1)-1); % find the date from the folder name
end
sessionid=strcat(animal,'-', num2str(date));
pname=strcat(animal,num2str(date(6:7)),num2str(date(9:10)));
%% Get position data
if GSQ==1
    if axona==1   % axona tracking
        pixel_ratio=400;
        posrate=50;
        [post,posx,posy,hd,HDint]= GetPosSyncedAxona;
    else % 1 George square bonsai
        pixel_ratio=490; 
        posrate=30;
        pname=strcat(pname,'.csv');
        [post,posx,posy,hd,HDint]= GetPosSynced(pname);
    end
elseif GSQ==0  % HRB
    pixel_ratio=460; 
    posrate=30;
    pname=dir('.csv'); pname=pname.name;
    [post,posx,posy,hd,HDint]= GetPosSyncedCorr(pname);
end

%% calculate instantaneous speed
posrate=1/mean(diff(post));
speed=sqrt(diff(posx).^2+diff(posy).^2); % create instantaneous speed
speed=speed/pixel_ratio*100*posrate;
speedt=post(1:end-1)+(diff(post)./2); %create times for instantaneous speed
% %%plot position data by hd
% figure;
% scatter(posx,posy,50,hd,'.'); hold on;
% colormap('JET');
%% plot 
% figure
% scatter(posx(2:end),posy(2:end),50,speed,'.'); hold on;
% colormap('JET');
% colorbar;

% get time data
[~, LFPtime, ~] = load_open_ephys_data(char(filenames(1)));
if srate==3000
    LFPtime=decimate(LFPtime,10,'fir');
else
    srate=30000;
end
% cut time data to length of pos data
LFPtime2=LFPtime(LFPtime>post(1) & LFPtime<post(end));
%% split time data into epochs
numepochs=floor(length(LFPtime2)/round(epochlength*srate)); % number of epochs
LFPtime2=LFPtime2(1:(round(epochlength*srate)*numepochs));
LFPtime2=reshape(LFPtime2,[round(epochlength*srate) numepochs]);

%% split position data into epochs
for i=1:numepochs
    epochspeeds=speed(speedt>LFPtime2(1,i) & speedt<LFPtime2(end,i));
    epochspeed(i)=mean(epochspeeds);
    epochmedianspeed(i)=median(epochspeeds);
    epochmaxspeed(i)=max(epochspeeds);
%     epochposts=speedt(speedt>LFPtime2(1,i) & speedt<LFPtime2(end,i));
%     epochspeedt(i)=mean(epochposts);
end

%% calculate epoch behaviour properties - speed, acceleration, 

%% loop through all LFP files 
for f=1:length(filenames)
% open LFP file
[LFP, ~, ~] = load_open_ephys_data(char(filenames(f)));

if srate==3000
    LFP=decimate(LFP,10,'fir'); % downsample LFP data
else
    srate=30000;
end
% cut data to length of time 
LFP=LFP(LFPtime>=LFPtime2(1) & LFPtime<=LFPtime2(end));

LFPsave=LFP;
% split LFP data into bins - LFP array is 900*numepochs in size
LFP=reshape(LFP,[round(epochlength*srate) numepochs]);

PSDepoch=NaN(numepochs,400);
thetapower=NaN(numepochs,1); midgammapower=NaN(numepochs,1); highgammapower=NaN(numepochs,1); lowgammapower=NaN(numepochs,1); notchpower=NaN(numepochs,1);
for i=1:numepochs
 % calculate the bandpower at relevant frequencies per epoch   
    thetapower(i)=bandpower(LFP(:,i),srate,[T1 T2]);
    midgammapower(i)=bandpower(LFP(:,i),srate,[MG1 MG2]);
    highgammapower(i)=bandpower(LFP(:,i),srate,[HG1 HG2]);
    lowgammapower(i)=bandpower(LFP(:,i),srate,[LG1 LG2]);
    notchpower(i)=bandpower(LFP(:,i),srate,[N1 N2]);

% also the PSD for each epoch

        [Pxx,F] = pwelch(LFP(:,i),[],[],0.5:0.5:200,srate);
        PSDepoch(i,:)=Pxx;
end


%% Scatter plots, speed v bandpower
figure;
scatter(epochspeed,thetapower,100,midgammapower,'.');
figure;
scatter(epochspeed,midgammapower,100,thetapower,'.');
figure;
scatter(epochspeed,highgammapower,100,thetapower,'.');

%% sort data by speed of epoch
[~,sorter]=sort(epochmedianspeed);
sortedspeed=epochspeed(sorter);
sortedPSD=PSDepoch(sorter,:);
LFPreshape=LFP(:,sorter);
LFPreshape=reshape(LFPreshape,[1,size(LFP,1)*size(LFP,2)]);
%% PSD per epoch
figure;
h=pcolor(log(PSDepoch)');
set(h, 'EdgeColor', 'none');
colormap('JET');
hold on
scatter(1:length(epochspeed),epochspeed,'.k')
%% PSD per epoch sorted by speed of epoch
figure
h=pcolor(log(sortedPSD)');
set(h, 'EdgeColor', 'none');
colormap('JET');
hold on;
scatter(1:length(sortedspeed),sortedspeed,'.k');
%% spectrogram
figure;
[~,~,~,PowSpDen]=spectrogram(LFPsave,6000,0,[],srate,'yaxis');
spectrogram(LFPsave,floor(length(LFPsave)/length(epochspeed)),0,[],srate,'yaxis');
 ylim([0 0.2]);
 caxis([0 10*log10(abs(max(max(PowSpDen))))*(2/3)]);
colormap('JET');
hold on;
scatter(1:length(sortedspeed),sortedspeed,'.k');
%% spectrogram sorted by speed of epoch
figure;
[~,~,~,PowSpDen]=spectrogram(LFPreshape,6000,0,[],srate,'yaxis');
spectrogram(LFPreshape,floor(length(LFPreshape)/length(epochspeed)),0,[],srate,'yaxis');
 ylim([0 0.2]);
 caxis([0 10*log10(abs(max(max(PowSpDen))))*(2/3)]);
colormap('JET');
hold on;
scatter(1:length(sortedspeed),sortedspeed,'.k');
end

