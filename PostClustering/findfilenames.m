function [filenames]=findfilenames(type)

% FINDFILENAMES is a function to find the correct open-ephys filenames within the current folder
%   type should be either 'continuous' or 'spikes'
%   [filenames]=findfilenames('continuous') will output all 16 .continuous
%   [filenames]=findfilenames('spikes') will output 4 .spikes files
%   filenames will be a cell array of strings listing all 16
%   channel.continous files or all 4 TT*.spikes files

allfilenames=dir(strcat('*.',type));
if length(type)==10;
    rootfilename=allfilenames(1).name;
    idx = strfind(rootfilename,'CH') ;
    filenamestart = rootfilename(1:idx+1);
    filenameend=rootfilename(idx:end);
    idx=strfind(filenameend,'_');
    filenameend=filenameend(idx:end);
    for i=1:16
        filenames(i)={strcat(filenamestart,num2str(i),filenameend)};
    end;
elseif length(type)==6
    allfilenames=dir(strcat('*.',type));
    for i=1:length(allfilenames)
        filenames(i)={allfilenames(i).name};
    end
end