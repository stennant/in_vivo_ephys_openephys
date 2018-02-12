%% PostClusteringClean
%% Tizzy December 2017
%% post-sorting analysis for open-ephys data with bonsai or axona position data
%% that has been sorted with MountainSort
%% it should auto-detect problems with missing mda files, opto files and pos files and skip affected plots

%% Initial Variables
%pname='Tracking_20171216.csv'; %comment out this line if the bonsai name is normal
CreateFolders % creates the /Data and /Figures folders
speedcut=0.5;%cm/second - threshold running speed to count as moving
%pixel_ratio=490; % pixels per m - 1 George Square - need to write this to autodetect
pixel_ratio=440; % pixels per m - 6th Floor HRB 
format='png'; % what format to save the output figures (matlab figure saved anyway)
OpenField=1; % is this an open-field session with 2d position data
Opto=1; % Is this an opto-tagging session?
electrodes=[1 2 3 4]; % set as 0 if using all tetrodes

%% Subplot locations for Figure 2
fig_rows=6; fig_cols=10;
waveplotstile=[1 2 11 12]; %whiteplotstile=[21 22 31 32];

postile=[3 4 13 14]; ratemaptile=[5 6 15 16]; gridcortile=[7 8 17 18]; posmaptile=[9 10 19 20];
postilerun=[23 24 33 34]; ratemaptilerun=[25 26 35 36]; gridcortilerun=[27 28 37 38]; posmaptilerun=[29 30 39 40];
speedtile = [59 60];

rasterplottile=[49 50]; refractoryperiodtile=[47 48]; thetacorrtile=[57 58];
hdpolartile=[21 22 31 32]; %[45 46 55 56];
optotile=[43 44 53 54]; optoplotstile=[41 42 51 52];
optohisttile=[45 46 55 56];

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
%posnameTiz=strcat(animal,num2str(date(6:7)),num2str(date(9:10)));
posnameTiz='R0616';
%% Get Spike Data
if electrodes==0
    [spikeind,tetid,cluid,waveforms,whiteforms] = GetFiring;
else
    [spikeind,tetid,cluid,waveforms,whiteforms] = GetFiring(electrodes);
end

numclu=length(unique(cluid)); % how many clusters are present
numtet=length(unique(tetid)); % how many tetrodes have been analysed
disp(strcat('Found-',num2str(numclu),' clusters, across-',num2str(numtet),' tetrodes' ))

%% Get position data
% this section needs fixing for 
if OpenField==1 % only do this if it's an open field session
    if exist('pname','var')
        [post,posx,posy,hd,HDint]= GetPosSyncedCorr(pname);        
    elseif any(size(dir('Tracking*'),1))%% if it's Klara's tracking file
        pname=dir('Tracking*'); pname=pname.name;
        [post,posx,posy,hd,HDint]= GetPosSyncedCorr(pname);
    elseif any(size(dir(strcat(posnameTiz,'*.csv')),1))%% bonsai George Square
        pname=dir(strcat(posnameTiz,'*.csv')); pname=pname.name;
        [post,posx,posy,hd,HDint]= GetPosSynced(pname);
    elseif any(size(dir('*.POS'),1)) %% if it's the axona position tracking system
        [post,posx,posy,hd,HDint]= GetPosSyncedAxona;
    else %% to pick up errors
        disp('Error: no position data file');
        OpenField=0;
    end
end

if Opto==1 % only do this if it's an opto-tagging session
    %% Get Real-TimeStamps + light pulse data
    try
        [LEDons,LEDoffs,timestamps]=GetOpto;
    catch
        disp('Problem with Opto data. Skipping these plots')
        try
            [~, timestamps, ~] = load_open_ephys_data('105_CH1_0.continuous');
        catch
            [~, timestamps, ~] = load_open_ephys_data('100_CH1.continuous'); 
        end
        Opto=0;
    end
else
    try
        [~, timestamps, ~] = load_open_ephys_data('105_CH1_0.continuous');
    catch
       [~, timestamps, ~] = load_open_ephys_data('100_CH1.continuous'); 
    end
