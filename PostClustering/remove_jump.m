function [posx, posy] = remove_jump(posx, posy, post, max_speed)

% max_speed = 500; % maximum speed allowed (pixals / s), instantaneous speed data exceeding this speed will cause the offending position data to be thrown out
speed=sqrt((diff(posx)).^2 + (diff(posy)).^2) ./ (diff(post));
speed=[NaN; speed];
nansbefore=sum(isnan(posx));
posx(speed>max_speed)=NaN;
posy(speed>max_speed)=NaN;
remove_count = sum(isnan(posx))-nansbefore
cprintf('black','\t%d samples were removed due to speed exceeding maximum\n', remove_count);

