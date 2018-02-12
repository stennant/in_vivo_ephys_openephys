%function CreateFolders                                                                                                    % by Roddy %%                                                                                                                                                      %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%       This script makes folders for images etc in the current directory
%       Any folder names contained in fold will be created										     	                  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
disp('Making data folders...')
fold = {'Figures','Data'};                                                                                                     % a list of folders to make
num = 0;                                                                                                                                % start a counter
for file = 1:length(fold)                                                                                                               % for every folder name listed in fold
        name = fold{file};  
        currentfolder=cd; % get the filename
        if ~exist(fullfile(currentfolder,name),'dir')                                                                                                        % if a folder with that name does not exist in the current directory								
                disp(sprintf('\t...making %s folder',name));                                                                 % display a message
                mkdir(name);                                                                                                            % make a new folder with the current folder name
	        num = num + 1;	                                                                                                        % increment counter							
        end % if exist(a, 'file')
end % for file = 1:length(ext)
disp(sprintf('\t...done'));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