end
%% trim spiking data to the length of the original data
% for some reason the python .continuous reader has an extra 1024 samples
% than the matlab .continuous reader so we need to remove these extra
% samples if the mda file was created using the python openephys reader

tetid(spikeind>length(timestamps))=[];
cluid(spikeind>length(timestamps))=[];
waveforms(:,:,spikeind>length(timestamps))=[];
whiteforms(:,:,spikeind>length(timestamps))=[];
spikeind(spikeind>length(timestamps))=[];
if OpenField==1
%% trim pos data to length of ephys data
posx=posx(post>min(timestamps) & post<max(timestamps));
posy=posy(post>min(timestamps) & post<max(timestamps));
hd=hd(post>min(timestamps) & post<max(timestamps));
HDint=HDint(post>min(timestamps) & post<max(timestamps));
post=post(post>min(timestamps) & post<max(timestamps));
end
%% Get real-time timestamps for each spike
total_time=max(timestamps)-min(timestamps);
spiketimes=timestamps(spikeind); % realtimestamps for each spike
%% Make electrode Cluster separation Plots
% need to decide which features to plot - probably energy
% for i=1:length(unique(tetid))
%     
% end


if OpenField==1 % only do this if it's an open field session
    %% make running position data only
    % filter by running speed
    [runind,speed]=speedfilter(posx,posy,post,speedcut,pixel_ratio); % speed in cm/sec
    posxrun=posx; posxrun(runind==0)=NaN;
    posyrun=posy; posyrun(runind==0)=NaN;
    %% set bins for working out closest position sample
    postboundary=post-[max(diff(post)); diff(post)./2];
    postboundary=[postboundary; max(postboundary)+(max(diff(post))/2)];
    sampling_rate=1/mean(diff(post)); %average position sampling rate. Needed for converting firing rates to Hz
end


