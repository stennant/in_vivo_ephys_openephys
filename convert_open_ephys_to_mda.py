'''
Functions for converting open ephys data to mountainsort's mda format

'''

import dead_channels
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
    if prm.get_is_windows():
        spike_data_path = prm.get_spike_path() + '\\'
    if prm.get_is_ubuntu():
        spike_data_path = prm.get_spike_path() + '/'
    continuous_file_name = prm.get_continuous_file_name()
    continuous_file_name_end = prm.get_continuous_file_name_end()

    raw_mda_file_path = file_utility.get_raw_mda_path_separate_tetrodes(prm)

    for tetrode in range(number_of_tetrodes):
        live_channels = dead_channels.get_list_of_live_channels(prm, tetrode)
        number_of_live_ch_in_tetrode = 0
        if os.path.isfile(spike_data_path + 't' + str(tetrode + 1) + raw_mda_file_path) is False:
            channel_data_all = []
            if len(live_channels) >= 3:
                for channel in range(4):
                    if (channel + 1) in live_channels:
                        number_of_live_ch_in_tetrode += 1
                        file_path = folder_path + continuous_file_name + str(tetrode*4 + channel + 1) + continuous_file_name_end + '.continuous'
                        channel_data = open_ephys_IO.get_data_continuous(prm, file_path)
                        channel_data_all.append(channel_data)

                recording_length = len(channel_data_all[live_channels[0]])
                channels_tetrode = np.zeros((number_of_live_ch_in_tetrode, recording_length))
                for ch in range(number_of_live_ch_in_tetrode):
                    channels_tetrode[ch, :] = channel_data_all[ch]
                mdaio.writemda16i(channels_tetrode, spike_data_path + 't' + str(tetrode + 1) + raw_mda_file_path)
            else:
                print('The number of live channels is fewer than 3 in this tetrode so I will not sort it.')

        else:
            print('This tetrode is already converted to mda, I will move on and check the next one. ' + spike_data_path + 't' + str(tetrode + 1) + '\\data\\raw.mda')


# this is for putting all tetrodes in the same mda file
def convert_all_tetrodes_to_mda(prm):
    spike_data_path = prm.get_spike_path()
    raw_mda_path = file_utility.get_raw_mda_path_all_channels(prm)
    if os.path.isfile(spike_data_path + raw_mda_path) is False:
        file_utility.create_folder_structure(prm)
        make_sorting_database.create_sorting_folder_structure(prm)
        folder_path = prm.get_filepath()
        continuous_file_name = prm.get_continuous_file_name()
        continuous_file_name_end = prm.get_continuous_file_name_end()

        path = spike_data_path + raw_mda_path

        file_path = folder_path + continuous_file_name + str(1) + continuous_file_name_end + '.continuous'
        first_ch = open_ephys_IO.get_data_continuous(prm, file_path)

        live_channels = dead_channels.get_list_of_live_channels_all_tetrodes(prm)
        number_of_live_channels = len(live_channels)

        recording_length = len(first_ch)
        channels_all = np.zeros((number_of_live_channels, recording_length))

        for channel in range(number_of_live_channels):
            if (channel + 1) in live_channels:
                file_path = folder_path + continuous_file_name + str(channel + 1) + continuous_file_name_end + '.continuous'
                channel_data = open_ephys_IO.get_data_continuous(prm, file_path)
                channels_all[channel, :] = channel_data

        mdaio.writemda16i(channels_all, path)
    else:
        print('The mda file that contains all channels is already in Electrophysiology/Spike_sorting/all_tetrodes/data.'
              ' You  need to delete it if you want me to make it again.')












