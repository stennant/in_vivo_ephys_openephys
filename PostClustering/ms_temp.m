function path=ms_temp
mfile_path=fileparts(mfilename('fullpath'));
path=sprintf('%s/../../tmp',mfile_path);
if (~exist(path,'dir'))
    mkdir(path);
end;
end