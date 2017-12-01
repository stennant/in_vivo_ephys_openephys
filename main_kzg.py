import convert_open_ephys_to_mda
import glob
import make_sorting_database
import os
import parameters
import vr_process_movement
import process_optogenetics


prm = parameters.Parameters()


def init_vr_params():
    # - 30 cm black box;60 cm outbound journey;20 cm reward zone;60 cm outbound journey;30 cm black box
    prm.set_stop_threshold(0.7/5)  # speed is given in cm/200ms 0.7*1/2000
    prm.set_num_channels(16)
    prm.set_movement_ch('100_ADC2.continuous')
    prm.set_opto_ch('100_ADC3.continuous')
    prm.set_waveform_size(40)  # number of sampling points to take when taking waveform for spikes (1ms)

    prm.set_track_length(200)
    prm.set_beginning_of_outbound(30)
    prm.set_reward_zone(90)


def init_open_field_params():
    pass

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
    # prm.set_filepath('D:\\open_field_test\\test\\')
    prm.set_filepath('\\\\cmvm.datastore.ed.ac.uk\\cmvm\\sbms\\groups\\mnolan_NolanLab\\ActiveProjects\\Klara\\open_field_setup\\test_recordings\\sorting_test\\recordings\\')
    prm.set_sampling_rate(30000)

    # f prm.set_filename('TT3.spikes')
    prm.set_file(prm.get_filepath(), prm.get_filename())
    prm.set_num_tetrodes(4)

    prm.set_is_open_field(True)

    if prm.is_vr is True:
        init_vr_params()

    if prm.is_open_field is True:
        init_open_field_params()


def process_a_dir(dir_name):
    print('All folders in {} will be processed.'.format(dir_name))
    prm.set_date(dir_name.rsplit('\\', 2)[-2])
    prm.set_filepath(dir_name)
    make_sorting_database.create_sorting_environment(prm)

    convert_open_ephys_to_mda.convert_continuous_to_mda(prm)
    convert_open_ephys_to_mda.convert_spk_to_mda(prm)

    if prm.is_vr is True:
        vr_process_movement.save_or_open_movement_arrays(prm)

    process_optogenetics.process_opto(prm)


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