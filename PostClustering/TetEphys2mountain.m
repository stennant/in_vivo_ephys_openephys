% function Ephys2mountain
tic;
for tetrode=1:4; %1:4
%% get data
[ref, ~,~] = load_open_ephys_data('105_CH2_0.continuous');
ref=zeros(size(ref));
for wire=1:4
    elec=((tetrode-1)*4)+wire;
    fname=['105_CH' num2str(elec) '_0.continuous'];
[data, ~,~] = load_open_ephys_data(fname);
data=ref-data;
if wire==1; X=zeros(4,length(data));end;
X(wire,:)=data;
clear data;
end
%% write mda files
disp('Writing MDA file. Sorry for the delay')
mdaname=['raw' num2str(tetrode) '.mda'];
writemda(X,mdaname,'int32');
clear X;
end
toc
% end