function [runind,speed]=speedfilter(posx,posy,post,speedcut,pixel_ratio)
%% pixel ratio is defined in pixels per meter, 
%% speedcut is defined in cm/second

if ~exist('pixel_ratio','var')
    pixel_ratio=max([max(posx)-min(posx) max(posy)-min(posy)]);
end

diffpos=sqrt(diff(posx).^2+diff(posy).^2);
diffpos=[NaN diffpos';diffpos' NaN]; 
speed=nanmean(diffpos); %speed in pixels per timepoint

speed=speed/(pixel_ratio/100)/mean(diff(post)); % speed in cm/second

runind=zeros(size(speed));
runind(speed>speedcut)=1;
