import os


def get_dead_channel_ids(prm):
    file_path = prm.get_filepath()
    dead_ch_path = file_path + "\\dead_channels.txt"

    if os.path.isfile(dead_ch_path) is True:
        dead_channel_reader = open(dead_ch_path, 'r')
        dead_channels = dead_channel_reader.readlines()
        dead_channels = [x.strip() for x in dead_channels]
        #todo: put dead channels in parameters, and skip them when sorting

    else:
        print('There are no dead channels in this recording.')
