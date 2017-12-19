'''
Functions for converting open ephys data to mountainsort's mda format

'''

import file_utility
import mdaio
import make_sorting_database
import numpy as np
import open_ephys_IO
import os


def convert_continuous_to_mda(prm):
    file_utility.create_folder_structure(prm)
    file_utility.folders_for_separate_tetrodes(prm)
    make_sorting_database.create_sorting_folder_structure_separate_tetrodes(prm)
    number_of_tetrodes = prm.get_num_tetrodes()
    folder_path = prm.get_filepath()
    spike_data_path = prm.get_spike_path() + '\\'
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = prm.get_continuous_file_name_end()

    for tetrode in range(number_of_tetrodes):
        if os.path.isfile(spike_data_path + 't' + str(tetrode + 1) + '\\data\\raw.mda') is False:
            channel_data_all = []
            for channel in range(4):
                file_path = folder_path + continuous_file_name + str(tetrode*4 + channel + 1) + continuous_file_name_end + '.continuous'
                channel_data = open_ephys_IO.get_data_continuous(prm, file_path)
                channel_data_all.append(channel_data)

            recording_length = len(channel_data_all[0])
            channels_tetrode = np.zeros((4, recording_length))

            for ch in range(4):
                channels_tetrode[ch, :] = channel_data_all[ch]
            mdaio.writemda16i(channels_tetrode, spike_data_path + 't' + str(tetrode + 1) + '\\data\\raw.mda')
        else:
            print('This tetrode is already converted to mda, I will move on and check the next one. ' + spike_data_path + 't' + str(tetrode + 1) + '\\data\\raw.mda')


# this is for putting all tetrodes in the same mda file
def convert_all_tetrodes_to_mda(prm):
    file_utility.create_folder_structure(prm)
    make_sorting_database.create_sorting_folder_structure(prm)
    number_of_tetrodes = prm.get_num_tetrodes()
    folder_path = prm.get_filepath()
    spike_data_path = prm.get_spike_path() + '\\'
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = prm.get_continuous_file_name_end()

    path = spike_data_path + 'all_tetrodes\\data\\raw.mda'

    file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
    first_ch = open_ephys_IO.get_data_continuous(prm, file_path)
    recording_length = len(first_ch)
    channels_all = np.zeros((number_of_tetrodes*4, recording_length))
    channels_all[0, :] = first_ch

    for channel in range(15):
        file_path = folder_path + continuous_file_name + str(channel + 2) + continuous_file_name_end + '.continuous'
        channel_data = open_ephys_IO.get_data_continuous(prm, file_path)
        channels_all[channel + 1, :] = channel_data

    mdaio.writemda16i(channels_all, path)












