function [frh_hd,meandir_hd,r_hd]=plothd(hd,spkhd,sampling_rate,subplots)
subplot(subplots(1),subplots(2),subplots(3:end));

smoo = 11;
angles = -179:180;

[occh,frh] = polar_hist(hd, spkhd, smoo, angles,sampling_rate);
frh(isnan(frh)) = 0; % this occurs when occh = 0, for plotting purposes, it might be easier to just set frh = 0
                                
angles_rad = angles*pi/180;
dy = sin(angles_rad);
dx = cos(angles_rad);

totx = sum(dx.*frh)/sum(frh);
toty = sum(dy.*frh)/sum(frh);
meandir = getdir(totx,toty);
r = sqrt(totx^2+toty^2);

rlim = ceil(max(occh)) + 1;

h=polarplot(angles_rad,frh,'r',angles_rad,occh.*(max(frh)/max(occh)),'k');
                                        
set(h(1),'LineWidth',2);
set(h(2),'LineWidth',1);
h = title(sprintf('Peak: %.1f Hz, PFD: %.1f^o, |{\\itr}|: %.2f',max(frh),meandir,r));
%set(h,'FontSize',6);

frh_hd = max(frh);
meandir_hd = meandir;
r_hd = r;