%% Make electrode Plots
for i=1:numclu
    figure2=figure;
    set(gcf,'color','white');
    %% get data for this cluster only
    cluspktimes=spiketimes(cluid==i); nspikes=length(cluspktimes); % calculate number of spikes
    tet=tetid(cluid==i);
    if max(tet)==min(tet); tet=max(tet); else; tet=mode(tet); disp('Error, cluster not on one tetrode');end
    cluwaves=waveforms(:,:,cluid==i);
    cluwhites=whiteforms(:,:,cluid==i);
    
    if OpenField==1 % only do this if it's an open field session
        %% find spike positions
        [~,posspk]=histc(cluspktimes,postboundary);
        posspk(posspk==0)=length(post);
        spkx=posx(posspk);
        spky=posy(posspk);
        spkhd=hd(posspk);
        spkxrun=posxrun(posspk);
        spkyrun=posyrun(posspk);
        spkspeed=speed(posspk);
        spkx(cluspktimes>max(post))=NaN; spkx(cluspktimes<min(post))=NaN;
        spky(cluspktimes>max(post))=NaN; spky(cluspktimes<min(post))=NaN;
        spkhd(cluspktimes>max(post))=NaN; spkhd(cluspktimes<min(post))=NaN;
        spkxrun(cluspktimes>max(post))=NaN; spkxrun(cluspktimes<min(post))=NaN;
        spkyrun(cluspktimes>max(post))=NaN; spkyrun(cluspktimes<min(post))=NaN;
        spkspeed(cluspktimes>max(post))=NaN; spkspeed(cluspktimes<min(post))=NaN;
    end
    
    %% make all the subplots
    %% spike plots
    [max_ampwaves,max_channelwaves,spk_widthwaves,ori]=plotwaveforms(cluwaves,[fig_rows fig_cols waveplotstile]);
    %[max_ampwhites,max_channelwhites,spk_widthwhites]=plotwaveforms(cluwhites,[fig_rows fig_cols whiteplotstile]);
    plotspikehist(cluspktimes,total_time,[fig_rows fig_cols rasterplottile]);
    plotspktimeautocor(cluspktimes,10,[fig_rows fig_cols refractoryperiodtile]);
    plotspktimeautocor(cluspktimes,250,[fig_rows fig_cols thetacorrtile]);
    
    %% position plots
    if OpenField==1 % only do this if it's an open field session
        plotposition(posx,posy,spkx,spky,[fig_rows fig_cols postile]);
        [frmap,posmap,skaggs,spars,cohe,max_firing,coverage]=plotratemap(posx,posy,spkx,spky,pixel_ratio,post,[fig_rows fig_cols ratemaptile], posmaptile);
        [grid_score,grid_spacing,field_size,grid_orientation,grid_ellipticity]=plotgrid(frmap,[fig_rows fig_cols gridcortile]);
        plotposition(posxrun,posyrun,spkxrun,spkyrun,[fig_rows fig_cols postilerun]);
        [frmaprun,posmaprun,skaggsrun,sparsrun,coherun,max_firingrun,coveragerun]=plotratemap(posxrun,posyrun,spkxrun,spkyrun,pixel_ratio,post,[fig_rows fig_cols ratemaptilerun],posmaptilerun);
        [grid_scorerun,grid_spacingrun,field_sizerun,grid_orientationrun,grid_ellipticityrun]=plotgrid(frmaprun,[fig_rows fig_cols gridcortilerun]);
        %% hd plot
        [frh_hd,meandir_hd,r_hd]=plothd(hd,spkhd,sampling_rate,[fig_rows fig_cols hdpolartile]);
        %% speed plot
        [speedscore]=calcspeedscore(post,cluspktimes,speed);
        plotspeed(speed,spkspeed,sampling_rate,speedscore,[fig_rows fig_cols speedtile]);
    end
    %% optoplots
    if Opto==1 % only do this if it's an opto-tagging session
        [onspikes]=plotoptoraster(cluspktimes,LEDons,LEDoffs,[fig_rows fig_cols optotile]);
        [lightscore_p,lightscore_I,lightlatency,percentresponse]=plotoptohist(LEDons,LEDoffs,cluspktimes,[fig_rows fig_cols optohisttile]);
        if length(onspikes)>0
            lightwaves=cluwaves(:,:,onspikes);
            [max_amplight,max_channellight,spk_widthlight]=plotwaveforms(lightwaves,[fig_rows fig_cols optoplotstile],ori);
        else
            max_amplight=NaN; max_channellight=NaN; spk_widthlight=NaN;
        end
    end
    %% save plot and store data matrix
    id = [sessionid '-Tetrode-' num2str(tet) '-Cluster-' num2str(i)];
    annotation('textbox', [0.05, 1.0, 1.0, 0], 'string', id);
    saveas(figure2,fullfile('Figures',id),'fig');
    set(gcf,'PaperUnits','centimeters'); 
    set(gcf,'PaperPosition',[0 0 50 30]);
    saveas(figure2,fullfile('Figures',id),format);
    close(figure2);
    if Opto==0; lightscore_p=NaN; lightscore_I=NaN; lightlatency=NaN; percentresponse=NaN; end % fill output data
    if OpenField==0; frh_hd=NaN; meandir_hd=NaN; r_hd=NaN; skaggs=NaN; spars=NaN; cohe=NaN; max_firing=NaN; grid_score=NaN; skaggsrun=NaN; sparsrun=NaN; coherun=NaN; max_firingrun=NaN; grid_scorerun=NaN; end; %fill output data
        
    datamatrix=[tet,i,nspikes,coverage,nspikes/total_time, max_ampwaves, max_channelwaves,spk_widthwaves, max(frh_hd), meandir_hd, r_hd, skaggs,spars,cohe,max_firing,grid_score,skaggsrun,sparsrun,coherun,max_firingrun,grid_scorerun,lightscore_p,lightscore_I,lightlatency,percentresponse];
datasave(i,:)=datamatrix;
end
save('datasave','datasave')
