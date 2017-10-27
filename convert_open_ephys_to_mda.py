'''
Functions for converting open ephys data to mountainsort's mda format

'''

import mdaio
import numpy as np
import open_ephys_IO


def get_padded_array(waveforms, samples_per_spike):
    number_of_events = waveforms.shape[0]
    padded_array = np.zeros((4, number_of_events, samples_per_spike*2))
    to_insert = np.zeros((samples_per_spike, number_of_events))

    for channel in range(4):
        padded_channel = np.insert(waveforms[:, :, channel], 0, to_insert, axis=1)
        padded_array[channel, :, :] = padded_channel
    return padded_array


def get_peak_indices(waveforms, samples_per_spike):
    number_of_events = waveforms.shape[0]
    waveforms2d = np.zeros((number_of_events, 4*samples_per_spike))

    for event in range(number_of_events):
        waveforms2d[event, :] = waveforms[event, :, :].flatten()

    peak_indices_all_ch = np.argmax(waveforms2d, 1)
    peak_indices = np.floor(peak_indices_all_ch/4)
    return peak_indices


def convert_spk_to_mda(prm):
    folder_path = prm.get_filepath()
    number_of_tetrodes = prm.get_num_tetrodes()
    samples_per_spike = prm.get_waveform_size()

    for tetrode in range(number_of_tetrodes):
        file_path = folder_path + 'TT' + str(tetrode) + '.spikes'
        waveforms, timestamps = open_ephys_IO.get_data_spike(folder_path, file_path, 'TT' + str(tetrode))
        padded_array = get_padded_array(waveforms, samples_per_spike)

        mdaio.writemda32(padded_array, folder_path + 'raw.nt' + str(tetrode) + '.mda')
        peak_indices = get_peak_indices(waveforms, samples_per_spike)
        mdaio.writemda32(peak_indices, folder_path + 'event_times.nt' + str(tetrode) + '.mda')



