function AM=ms_adjacency_matrix(locations,radius)
% TODO: Docs
N=size(locations,1);
AM=zeros(N,N);
for i1=1:N
    for i2=1:N
        diff0=locations(i1,:)-locations(i2,:);
        dist0=sqrt(diff0*diff0');
        if (dist0<=radius) AM(i1,i2)=1; end;
    end;
end;

end