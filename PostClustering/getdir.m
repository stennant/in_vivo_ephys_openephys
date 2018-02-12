function d = getdir(dx,dy)


if (dx >= 0) & (dy >= 0)
  
  if (dx == 0)
    d = 90;
  else
    d = atand(dy/dx);
  end
  
elseif (dx > 0) & (dy < 0) 
  
  d = 360-atand(-dy/dx);
  
elseif (dx < 0) & (dy > 0)
  
  d = 180-atand(dy/-dx);
  
else
  
  d = 180+atand(-dy/-dx);
  
end
  