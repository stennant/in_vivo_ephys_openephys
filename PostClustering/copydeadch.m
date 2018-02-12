%% copydeadch - copies dead_channels.txt to all subfolders
%% find all subfolders
contents=dir; contents(1:2)=[];
dirflags=[contents.isdir];
foldernames=contents(dirflags);

for i=1:length(foldernames)
    subpath=strcat(foldernames(i).name,'/dead_channels.txt');
    copyfile('dead_channels.txt',subpath);
end