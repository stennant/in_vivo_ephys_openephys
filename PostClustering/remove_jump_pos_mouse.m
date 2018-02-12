function [posx, posy] = remove_jump_pos_mouse(posx, posy, post, max_speed)

% max_speed = 500; % maximum speed allowed (pixals / s), instantaneous speed data exceeding this speed will cause the offending position data to be thrown out

thrown_pos = 0;
p_posx = NaN;
p_posy= NaN;
p_post = NaN;
si=0;
while((isnan(p_posx) || isnan(p_posy) || isnan(p_post)) && si<length(posx))
  si = si+1;
  p_posx=posx(si);
  p_posy=posy(si);
  p_post=post(si);
end

remove_count = 0;
for ii=si+1:length(posx)
  nposx=posx(ii);
  nposy=posy(ii);
  npost=post(ii);
  if(~isnan(nposx) && ~isnan(nposy) && ~isnan(npost))
    speed = sqrt((nposx-p_posx)^2 + (nposy-p_posy)^2) / (npost-p_post);
    if (speed>max_speed)
      posx(ii) = NaN;
      posy(ii) = NaN;
      remove_count = remove_count + 1;
    else
      p_posx = nposx;
      p_posy = nposy;
      p_post = npost;
    end
  end
end

cprintf('black','\t%d samples were removed due to speed exceeding maximum\n', remove_count);

