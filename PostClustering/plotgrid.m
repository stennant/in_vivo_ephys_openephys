function [grid_score,grid_spacing,field_size,grid_orientation,grid_ellipticity]=plotgrid(frmap,subplots)
bin_size=2.5;
ax3=subplot(subplots(1),subplots(2),subplots(3:end)); % Plotting the grid plot)

corr_vector = GridAutoCorr(frmap);
[grid_score,grid_spacing,field_size,grid_orientation,grid_ellipticity] = GridAnalysis(corr_vector,bin_size);
pos = pcolor(corr_vector);

colormap(ax3,'JET');
caxis([min(min(corr_vector)) max(max(corr_vector))]);
shading interp
box off
set(gca,'xcolor','w')
set(gca,'ycolor','w')
set(gca,'xtick',[])
set(gca,'xticklabel',[])
set(gca,'ytick',[])
set(gca,'yticklabel',[])
set(pos,'linestyle','none');
set(gca, 'DataAspectRatio', [1 1 1]);

if isnan(grid_score)
    title(sprintf('Too few fields to calculate'),'FontSize', 8);
else
    title({sprintf('Gridness: %.1f Spacing: %.1f',grid_score,grid_spacing),sprintf('Size: %.1f Ori: %.1f Elli: %.1f',field_size,grid_orientation,grid_ellipticity)});
end 
