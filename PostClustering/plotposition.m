function plotposition(posx,posy,spkx,spky,subplots)

subplot(subplots(1),subplots(2),subplots(3:end));
plot(posx,posy,'k');
hold on
scatter(spkx,spky,'.r');
axis([min(posx) max(posx) min(posy) max(posy)]);
