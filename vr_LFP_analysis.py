# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 15:33:25 2015

@author 
Marlies - convert_rawkwd_to_dat function
Klara - some based on Alfredo's scripts
"""
from __future__ import division
import h5py
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy import signal
import os
from scipy.signal import butter, filtfilt
import parameters
import file_reader

prm = parameters.Parameters()
#TODO - get rid of this and make these functions accept any channel!!!
test_channel=11


#get signal from chosen channel for indices
def signal_for_indices(channel,raw_data,indices):
    signal = []
    channel_data = raw_data[:,channel]
    for i in indices:
        signal.append(channel_data[i])
    return signal
    

def intersect(a, b):
    return list(set(a) & set(b))



#this needs to be modified to only give the signal back using the indices from the movement module
def cached_stationary_movement(channel, filepath, raw_data, velocity):
    if os.path.isfile(filepath + "stationary.npy") == False or os.path.isfile(filepath + "moves.npy") == False:
        stationary, moves = moves_or_stationary(velocity)
        np.save(filepath + "stationary", stationary)
        np.save(filepath + "moves", moves)
    else:
        stationary = np.load(filepath + "stationary.npy")
        moves = np.load(filepath + "moves.npy")
    if os.path.isfile(filepath + "stationary_signal.npy") == False or os.path.isfile(
                    filepath + "movement_signal.npy") == False:
        # TODO: Write movement_stationary_ephys in a way that it makes these arrays for all channels
        #        stationary_signal,movement_signal = movement_stationary_ephys(channel, data, moves, stationary)
        stationary_signal = signal_for_indices(channel, raw_data, stationary)
        movement_signal = signal_for_indices(channel, raw_data, moves)
        np.save(filepath + "stationary_signal", stationary_signal)
        np.save(filepath + "movement_signal", movement_signal)
    else:
        stationary_signal = np.load(filepath + "stationary_signal.npy")
        movement_signal = np.load(filepath + "movement_signal.npy")
    return movement_signal, moves, stationary, stationary_signal

    
#Calculate location, velocity, speed, stationary and movement indices and save them, or open if they exist
def save_or_open_arrays(filepath,filename, raw_data, samplingpoints_per200ms,channel):
#Check for empty files and delete them if there are any
    for file in os.listdir(filepath):
        os.chdir(filepath)
        if file.endswith(".npy") and os.path.getsize(file)==0:
            print('---FILE ERROR: The size of '+file+' is 0, something is wrong.---')
    movement_signal, moves, stationary, stationary_signal = cached_stationary_movement(channel, filepath, raw_data,
                                                                                       velocity)
    return stationary_signal, movement_signal, beaconed, nbeaconed, probe, beaconed_signal, nbeaconed_signal, \
           probe_signal



'''
#plot power spectum for channel
def power_spectrum(channel,samplingrate,color):
#    channel = data['data'][:,10][-50947920:] #channel 11, 5th of the data is removed from the beginning because of noise
    ps = np.abs(np.fft.fft(channel))**2
    time_step = 1 / int(samplingrate)
    freqs = np.fft.fftfreq(channel.size, time_step)
    idx = np.argsort(freqs)
    plt.plot(freqs[idx], ps[idx],color,linewidth=10)
    plt.xlim(0,200)

#plot logarithmic power spectum for channel
def power_spectrum_log(channel,samplingrate,color):
# I hardcoded my sampling rate (30000) to be nperseg in spectral.py (python file) anf commented out some conditions. There was no other way.
    window=scipy.signal.get_window('hamming',samplingrate)
    f, Pxx_den = signal.periodogram(channel, samplingrate, window)
    plt.semilogy(f, np.sqrt(Pxx_den), color, linewidth=5)
    plt.xlim([0, 100])
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.show()
'''
  
#Plot power spectra for the same amount of stationary and movement data
def stationary_movement_power_spectra(stationary_signal,movement_signal,samplingrate):
    #Make sure that arrays are the same size
   if len(stationary_signal)>len(movement_signal):
       stationary_signal = stationary_signal[:len(movement_signal)]
   else:
       movement_signal = movement_signal[:len(stationary_signal)]

#   print(len(movement_signal)) 
#   print(len(stationary_signal))
   power_spectrum_log(stationary_signal,samplingrate,'k')
   power_spectrum_log(movement_signal,samplingrate,'b')

#it is not necessary for the arrays to be the same size for a power spectrum
def location_specific_power_spectra(raw_data,samplingrate,array1,array2,array3):
    if len(array1)<len(array2) and len(array1)<len(array3):
        array2 = array2[:len(array1)]
        array3 = array3[:len(array1)]
    if len(array2)<len(array1) and len(array2)<len(array3):
        array1 = array1[:len(array2)]
        array3 = array3[:len(array2)]
    if len(array3)<len(array1) and len(array3)<len(array2):
        array1 = array1[:len(array3)]
        array2 = array2[:len(array3)]
    array1_signal = signal_for_indices(test_channel, raw_data, array1)
    array2_signal = signal_for_indices(test_channel, raw_data, array2)
    array3_signal = signal_for_indices(test_channel, raw_data, array3)
    
    power_spectrum_log(array1_signal,samplingrate,'k')
    power_spectrum_log(array2_signal,samplingrate,'b')
    power_spectrum_log(array3_signal,samplingrate,'r')
            
#TODO
# it is not necessary to make the arrays the same size for this since this is normalized anyway
def beaconed_nbeaconed_probe_power_spectra(beaconed_signal,nbeaconed_signal,probe_signal,samplingrate):
    beaconed_signal = beaconed_signal[:len(probe_signal)]
    nbeaconed_signal = nbeaconed_signal[:len(probe_signal)]
    power_spectrum_log(beaconed_signal,samplingrate,'k')
    power_spectrum_log(nbeaconed_signal,samplingrate,'b')
    power_spectrum_log(probe_signal,samplingrate,'r')


# This is to test the script while developing - plots Ch11, location and speed
def test(raw_data,speed,velocity,location,color,channel):
#    channel = raw_data[:,10]
    plt.rcParams.update({'font.size': 36})
    plt.xlabel('sample points (rate=30000/sec)')
  #  plt.plot(all_channels[0],'g')
 #   plt.plot(all_channels[10]-5000,'b')
#    plt.plot(all_channels[11]-10000,'k')
#    plt.plot(location*100+1000,'k') # Channel 21 contains information about the location on the VR.
#    plt.plot(velocity)
#    plt.plot(speed*1000000-5000,'c')
#    theta_filter(all_channels[9],samplingrate,0,'g')
#    theta_filter(all_channels[10],samplingrate,5000,'b')
#    theta_filter(all_channels[11],samplingrate,10000,'k')
 #   gamma_filter(all_channels[9],samplingrate,'b')





