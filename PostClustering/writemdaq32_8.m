function writemdaq32_8(X,fname)
%WRITEMDA - write to a .mda file. with 8-bit quantization
%
% Syntax: writemdaq32_8(X,fname)
%
% Inputs:
%    X - the multi-dimensional array
%    fname - path to the output .mda file
%
% Other m-files required: none
%
% See also: readmda

% Author: Jeremy Magland
% June 2016

if nargin<2
    test_writemdaq32_8;
    return;
end;

num_dims=2;
if (size(X,3)~=1) num_dims=3; end;
if (size(X,4)~=1) num_dims=4; end;
if (size(X,5)~=1) num_dims=5; end;
if (size(X,6)~=1) num_dims=6; end;

FF=fopen(fname,'w');

fwrite(FF,-1003,'int32'); %float32
fwrite(FF,4,'int32');
fwrite(FF,num_dims,'int32');
dimprod=1;
for dd=1:num_dims
    fwrite(FF,size(X,dd),'int32');
    dimprod=dimprod*size(X,dd);
end;

Y=reshape(X,dimprod,1);
[qtable,bytes]=make_quantization_table32_8(Y);
fwrite(FF,8,'int32'); %8-bit
fwrite(FF,qtable,'float32');
fwrite(FF,bytes,'uchar');

fclose(FF);
end

function [qtable,bytes]=make_quantization_table32_8(X)
N=length(X);
qsize=2^8;
[Xsorted,inds]=sort(X);
[~,inds2]=sort(inds);
bytes=round(inds2/N*(qsize-1));
qtable=Xsorted(round(linspace(1,N,qsize)));
end

function test_writemdaq32_8
t=linspace(0,1,1000);
X=rand(size(t))+sin(t*2*pi*30);
writemdaq32_8(X,'test.mdaq');
Y=readmdaq('test.mdaq');
figure; plot(1:length(X),X,'b',1:length(Y),Y,'r');
end

