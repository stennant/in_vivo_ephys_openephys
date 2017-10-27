import convert_open_ephys_to_mda
import glob
import os
import parameters


prm = parameters.Parameters()

'''
Initializes parameters
    filepath : string, location of raw data file
    filename : string, name of raw data file (without raw.kwd extension)
    good_channels : int, list, channels that are not dead
    stop_threshold : float, given in cm/200ms.
        example:
        0.7cm/200ms = 0.7(1/200cm)/ms = 0.7(1000/200cm/s) = 0.7(5cm/s) = 0.7/5 cm/s
    num_channels : int, number of recording channels
    movement_ch : channel number for movement information
'''

def init_params():
    prm.set_filepath('C:\\Users\\s1466507\\Documents\\Ephys\\test_VR_opto\\')

    # f prm.set_filename('TT3.spikes')
    prm.set_file(prm.get_filepath(), prm.get_filename())
    prm.set_num_tetrodes(4)

    # - 30 cm black box;60 cm outbound journey;20 cm reward zone;60 cm outbound journey;30 cm black box
    prm.set_stop_threshold(0.7/5)  # speed is given in cm/200ms 0.7*1/2000
    prm.set_num_channels(16)
    prm.set_movement_ch(20) # this won't work anymore
    prm.set_waveform_size(40)  # number of sampling points to take when taking waveform for spikes (1ms)

    prm.set_sampling_rate(30000)


def process_a_dir(dir_name):
    print('All folders in {} will be processed.'.format(dir_name))
    prm.set_filepath(dir_name)
    convert_open_ephys_to_mda.convert_spk_to_mda(prm)

    # read and process location info
    # read opto light


def process_files():
    for name in glob.glob(prm.get_filepath()+'*'):
        os.path.isdir(name)
        process_a_dir(name + '\\')


def main():
    print('-------------------------------------------------------------')
    print('Check whether the arrays have the correct size in the folder. '
          'An incorrect array only gets deleted automatically if its size is 0. Otherwise, '
          'it needs to be deleted manually in order for it to be generated again.')
    print('-------------------------------------------------------------')

    init_params()
    process_files()

if __name__ == '__main__':
    main()