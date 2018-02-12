function [grid_score grid_spacing field_size grid_orientation grid_ellipticity] = GridAnalysis(amap,binsize)                                              
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%	
%	A script which analyses grid cell autocorrelograms and outputs several commonly used grid field measures.
%
%	Input:
%	amap = the autocorrelation matrix for processing
%	binsize = the bin size (cm) used to create the original firing rate map
%
%	Output:
%		Grid score:
%		Defined by Krupic, Bauza, Burton, Barry, O'Keefe (2015) as the difference between the minimum correlation coefficient for autocorrelogram 
%		rotations of 60 and 120 degrees and the maximum correlation coefficient for autocorrelogram rotations of 30, 90 and 150 degrees.
%		This score can vary between -2 and 2, although generally values above below -1.5 or above 1.5 are uncommon
%
%		Grid spacing/wavelength:
%		Defined by Hafting, Fyhn, Molden, Moser, Moser (2005) as the distance from the central autocorrelogram peak to the vertices of the inner 
%		hexagon in the autocorrelogram (the median of the six distances). 
%		This should be in cm.
%
%		Field Size:
%		Defined by Wills, Barry, Cacucci (2012) as the square root of the area of the central peak of the autocorrelogram divided by pi.
%		This should be in cm2
%
%		Grid orientation:
%		Defined by Hafting, Fyhn, Molden, Moser, Moser (2005) as the angle between a camera-defined reference line (0 degrees or x axis) 
%		and a vector to the nearest vertex of the inner hexagon in the counterclockwise direction
%		This is in degrees and can vary between 0 and 59 (after 59 a new field should emerge at 0 if its a grid cell);
%
%		Ellipticity/eccentricity:
%		As measured by Krupic, Bauza, Burton, Barry, O'Keefe (2015) by fitting an ellipse to the six central peaks of the local spatial 
%		autocorrelogram using a least squares method. Eccentricity e was used as a measure of ellipticity (with 0 indicating a perfect 
%		circle): e = sqrt(1 - (b^2/a^2)) where a and b are the major and minor axis lengths respectively
%		This varies between 0 and 1; 0 is the ellipticity of a perfect circle, 1 is the ellipticity of a parabola
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Find autocorrelation peaks

amap_thresh = amap;															% copy autocorrelation
amap_thresh(amap_thresh < 0.2) = 0;     												% threshold at 0.2
amap_thresh(amap_thresh > 0.2) = 1; 													% threshold at 0.2

bin_amap = bwlabel(amap_thresh,8);													% transform ratemap to binary ratemap, each field becomes an island of a single digit representing that field
stats = regionprops(bin_amap,amap,'Area','Centroid');											% run regionprops to get properties of islands i.e. fields

all_cords = [];																% reserve memory
all_areas = []; 															% reserve memory
for i = 1:length(stats)															% for every field/blob
        c_cords = stats(i).Centroid;													% get its centre point/centroid
        all_cords = [all_cords; c_cords];												% add the coordinates to a matrix

        c_area = stats(i).Area;														% get its area
        all_areas = [all_areas; c_area];												% add this to a matrix too										
end % for i = 1:length(stats)	

