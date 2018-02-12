function [nclu,labels] = getclusters2(filename)

% read cluster labels from KlustaKwik .clu file
% usage: [nclu,labels] = getclusters(filename)
%
% Matthijs van der Meer <M.vanderMeer@ed.ac.uk>
% modified by Steven Huang for efficiency<s.huang@ed.ac.uk>
%
% Centre for Neuroscience and Institute for Adaptive and Neural
% Computation, University of Edinburgh, UK
% http://www.cfn.ed.ac.uk and http://www.anc.ed.ac.uk

fid = fopen(filename,'r');

if (fid == -1)
   error(sprintf('Could not open file %s',filename));
end

line = fgetl(fid);
nclu = sscanf(line,'%d');
i = 1;
ind = 0;
while 1
  if ~ischar(fgetl(fid)), break, end
  ind = ind+1;
end
fclose(fid);
labels = zeros(1,ind);
ind = 1;
fid = fopen(filename,'r');
line = fgetl(fid);
while 1
  line = fgetl(fid);
  if ~ischar(line), break, end
  tmp = sscanf(line,'%d');
  labels(ind) = tmp;
  ind = ind+1;
end

zero_clust = find(labels == 0);
if (length(zero_clust > 0))
  labels(zero_clust) = 1; %group artificial cluster (assigned label 0) with noise cluster (assigned label 1)
  nclu = nclu - 1;
end

fclose(fid);

