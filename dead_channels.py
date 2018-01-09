import os
import csv

def get_dead_channel_ids(prm):
    file_path = prm.get_filepath()
    dead_ch_path = file_path + "\\dead_channels.txt"

    if os.path.isfile(dead_ch_path) is True:
        dead_channel_reader = open(dead_ch_path, 'r')
        dead_channels = dead_channel_reader.readlines()
        dead_channels = list([x.strip() for x in dead_channels])
        prm.set_dead_channels(dead_channels)

    else:
        print('There are no dead channels in this recording, or dead_channels.txt is missing.')


def remove_dead_channels_from_geom_file_tetrode_by_tetrode(prm):
    file_path = prm.get_filepath()
    dead_ch_path = file_path + "\\dead_channels.txt"

    tetrode_channels = [1, 2, 3, 4]

    #todo write csv file according to dead channels

    if os.path.isfile(dead_ch_path) is True:
        dead_channels = prm.get_dead_channels()
        for channel in range(len(dead_channels)):
            ch_number = dead_channels[0][channel] % 4 # this is incorrect, it's still probably a list
            tetrode_channels.remove(ch_number)

        with open('geom.csv', 'w') as csvfile:
            for channel in tetrode_channels:
                fieldnames = ['channel_id', 'distance']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writerow({'channel_id': channel + 1, 'distance': 0})
    else:
        return
