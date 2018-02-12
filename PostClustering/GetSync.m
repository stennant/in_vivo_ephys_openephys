function [Ons,Offs]=GetSync
try
fname=dir('105_CH20*'); fname=fname.name;
catch
    fname=dir('100_ADC1*'); fname=fname.name;
end
%% get sync data from openephys

[Sync, LEDtime, ~] = load_open_ephys_data(fname);

%% identification of sync pulses
onindexS=Sync>0.5;
flipS=diff(onindexS);
mintimesS=find(flipS==1); mintimesS=mintimesS+1;
maxtimesS=find(flipS==-1);
Ons=LEDtime(mintimesS);
Offs=LEDtime(maxtimesS);