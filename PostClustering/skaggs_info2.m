function info = skaggs_info2(frmap,posmap)

%Dim H0, H1, MeanRate As Single
%Dim SumRate, SumOcc As Single
%Dim j, k As Integer
  

H0 = 0;
H1 = 0;
SumRate = 0;
SumOcc = 0;
for j = 1:length(frmap(:,1))
  for k = 1:length(frmap(1,:))
    if ((posmap(j, k) > 0) & (frmap(j, k) >= 0))
      SumRate = SumRate + frmap(j, k);
      SumOcc = SumOcc + 1;
    end
  end
end

for j = 1:length(frmap(:,1))
  for k = 1:length(frmap(1,:))
        if (frmap(j, k) > 0.0001)
            H1 = H1 + -frmap(j, k) * (log(frmap(j, k)) / log(2)) / SumOcc;
        end
    end
end

MeanRate = SumRate / SumOcc;
H0 = -MeanRate * (log(MeanRate) / log(2));
info = (H0 - H1) / MeanRate;

