import os
import csv
import file_utility


def get_dead_channel_ids(prm):
    file_utility.set_dead_channel_path(prm)
    dead_ch_path = prm.get_dead_channel_path()

    if os.path.isfile(dead_ch_path) is True:
        dead_channel_reader = open(dead_ch_path, 'r')
        dead_channels = dead_channel_reader.readlines()
        dead_channels = list([x.strip() for x in dead_channels])
        prm.set_dead_channels(dead_channels)

    else:
        print('There are no dead channels in this recording, or dead_channels.txt is missing.')


def remove_dead_channels_from_geom_file_tetrode_by_tetrode(prm, tetrode):
    main_path = file_utility.get_main_path(prm)
    dead_ch_path = prm.get_dead_channel_path()
    geom_path = ''

    if prm.is_windows:
        geom_path = '\\sorting_files\\geom.csv'
    if prm.is_ubuntu:
        geom_path = '/sorting_files/geom.csv'

    tetrode_channels = [1, 2, 3, 4]

    if os.path.isfile(dead_ch_path) is True:
        dead_channels = prm.get_dead_channels()
        for channel in range(len(dead_channels[0])):
            channel_id = int(dead_channels[0][channel])
            if (tetrode*4 + 1) <= channel_id <= (tetrode*4 + 4):
                ch_number = channel_id % 4
                if ch_number == 0:
                    ch_number = 4
                tetrode_channels.remove(ch_number)

    with open(main_path + geom_path, 'w', newline='') as csvfile:
        for channel in tetrode_channels:
            fieldnames = ['channel_id', 'distance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow({'channel_id': channel, 'distance': 0})


def remove_dead_channels_from_geom_file_all_tetrodes(prm):
    main_path = file_utility.get_main_path(prm)
    dead_ch_path = prm.get_dead_channel_path()

    if prm.is_windows:
        geom_path = '\\sorting_files\\geom_all_tetrodes.csv'
    if prm.is_ubuntu:
        geom_path = '/sorting_files/geom_all_tetrodes.csv'

    coordinates_x = [0, 25, 25, 0, 200, 225, 225, 200, 400, 425, 425, 400, 600, 625, 625, 600]
    coordinates_y = [0, 0, 25, 25, 200, 200, 225, 225, 400, 400, 425, 425, 600, 600, 625, 625]

    if os.path.isfile(dead_ch_path) is True:
        dead_channels = prm.get_dead_channels()
        for channel in range(len(dead_channels[0])):
            dead_channel_index = int(dead_channels[0][channel]) - 1
            temporary_value_to_replace = 6666
            coordinates_x[dead_channel_index] = temporary_value_to_replace
            coordinates_y[dead_channel_index] = temporary_value_to_replace

        coordinates_x.remove(temporary_value_to_replace)
        coordinates_y.remove(temporary_value_to_replace)

        with open(main_path + geom_path, 'w', newline='') as csvfile:
            for channel in range(len(coordinates_x)):
                fieldnames = ['x_coord', 'y_coord']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writerow({'x_coord': coordinates_x[channel], 'y_coord': coordinates_y[channel]})
    else:
        return


def get_list_of_live_channels(prm, tetrode):
    tetrode_channels = [1, 2, 3, 4]

    dead_ch_path = prm.get_dead_channel_path()
    if os.path.isfile(dead_ch_path) is True:
        dead_channels = prm.get_dead_channels()
        for channel in range(len(dead_channels[0])):
            channel_id = int(dead_channels[0][channel])
            if (tetrode*4 + 1) <= channel_id <= (tetrode*4 + 4):
                ch_number = channel_id % 4
                if ch_number == 0:
                    ch_number = 4
                tetrode_channels.remove(ch_number)
    return tetrode_channels


def get_list_of_live_channels_all_tetrodes(prm):
    channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    dead_ch_path = prm.get_dead_channel_path()

    if os.path.isfile(dead_ch_path) is True:
        dead_channels = prm.get_dead_channels()
        for channel in range(len(dead_channels[0])):
            channel_id = int(dead_channels[0][channel])
            channels.remove(channel_id)
    return channels