if length(all_cords) > 7														% only continue if there are more than 7 peaks (central one and six surrounding ones)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Find field distances from mid_point

	[y,x] = size(amap);														% get the size of the autocorrelation
	mid_amap = [ceil(x/2) ceil(y/2)];												% use the measurements to calculate the matrix's mid point
	dees = [];															% reserve memory
	for p = 1:length(all_cords(:,1))												% for each of the fields/blobs
		c_point = all_cords(p,:);												% load its centre coordinate
		d = sqrt(((c_point(1)-mid_amap(1))^2) + ((c_point(2)-mid_amap(2))^2));							% find its distance from the matrix mid_point
		dees = [dees; d];													% collect this info
	end % for p = 1:length(stats)

	[Y,I] = sort(dees,'ascend');													% sort the blob distances in ascending order
	sorted_dees = dees(I);														% use index to sort the distances
	sorted_peaks = all_cords(I,:);													% use index to sort the field centre coordinates
	sorted_areas = all_areas(I,:);													% use index to sort the field areas
	mid_peak = sorted_peaks(1,:);													% the field with the shortest distance to the matrix midpoint must the be central peak
	ring_peaks = sorted_peaks(2:7,:);												% the next nearest 6 fields are the surrounding ring

	ring_dists = sorted_dees(2:7,:);												% get the distances to the 6 ring fields
	mean_dist = nanmean(ring_dists);													% find the mean of these distances
	grid_spacing = nanmedian(ring_dists)*binsize;%% Calculate grid spacing 
	mask_r = (mean_dist * 2.5)/2;													% calculate the radius of a circle which will surround all 6 ring fields
	mid_mask_r = (mean_dist * 0.5)/2;												% calculate the radius of a circle which will mask the central field

	[X,Y] = CircleCords(mid_peak,mask_r,100);											% use the radius to find 100 vertices of a circle
	[X2,Y2] = CircleCords(mid_peak,mid_mask_r,100);											% use the radius to find 100 vertices of a circle

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Cut autocorrelogram to middle ring for analysis

	BW = poly2mask(X,Y,y,x);													% create a mask using the circle vertices - this one is for the outer ring
	BW2 = poly2mask(X2,Y2,y,x);													% create a mask using the other circle vertices - this one is for the inner ring
	amap(BW == 0) = NaN;														% empty any bins outside the outer circle
	amap(BW2 == 1) = NaN;														% empty any bins inside the inner circle

	amap_fields = amap;	 													% copy autocorrelogram
	amap_fields(amap_fields < 0.2) = NaN;												% threshold at 0.2
	amap_fields(amap_fields > 0.2) = 1;												% threshold at 0.2
	amap_fields(BW2 == 1) = NaN;													% use outer ring mask
	tot_field_area = nansum(nansum(amap_fields))*(binsize^2);										% calculate the area left behind - this should contain only the central field

	field_size = sqrt(tot_field_area)/pi;%% Calculate field size

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Rotate autocorrelogram to find symmetry

	angles = 30:30:150;														% prepare angles; 30 60 90 120 150
	corrs = [];															% reserve memory
	for a = 1:length(angles)													% for each of the angles in 'angles'
		amap2 = imrotate(amap,angles(a),'nearest','crop');									% rotate autocorrelogram by current angle 
		amap2(BW == 0) = NaN;													% apply outer ring mask
		amap2(BW2 == 1) = NaN;													% apply inner ring mask
		[R P] = corrcoef(amap,amap2,'rows','pairwise');										% perform pairwise pearson correlation
		r = R(1,2);														% get r value
		corrs(a) = r;														% store r value
	end % for a = 1:length(angles)
	grid_score = nanmin(corrs([2,4])) - nanmax(corrs([1,3,5]));%% Calculate grid score

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Find orientation of grid to x axis

	orients = [];															% reserve memory
	for r = 1:length(ring_peaks)													% for each field in the central ring
		cpeak = ring_peaks(r,:);  												% get the field's coordinate
		theta = atan2(cpeak(2)-mid_peak(2),cpeak(1)-mid_peak(1))*180/pi;							% calculate the angle between the x axis and a line joining the field to the central field
		orients(r) = theta;													% collect these angles
	end % for r = 1:length(ring_peaks)
	grid_orientation = nanmin(orients(orients > 0));%% Calculate grid orientation

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Find eccentricity/ellipticity of grid 

	[maj_axis,min_axis,x0,y0,phi] = ellipse_fit(ring_peaks(:,1),ring_peaks(:,2));							% fit an ellipse to the ring of fields
	grid_ellipticity = sqrt(1 - (min_axis^2 / maj_axis^2));%% Calculate grid ellipticity

else
	grid_score = NaN;														% if there are less than 7 fields leave all scores empty
	grid_spacing = NaN;
	field_size = NaN;
	grid_orientation = NaN;
	grid_ellipticity = NaN;
end % if length(all_cords)>7







