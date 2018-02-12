function [frmap,posmap,skaggs,spars,cohe,max_firing,coverage]=plotratemap(posx,posy,spkx,spky,pixel_ratio,post,subplots,subplots2)
bin_size=2.5; % in cm
min_dwell_distance=5; % cm from a point to determine min dwell time
dt_position=mean(diff(post))*1000; % (ms) sampling interval for posdata
min_dwell_time=3*dt_position; %~100; % ms min dwell time for plotting rate map
smooth=5;% (cm) smooth factor for gaussian smoothing
% get rid of NaNs so plot works
posx=posx(~isnan(posx)); posy=posy(~isnan(posy));
spkx=spkx(~isnan(spkx)); spky=spky(~isnan(spky));
% create rate map
[posmap,frmap,xmap,ymap,spdmap] = ratemap(posx,posy, spkx, spky, bin_size, pixel_ratio, min_dwell_distance, min_dwell_time, dt_position, smooth, 1);
% calculate output variables
skaggs = skaggs_info2(frmap,posmap);
spars = sparsity(frmap, posmap);
cohe = spatial_coherence(frmap, posmap);
max_firing = max(max(frmap));
% make plot
ax1=subplot(subplots(1),subplots(2),subplots(3:end));
frco = pcolor(frmap);			
colormap(ax1,'JET');
caxis([0 max(max(frmap))]);
shading interp
box off
set(gca,'xcolor','w')
set(gca,'ycolor','w')
ylabel(strcat(num2str(size(frmap,2)*bin_size),'cm by  ',num2str(size(frmap,1)*bin_size),'cm'),'Color','k')
%xlabel(strcat('Max FR =',num2str(round(max(max(frmap)))),'Hz'),'Color','k')

set(gca,'xtick',[])
set(gca,'xticklabel',[])
set(gca,'ytick',[])
set(gca,'yticklabel',[])
set(frco,'linestyle','none');
set(gca, 'DataAspectRatio', [1 1 1]);
title({sprintf('Max FR = %.2f Hz, Spatial Info: %.2f b/s',max(max(frmap)),skaggs),sprintf('Sparsity %.2f%%, Coherence %.2f',(spars*100),cohe)});



% p = get(gca, 'pos');				                                                % p = colorbar parameters (x y (of bottom left corner) width height)
% cb = colorbar('East');                                                 
% axpos=get(cb,'Position');                                                
% axpos(4)=axpos(4)/2;                                                
% axpos(2)=axpos(2)-0.05;                                                
% set(cb,'Position',axpos);% add colorbar to north of last plot
% ylabel(cb, 'Hz');
% set(gca, 'pos', p);	  % Adjusting values
% view(90,90);



if exist('subplots2','var')
ax2=subplot(subplots(1),subplots(2),subplots2);
pco = pcolor(posmap);			
colormap(ax2,'COOL');
caxis([0 max(max(posmap))]);
shading interp
box off
set(gca,'xcolor','w')
set(gca,'ycolor','w')
xlabel(strcat(num2str(size(posmap,2)*bin_size),'cm by  ',num2str(size(posmap,1)*bin_size),'cm'),'Color','k')
set(gca,'xtick',[])
set(gca,'xticklabel',[])
set(gca,'ytick',[])
set(gca,'yticklabel',[])
set(pco,'linestyle','none');
set(gca, 'DataAspectRatio', [1 1 1]);
coverage=sum(sum(~isnan(posmap)))/(size(posmap,1)*size(posmap,2))*100;
title({sprintf('Coverage: %.2f %%',coverage)});
end