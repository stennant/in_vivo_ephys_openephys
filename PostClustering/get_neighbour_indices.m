%%% Steven Huang<s.huang@ed.ac.uk> %%%
function indices = get_neighbour_indices(ii,jj, max_x, max_y)
xx = [ii-1 ii ii+1];
yy = [jj-1 jj jj+1];

xx = xx(xx>0 & xx<=max_x);
yy = yy(yy>0 & yy<=max_y);

lx = length(xx);
ly = length(yy);

indices = zeros(lx*ly - 1, 2);

ind = 1;
for (kk=1:lx)
  for(ll=1:ly)
    if (xx(kk)~=ii || yy(ll)~=jj)
      indices(ind,1) = xx(kk);
      indices(ind,2) = yy(ll);
      ind = ind+1;
    end
  end
end
