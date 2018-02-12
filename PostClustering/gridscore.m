% This function computes the gridness score from an autocorrelation map (ACMAP)
% according to Sargolini et al 2006 "Conjunctive Representation of Position, 
% Direction, and Velocity in Entorhinal Cortex" (note that this code is only suitable for 
% square or circular maps)
% 
% Luisa Castro, FCUP
% luisa.castro@fc.up.pt

function[GRSc]=gridscore(ACMAP)

l_ACMAP=length(ACMAP);        %use only square maps					
c_ACMAP=floor((l_ACMAP+1)/2);        			

% Construct a ring filter to extract the six closest fields 
% of the center of the autocorrelation map. 
% The user must choose the apropriate inner and outer radious of such filter.
% For dorsal most areas, the spacing is aprox. 35 and the field 
% radius is aprox. 10. Accordingly, we set:
in_ra  = 10;	%20		
out_ra = 25; %48	

RingFilt=zeros(l_ACMAP);          			
for i=1:l_ACMAP
    for j=1:l_ACMAP     
        if(c_ACMAP-i)^2 + (c_ACMAP-j)^2 <= out_ra^2 && ...
		(c_ACMAP-i)^2 + (c_ACMAP-j)^2 >= in_ra^2
            RingFilt(i,j)=1;
        end
    end
end

ACMAPR=ACMAP.*RingFilt;

ACMAPR=ACMAPR(c_ACMAP-out_ra-1:c_ACMAP+out_ra+1,c_ACMAP-out_ra-1:c_ACMAP+out_ra+1);
[nx,ny]=size(ACMAPR);

% Now rotate the extracted ring of the ACMAP and for each rotation (from 1� to 180�) 
% compute the correlation with the original
% note (para retirar aquando da public): this is the correlation value between two matrixes. 
% The crosscorrelation is a map of correlation values between the two matrices
% and their lags. 
% So basically correlation is the central value of the crosscorrelogram with lag=0.

corrot=zeros(1,180);

for idrot=1:180
    rot=imrotate(ACMAPR,idrot,'crop');
    A=ACMAPR;
    B=rot;
    %corrot computs the correlation between two matrixes A and B
    corrot(idrot)= (nx*ny*sum(dot(A,B))-sum(dot(A,ones(nx,ny)))*sum(dot(B,ones(nx,ny))))/(sqrt(nx*ny*sum(dot(A,A))-(sum(dot(A,ones(nx,ny))))^2)*sqrt(nx*ny*sum(dot(B,B))-(sum(dot(B,ones(nx,ny))))^2));
end

figure %not shown in the manuscript
subplot(211)
imagesc(ACMAPR)
set(gca,'YDir','normal')  
title('Ring of the NormAutoCorMAP')
set(gca,'XTick',[1 nx]);         set(gca,'XTickLabel',{'1',nx})
set(gca,'YTick',[1 ny]);         set(gca,'YTickLabel',{'1',ny})
axis square
colorbar

subplot(212)
plot(corrot(1:180),'g','LineWidth',2)
xlabel('Rotation [deg]');        xlim([0 180])
ylabel('Correlation [r]');       ylim([-0.5 1])
set(gca,'XTick',0:60:180);       set(gca,'XTickLabel',{'0','60','120','180'})
set(gca,'YTick',-0.5:0.5:1);    
GRSc=min(corrot(60),corrot(120))-max([corrot(30);corrot(90);corrot(150)],[],1);
title(['Gridness Score = ',num2str(GRSc)])