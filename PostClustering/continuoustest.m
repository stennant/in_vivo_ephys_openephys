% function Ephys2mountain
tic;
for tetrode=3
%% get data
    fname=['105_CH2_0.continuous'];
[data, conttime,~] = load_open_ephys_data(fname);
[b,a]=butter(2,[600 6000]/(30000/2));
ref=filter(b,a,data);
for wire=1:4
    elec=((tetrode-1)*4)+wire;
    fname=['105_CH' num2str(elec) '_0.continuous'];
[data, ~,~] = load_open_ephys_data(fname);
[b,a]=butter(2,[600 6000]/(30000/2));
data=filter(b,a,data);
if wire==1; X=zeros(4,length(data)); Y=X; end;
X(wire,:)=data;
data=ref-data;
Y(wire,:)=data;
clear data;
end
%% write mda files
snip=[1 30000];
figure
subplot(8,1,1);
plot(snip(1):snip(2),X(1,snip(1):snip(2)));
subplot(8,1,2);
plot(snip(1):snip(2),Y(1,snip(1):snip(2)));
subplot(8,1,3);
plot(snip(1):snip(2),X(2,snip(1):snip(2)));
subplot(8,1,4);
plot(snip(1):snip(2),Y(2,snip(1):snip(2)));
subplot(8,1,5);
plot(snip(1):snip(2),X(3,snip(1):snip(2)));
subplot(8,1,6);
plot(snip(1):snip(2),Y(3,snip(1):snip(2)));
subplot(8,1,7);
plot(snip(1):snip(2),X(4,snip(1):snip(2)));
subplot(8,1,8);
plot(snip(1):snip(2),Y(4,snip(1):snip(2)));
end

%% compare waveforms
[waves, wavetimes, winfo] = load_open_ephys_data('TT2.spikes');
[nclu,labels] = getclusters2('TT2.clu.1');
ind=[21 67 110 132 135 195 251];
times=wavetimes(ind); times2=times-min(conttime); times2=round(times2*30000);
figure;
for num=1:length(ind);
   
snip=[times2(num)-30 times2(num)+3];
subplot(8,1,1);
plot(1:snip(2)-snip(1)+1,X(1,snip(1):snip(2))); hold on;
subplot(8,1,2);
plot(1:snip(2)-snip(1)+1,Y(1,snip(1):snip(2))); hold on;
subplot(8,1,3);
plot(1:snip(2)-snip(1)+1,X(2,snip(1):snip(2))); hold on;
subplot(8,1,4);
plot(1:snip(2)-snip(1)+1,Y(2,snip(1):snip(2))); hold on;
subplot(8,1,5);
plot(1:snip(2)-snip(1)+1,X(3,snip(1):snip(2))); hold on;
subplot(8,1,6);
plot(1:snip(2)-snip(1)+1,Y(3,snip(1):snip(2))); hold on;
subplot(8,1,7);
plot(1:snip(2)-snip(1)+1,X(4,snip(1):snip(2))); hold on;
subplot(8,1,8);
plot(1:snip(2)-snip(1)+1,Y(4,snip(1):snip(2))); hold on;
end
toc
% end