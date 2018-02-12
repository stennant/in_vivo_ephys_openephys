function [postnew,posx,posy,hd,HDint]= GetPosSynced(pname)
%% get position data
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

[post,posx,posy,hd,HDint,light]= readbonsai(pname,490);

%% Get Pulse data
[Ons,Offs]=GetSync;

%% get sync times from video
stdevlight=std(light); % threshold is 2stdeviations above the median intensity
threshold=median(light)+2*stdevlight;
%threshold=(max(light)-(median(light)/10)*9);
onindexS=light>threshold; %need to work out a way to automatically set this threshold
flipS=diff(onindexS);
mintimes=find(flipS==1); mintimes=mintimes+1;
maxtimes=find(flipS==-1);

%get rid of offs before ons and trim both matrices to the same length
if maxtimes(1)<mintimes(1); maxtimes(1)=[]; end
if length(maxtimes)<length(mintimes); mintimes=mintimes(1:length(maxtimes));end
% get rid of pulses that aren't the right length
gap=maxtimes-mintimes;
maxtimes(gap>4)=[]; mintimes(gap>4)=[];

% get rid of pulses that aren't the right intensity
midtimes=round((mintimes+maxtimes)./2);
variability = (median(light(midtimes))-mean(light))*0.2;
threshold2=median(light(midtimes))+variability;
maxtimes(light(midtimes)>threshold2)=[]; mintimes(light(midtimes)>threshold2)=[];
threshold2=median(light(midtimes))-variability;
maxtimes(light(midtimes)<threshold2)=[]; mintimes(light(midtimes)<threshold2)=[];

% find timepoints of ons+offs
OnL=post(mintimes);
OffL=post(maxtimes);
L=round((mintimes+maxtimes)./2);
W=diff(L);

OEpulse=(Ons+Offs)./2;
BZpulse=(OnL+OffL)./2;

%% check if there is a significant lag in one of the systems
%try
BZnorm=BZpulse-min(BZpulse)+min(OEpulse);
lag=OEpulse-BZnorm;

if max(abs(lag))>2/30
    cprintf('red','You have a significant lag between systems');
    maxlag=max(abs(lag))
    postnew = post+(min(OEpulse)-post(L(1)));
    lag=OEpulse-postnew(L);
    postmorph=postnew;
    for j=2:length(L)
        inc=lag(j)/W(j-1);
        incs=1:W(j-1); incs=incs*inc;
        postmorph(L(j-1)+1:L(j))=postnew(L(j-1)+1:L(j))+incs';
        
    end
    lag2=OEpulse-postmorph(L);
    
    disp('The lag has been fixed');
    maxlag=max(lag2);
    if maxlag<2/30
        postnew=postmorph;
    end
    
    
else
    
    postnew = post+(min(OEpulse)-min(BZpulse));
end
% catch
%     cprintf('red', 'pulses do not match, trying to remove mismatched pulses');
% 
%     for i=1:length(BZpulse)
%         if (maxtimes(i)-mintimes(i))>5 % remove flashes that aren't the LED
%             BZpulse(i)=[]; maxtimes(i)=[]; mintimes(i)=[];OnL(i)=[];OffL(i)=[]
%         end
%         % check if interflash interval is same BZ and OE        
%     end
%         OEdiff=diff(OEpulse);
%         BZdiff=diff(BZpulse); 
%     for i=1:length(BZdiff)
%         if abs(BZdiff(i)-OEdiff(i))>1 % remove flashes that aren't the LED
%             OEpulse(i+1)=[]
%         end             
%     end   
%     OEpulse=OEpulse(1:length(BZpulse));
%     %% align based on remaining pulses
%     BZnorm=BZpulse-min(BZpulse)+min(OEpulse);
%     lag=OEpulse-BZnorm;
%     maxlag=max(abs(lag))
%     postnew = post+(min(OEpulse)-post(L(1))); 
%     lag=OEpulse-postnew(L);
%     postmorph=postnew;
%     for j=2:length(L)
%         inc=lag(j)/W(j-1);
%         incs=1:W(j-1); incs=incs*inc;
%         postmorph(L(j-1)+1:L(j))=postnew(L(j-1)+1:L(j))+incs';
%         
%     end
%     lag2=OEpulse-postmorph(L);
%     
%     cprintf('green','The lag has been fixed')
%     maxlag=max(lag2)
%     if maxlag<2/30
%         postnew=postmorph;
%     end
%     %%
% %     if (maxtimesS(1)-mintimesS(1))<5
% %     cprintf('red', 'pulses do not match, aligning based on first pulse');
% %     postnew = post+(min(OEpulse)-min(BZpulse));
% %     else
% %     cprintf('red', 'pulses do not match, and first pulse is wrong');
% %     end
% end
%% Syncronise data

%total_time=max(post)-min(post);

%     post=post(mintimes:length(light));
%     posx=posx(mintimes:length(light));
%     posy=posy(mintimes:length(light));
%     postnew=postnew(mintimes:length(light));
%     HDint=HDint(mintimes:length(light));
%     hd=hd(mintimes:length(light));
