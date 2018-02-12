function [post,posx,posy,HD,HDint,light]= readbonsai(fname,pixel_ratio)
figures=0; % set as 1 if you want to check what position data looks like. you will need to type 'dbcont' when prompted
maxspeed=1; % m/second % defined for removing jumps - anything above this isn't realistic
fid=fopen(fname); 
contents=textscan(fid,'%s %f %f %f %f %f');
leftx=cell2mat(contents(2));
lefty=cell2mat(contents(3));
rightx=cell2mat(contents(4));
righty=cell2mat(contents(5));
light=cell2mat(contents(6));
%% extract time data
time=contents{1}; time = cellfun(@(x) x(12:24), time, 'UniformOutput', false);[~,~,~,H,MN,S]=datevec(time); %extract times
post=H*3600+MN*60+S; %post=post-min(post); %convert to seconds and don't subtract start time
%% process light data
%  lightmed=nanmedian(light); lightmax=max(light); lightthresh=lightmed+((lightmax-lightmed)/100);
%  light(light<lightthresh)=lightmed; light=light-lightmed;
% work out pixel_ratio if does not exist
if ~exist('pixel_ratio','var')
    pixel_ratio=mean([max([max(leftx)-min(leftx) max(rightx)-min(rightx)]) max([max(lefty)-min(lefty) max(rightx)-min(righty)])]);
    if pixel_ratio<380 % this can only happen if mouse is not in the 1m box so reset pixel_ratio to default
        pixel_ratio=490;
    end
end

maxspeed=maxspeed*pixel_ratio; % pixels/second
%% remove jumps in data
[leftx, lefty] = remove_jump_pos_mouse(leftx, lefty, post,maxspeed);
[rightx, righty] = remove_jump_pos_mouse(rightx, righty, post,maxspeed);
cprintf('green','\t%d %% left coverage\n', round(sum(~isnan(leftx))/length(leftx)*100));
cprintf('green','\t%d %% right coverage\n', round(sum(~isnan(rightx))/length(rightx)*100));
cprintf('blue','\t%d %% double coverage\n', round(sum(~isnan(rightx.*leftx))/length(rightx)*100));


%% create hd only during times when both lights are visible and believable
leftxp=leftx;leftyp=lefty;rightxp=rightx;rightyp=righty;
% dist=sqrt(((leftxp-rightxp)+(leftyp-rightyp)).^2); %delete points that have >minimum distance apart
% leftxp(dist>35)=NaN; leftyp(dist>35)=NaN;rightxp(dist>35)=NaN; rightyp(dist>35)=NaN;
[hdrad,rho]=cart2pol((rightxp-leftxp),(rightyp-leftyp));
HD=rad2deg(hdrad); %output HD data
HD(rho>40)=NaN;
cprintf('red','\t%d samples violate left-right distance\n', sum(rho>40));
cprintf('blue','\t%d %% of data has head-direction\n', round(sum(~isnan(HD))/length(HD)*100));
%% create central position
posx=(leftx+rightx)/2; posx(rho>40)=NaN;
posy=(lefty+righty)/2; posy(rho>40)=NaN;


%% calculate central based on remaining when single
%getittowraptherightway
HDplus=HD; HDplus(HDplus<0)=HDplus(HDplus<0)+360;
hdint1=fillmissing(HD,'linear'); length1=abs(diff(hdint1)); length1=[NaN; length1];
hdint2=fillmissing(HDplus,'linear'); length2=abs(diff(hdint2)); length2=[NaN; length2];
hdint2(hdint2>180)=hdint2(hdint2>180)-360;
hdint1(length1>length2)=NaN; hdint2(length2>length1)=NaN;
HDint=HD;
HDint(isnan(HDint))=hdint1(isnan(HDint)); HDint(isnan(HDint))=hdint2(isnan(HDint));

rho(rho>40)=NaN; 
rho=fillmissing(rho,'linear');
rho=rho/2;
[vectx,vecty]=pol2cart(deg2rad(HDint),rho);
posxL=leftx+vectx; 
posyL=lefty+vecty;
posxR=rightx-vectx;
posyR=righty-vecty;
posxB=posxL; posxB(isnan(posxB))=posxR(isnan(posxB));
posyB=posyL; posyB(isnan(posyB))=posyR(isnan(posyB));
[posxB,posyB] = remove_jump_pos_mouse(posxB, posyB, post,maxspeed);
posx(isnan(posx))=posxB(isnan(posx));posy(isnan(posy))=posyB(isnan(posy));
[posx,posy] = remove_jump_pos_mouse(posx, posy, post,maxspeed); % remove jumps
%% jump filter this removes points that don't fail on remove jump pos but are more than 15cm away from last position point
if figures==1
fighandle=figure; posxcont=fillmissing(posx,'linear'); posycont=fillmissing(posy,'linear'); plot(posxcont,posycont,'k'); hold on;
end
endit=0;
for counter=1:20
    if endit==0
        index=1:length(posx);
        posxi=posx; posyi=posy;
        posxi(isnan(posx))=[]; posyi(isnan(posx))=[]; index(isnan(posx))=[];
        diffs=sqrt((abs(diff(posxi))+abs(diff(posyi))).^2); diffs=[0;diffs];
        posxi(diffs>50)=NaN;
        if counter>1
            if sum(isnan(posxi))< oldsum
                posx(index(isnan(posxi)))=NaN;
                posy(index(isnan(posxi)))=NaN;
                cprintf('green','\t%d bad position points removed,%d %% position data remaining\n', sum(isnan(posxi)),round(sum(~isnan(posx))/length(posx)*100));
                oldsum=sum(isnan(posxi));
            else 
                endit=1;
            end
        else
            posx(index(isnan(posxi)))=NaN;
            posy(index(isnan(posxi)))=NaN;
            cprintf('green','\t%d NaNs,%dNaNs\n', sum(isnan(posx)),sum(isnan(posxi)));
            oldsum=sum(isnan(posxi)) ;  
        end
    end
end

%% final kalman filter
if figures==1
    posxcont=fillmissing(posx,'linear'); posycont=fillmissing(posy,'linear'); plot(posxcont,posycont,'r');
end
[post,posx,posy]=trajectory_kalman_filter(posx,posy,post); 
if figures==1
plot(posx,posy,'c');
drawnow
disp('type dbcont to continue')
keyboard
close(fighandle)
end
