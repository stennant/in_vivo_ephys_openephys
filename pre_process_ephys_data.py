import convert_open_ephys_to_mda
import dead_channels
import file_utility
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
    prm.set_continuous_file_name('100_CH')
    prm.set_continuous_file_name_end('')
    prm.set_waveform_size(40)  # number of sampling points to take when taking waveform for spikes (1ms)

    prm.set_track_length(200)
    prm.set_beginning_of_outbound(30)
    prm.set_reward_zone(90)


def init_open_field_params():
    prm.set_movement_ch('100_ADC2.continuous')
    prm.set_opto_ch('100_ADC3.continuous')
    # file_utility.init_data_file_names(prm, '105_CH', '_0')  # old files
    # file_utility.init_data_file_names(prm, '100_CH', '')  # currently used (2018)
    prm.set_waveform_size(40)


def init_params():
    # prm.set_filepath('C:\\Users\\s1466507\\Documents\\mountain_sort_tmp\\open_field_test\\recordings\\')
    # prm.set_filepath('\\\\cmvm.datastore.ed.ac.uk\\cmvm\\sbms\\groups\\mnolan_NolanLab\\ActiveProjects\\Klara\\open_field_setup\\sync_test\\recordings\\')
    # prm.set_filepath('/run/user/1001/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=cmvm/sbms/groups/mnolan_NolanLab/ActiveProjects/Klara/open_field_setup/sync_test/recordings/')

    # rat test data
    # prm.set_filepath('/run/user/1001/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=cmvm/sbms/groups/mnolan_NolanLab/ActiveProjects/Klara/open_field_setup/rat_test/recordings/')
    prm.set_filepath('/home/nolanlab/rat_test/recordings')
    prm.set_filepath('/home/nolanlab/sync_test/recordings')

    # prm.set_filepath('\\\\cmvm.datastore.ed.ac.uk\\cmvm\\sbms\\groups\\mnolan_NolanLab\\ActiveProjects\\Tizzy\\Cohort3\\TestProject\\recordings\\')
    # prm.set_filepath('\\\\cmvm.datastore.ed.ac.uk\\cmvm\\sbms\\groups\\mnolan_NolanLab\\ActiveProjects\\Sarah\\Test_for_Klara\\recordings\\')
    # prm.set_filepath('D:\\sort\\mountain_test\\open_field_test\\recordings\\')

    prm.set_sampling_rate(30000)
    prm.set_num_tetrodes(4)

    prm.set_is_open_field(True)

    prm.set_is_ubuntu(True)
    prm.set_is_windows(False)

    if prm.is_vr is True:
        init_vr_params()

    if prm.is_open_field is True:
        init_open_field_params()

    # These are not exclusive, both can be True for the same recording - that way it'll be sorted twice
    prm.set_is_tetrode_by_tetrode(True)  # set to True if you want the spike sorting to be done tetrode by tetrode
    prm.set_is_all_tetrodes_together(False)  # set to True if you want the spike sorting done on all tetrodes combined


def process_a_dir(dir_name):
    print('')
    print('')
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
          '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
          '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
          '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print('')
    print('All folders in {} will be processed.'.format(dir_name))
    if prm.get_is_windows():
        prm.set_date(dir_name.rsplit('\\', 2)[-2])
    if prm.get_is_ubuntu():
        prm.set_date(dir_name.rsplit('/', 2)[-2])

    prm.set_filepath(dir_name)
    file_utility.set_continuous_data_path(prm)

    dead_channels.get_dead_channel_ids(prm)  # read dead_channels.txt
    file_utility.create_folder_structure(prm)

    if prm.get_is_tetrode_by_tetrode() is True:
        print('------------------------------------------')
        print('I am making one mda file for each tetrode.')
        print('------------------------------------------')
        make_sorting_database.create_sorting_folder_structure_separate_tetrodes(prm)
        convert_open_ephys_to_mda.convert_continuous_to_mda(prm)
        print('All 4 tetrodes were converted to separate mda files.')
        print('*****************************************************')

    if prm.get_is_all_tetrodes_together() is True:
        print('-------------------------------------------------------------------------')
        print('I am converting all channels into one mda file. This will take some time.')
        print('-------------------------------------------------------------------------')
        make_sorting_database.create_sorting_folder_structure(prm)
        convert_open_ephys_to_mda.convert_all_tetrodes_to_mda(prm)
        print('The big mda file is created, it is in Electrophysiology/Spike_sorting/all_tetrodes/data')
        print('***************************************************************************************')

    if prm.is_vr is True:
        vr_process_movement.save_or_open_movement_arrays(prm)

    # process_optogenetics.process_opto(prm)


def process_files():
    if prm.get_is_windows():
        for name in glob.glob(prm.get_filepath() + '*'):
            os.path.isdir(name)
            process_a_dir(name + '\\')

    if prm.get_is_ubuntu():
        for name in glob.glob(prm.get_filepath() + '/*'):
            os.path.isdir(name)
            process_a_dir(name + '/')
            break  # this is here so it only does the first file for now


def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    init_params()
    process_files()


if __name__ == '__main__':
    main()