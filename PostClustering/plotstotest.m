wave1=waves(:,:,find(cluid==1));
wave2=waves(:,:,find(cluid==2));
wave3=waves(:,:,find(cluid==3));
wave4=waves(:,:,find(cluid==4));
wave5=waves(:,:,find(cluid==5));

filt1=waves2(:,:,find(cluid==1));
filt2=waves2(:,:,find(cluid==2));
filt3=waves2(:,:,find(cluid==3));
filt4=waves2(:,:,find(cluid==4));
filt5=waves2(:,:,find(cluid==5));

figure
random=rand(1,100);
for b=1:4
subplot(5,4,b)
for i=1:100; 
    wavei=round(size(wave1,3)*random(i)); 
    plot(1:40,wave1(b,:,wavei)); 
    hold on; 
    ylim([-5 15]);
end
end
for b=1:4
subplot(5,4,b+4)
for i=1:100; 
    wavei=round(size(wave2,3)*random(i)); 
    plot(1:40,wave2(b,:,wavei)); 
    hold on; 
    ylim([-5 15]);
end
end

for b=1:4
subplot(5,4,b+8)
for i=1:100; 
    wavei=round(size(wave3,3)*random(i)); 
    plot(1:40,wave3(b,:,wavei)); 
    hold on; 
    ylim([-5 15]);
end
end

for b=1:4
subplot(5,4,b+12)
for i=1:100; 
    wavei=round(size(wave4,3)*random(i)); 
    plot(1:40,wave4(b,:,wavei)); 
    hold on; 
    ylim([-5 15]);
end
end
for b=1:4
subplot(5,4,b+16)
for i=1:100; 
    wavei=round(size(wave5,3)*random(i)); 
    plot(1:40,wave5(b,:,wavei)); 
    hold on; 
    ylim([-5 15]);
end
end