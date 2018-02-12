function A=readmdaq(fname)
%READMDA - read the contents of a .mda file, possibly with quantization.
%
% Syntax: A=readmdaq(fname)
%
% Inputs:
%    fname - path to the .mda or .mdaq file
%
% Outputs:
%    A - the multi-dimensional array
%
% Other m-files required: none
%
% See also: writemdaq

% Author: Jeremy Magland
% Jun 2016;

F=fopen(fname,'rb');

try
code=fread(F,1,'int32');
catch
    error('Problem reading file: %s',fname);
end
if (code>-1000) 
    % the standard format
    fclose(F);
    A=readmda(fname);
    return;
end;

fread(F,1,'int32');
num_dims=fread(F,1,'int32');    

S=zeros(1,num_dims);
for j=1:num_dims
    S(j)=fread(F,1,'int32');
end;
N=prod(S);

num_bits=fread(F,1,'int32');
if (num_bits~=8)
    fclose(F);
    error('num_bits=%d not supported',num_bits);
end;

if (code==-1002)
    qtable=fread(F,2^(num_bits),'uchar');
elseif (code==-1003)
    qtable=fread(F,2^(num_bits),'float');
elseif (code==-1004)
    qtable=fread(F,2^(num_bits),'int16');
elseif (code==-1005)
    qtable=fread(F,2^(num_bits),'int32');
elseif (code==-1006)
    qtable=fread(F,2^(num_bits),'uint16');
elseif (code==-1007)
    qtable=fread(F,2^(num_bits),'double');
else
    fclose(F);
    error('Unrecognized code: %d',code);
end;

if num_dims == 1,
  A = zeros(1,S);
else
  A=zeros(S);
end

B=fread(F,N,'uchar');
A(:)=qtable(B+1);

fclose(F);
