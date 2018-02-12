function frmap_out = GridAutoCorr(frmap1)

% calculate shift values

lengthy = size(frmap1,1)-1;
lengthx = size(frmap1,2)-1;

for i = -lengthx:lengthx;
        shiftx = i;
        for j = -lengthy:lengthy
                shifty = j;
                %shift frmap
                frmap2 =shiftmatrix(frmap1,1,[shiftx shifty],NaN);
                %correlate two maps
                nNanI = ~isnan(frmap1);
                frmap1c = frmap1(nNanI);
                frmap2c = frmap2(nNanI);
                nNanI = ~isnan(frmap2c);
                frmap1c = frmap1c(nNanI);
                frmap2c = frmap2c(nNanI);


                corry = i+lengthx+1;
                corrx = j+lengthy+1;
                if isempty(frmap1c)
                        corr_vector(corrx,corry) = NaN;
                elseif numel(frmap1c)<20
                        corr_vector(corrx,corry) = NaN;
                else
                        corr_vector(corrx,corry) = corr(frmap1c, frmap2c);
                end % if isempty(frmap1c)
        end % for j = -lengthy:lengthy
end % for i = -lengthx:lengthx;
frmap_out = corr_vector;




















%map1 = map;
%map2 = map;

%% Number of bins in each dimension of the rate map
%numBins = size(map1,1);

%% Number of correlation bins
%numCorrBins = numBins * 2 - 1;

%% Index for the centre bin in the correlation map
%centreBin = (numCorrBins+1)/2;

%% Allocate memory for the cross-correlation map
%Rxy = zeros(numCorrBins);



%for hLag = 0:numBins-1
%    for vLag = 0:numBins-1
%        sumX = 0;
%        sumY = 0;
%        sumX2 = 0;
%        sumY2 = 0;
%        sumXY = 0;
%        N = 0;
%        for ii = 1:numBins-hLag
%            for jj = 1:numBins-vLag
%                if ~isnan(map1(ii,jj)) && ~isnan(map2(ii+hLag,jj+vLag))
%                    sumX = sumX + map1(ii,jj);
%                    sumY = sumY + map2(ii+hLag,jj+vLag);
%                    sumX2 = sumX2 + map1(ii,jj)^2;
%                    sumY2 = sumY2 + map2(ii+hLag,jj+vLag)^2;
%                    sumXY = sumXY + map1(ii,jj) * map2(ii+hLag,jj+vLag);
%                    N = N + 1;
%                end
%            end
%        end
%        Rxy(centreBin-hLag,centreBin-vLag) = (N*sumXY - sumX*sumY)/(sqrt(N*sumX2 - sumX^2) * sqrt(N*sumY2 - sumY^2));
%        Rxy(centreBin+hLag,centreBin+vLag) = Rxy(centreBin-hLag,centreBin-vLag);
%        
%        sumX = 0;
%        sumY = 0;
%        sumX2 = 0;
%        sumY2 = 0;
%        sumXY = 0;
%        N = 0;
%        for ii = 1:numBins-hLag
%            for jj = 1:numBins-vLag
%                if ~isnan(map1(ii,jj+vLag)) && ~isnan(map2(ii+hLag,jj))
%                    sumX = sumX + map1(ii,jj+vLag);
%                    sumY = sumY + map2(ii+hLag,jj);
%                    sumX2 = sumX2 + map1(ii,jj+vLag)^2;
%                    sumY2 = sumY2 + map2(ii+hLag,jj)^2;
%                    sumXY = sumXY + map1(ii,jj+vLag) *map2(ii+hLag,jj);
%                    N = N + 1;
%                end
%            end
%        end
%        Rxy(centreBin+hLag,centreBin-vLag) = (N*sumXY - sumX*sumY)/(sqrt(N*sumX2 - sumX^2) * sqrt(N*sumY2 - sumY^2));
%        Rxy(centreBin-hLag,centreBin+vLag) = Rxy(centreBin+hLag,centreBin-vLag);
%    end
%end

