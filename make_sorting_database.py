import os
import dead_channels
import file_utility
from shutil import copyfile


def write_bash_script_for_sorting(prm):
    # /run/user/1000/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=cmvm/sbms/groups/mnolan_NolanLab/ActiveProjects/Klara/open_field_setup/test_recordings/sorting_test
    name_of_dataset = prm.get_date()
    file_path_win = prm.get_filepath()
    main_path_win = ''

    if prm.is_windows():
        main_path_win = file_path_win.rsplit('\\', 3)[-4] + '\\'
    if prm.is_ubuntu():
        main_path_win = file_path_win.rsplit('/', 3)[-4] + '/'

    if os.path.isfile(main_path_win + "run_sorting.sh") is False:
        batch_writer = open(main_path_win + 'run_sorting.sh', 'w', newline='\n')
        batch_writer.write('#!/bin/bash\n')
        batch_writer.write('echo "-----------------------------------------------------------------------------------"\n')
        batch_writer.write('echo "This is a shell script that will hopefully run mountain sort on all recordings in the folder."\n')

    else:
        batch_writer = open(main_path_win + 'run_sorting.sh', 'a', newline='\n')

    for tetrode in range(4):
        data_folder_name_continuous = 't' + str(tetrode + 1)

        mountain_main_path = 'recordings/' + name_of_dataset + '/Electrophysiology/Spike_sorting/' + data_folder_name_continuous
        mountain_main_data_path = 'recordings/' + name_of_dataset + '/Electrophysiology/Spike_sorting/' + data_folder_name_continuous + '/data'

        mda_path = mountain_main_data_path + '/raw.mda'

        pipeline_path = mountain_main_path + '/mountainsort3.mlp'
        geom_path = mountain_main_data_path + '/geom.csv'
        firings_out_path = mountain_main_data_path + '/firings.mda'
        firings_out_curated_path = mountain_main_data_path + '/firings_curated.mda'
        pre_out_path = mountain_main_data_path + '/pre.mda'
        filt_out_path = mountain_main_data_path + '/filt.mda'
        params_path = mountain_main_path + '/params.json'
        metrics_path = mountain_main_path + '/cluster_metrics.json'

        batch_writer.write('echo "I am calling mountainsort now for tetrode {0}, {1}."\n'.format(tetrode + 1, name_of_dataset))

        sort_command = 'mlp-run ' + pipeline_path + ' sort' + ' --raw=' + mda_path + ' --geom=' + geom_path + ' --firings_out=' + firings_out_path + ' --pre_out=' + pre_out_path + ' --filt_out=' + filt_out_path + ' --_params=' + params_path

        batch_writer.write(sort_command + '\n')

        sort_command_curate = 'mlp-run ' + pipeline_path + ' sort' + ' --raw=' + mda_path + ' --geom=' + geom_path + ' --firings_out=' + firings_out_curated_path + ' --_params=' + params_path + ' --curate=true' + ' --cluster_metrics_out=' + metrics_path

        batch_writer.write('echo "Now with curation."\n')

        batch_writer.write(sort_command_curate + '\n')


def write_bash_script_for_sorting_all_tetrodes(prm):
    # /run/user/1000/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=cmvm/sbms/groups/mnolan_NolanLab/ActiveProjects/Klara/open_field_setup/test_recordings/sorting_test
    name_of_dataset = prm.get_date()
    file_path_win = prm.get_filepath()
    if prm.get_is_windows():
        main_path_win = file_path_win.rsplit('\\', 3)[-4] + '\\'
    if prm.get_is_ubuntu():
        main_path_win = file_path_win.rsplit('/', 3)[-4] + '/'


    if os.path.isfile(main_path_win + "run_sorting.sh") is False:
        batch_writer = open(main_path_win + 'run_sorting.sh', 'w', newline='\n')
        batch_writer.write('#!/bin/bash\n')
        batch_writer.write('echo "-----------------------------------------------------------------------------------"\n')
        batch_writer.write('echo "This is a shell script that will hopefully run mountain sort on all recordings in the folder."\n')

    else:
        batch_writer = open(main_path_win + 'run_sorting.sh', 'a', newline='\n')


    data_folder_name_all_ch = 'all_tetrodes'

    mountain_main_path = 'recordings/' + name_of_dataset + '/Electrophysiology/Spike_sorting/' + data_folder_name_all_ch
    mountain_main_data_path = 'recordings/' + name_of_dataset + '/Electrophysiology/Spike_sorting/' + data_folder_name_all_ch + '/data'

    mda_path = mountain_main_data_path + '/raw.mda'

    pipeline_path = mountain_main_path + '/mountainsort3.mlp'
    geom_path = mountain_main_data_path + '/geom_all_tetrodes.csv'
    firings_out_path = mountain_main_data_path + '/firings.mda'
    firings_out_curated_path = mountain_main_data_path + '/firings_curated.mda'
    pre_out_path = mountain_main_data_path + '/pre.mda'
    filt_out_path = mountain_main_data_path + '/filt.mda'
    metrics_path = mountain_main_path + '/cluster_metrics.json'

    params_path = mountain_main_path + '/params.json'

    batch_writer.write('echo "I am calling mountainsort now for all tetrodes combined, {0}."\n'.format(name_of_dataset))

    sort_command = 'mlp-run ' + pipeline_path + ' sort' + ' --raw=' + mda_path + ' --geom=' + geom_path + ' --firings_out=' + firings_out_path + ' --pre_out=' + pre_out_path + ' --filt_out=' + filt_out_path + ' --_params=' + params_path

    batch_writer.write(sort_command + '\n')

    sort_command_curate = 'mlp-run ' + pipeline_path + ' sort' + ' --raw=' + mda_path + ' --geom=' + geom_path + ' --firings_out=' + firings_out_curated_path + ' --_params=' + params_path + ' --curate=true' + ' --cluster_metrics_out=' + metrics_path

    batch_writer.write('echo "Now with curation."\n')

    batch_writer.write(sort_command_curate + '\n')


def create_sorting_folder_structure_separate_tetrodes(prm):
    main_path = file_utility.get_main_path(prm)
    spike_path = prm.get_spike_path()

    for tetrode in range(4):
        dead_channels.remove_dead_channels_from_geom_file_tetrode_by_tetrode(prm, tetrode)
        data_folder_name = 't' + str(tetrode + 1)

        if prm.is_windows():
            current_folder_continuous = spike_path + '\\' + data_folder_name + '\\'
            sorting_folder = '\\sorting_files\\'
            data_path = 'data\\'
        if prm.is_ubuntu():
            current_folder_continuous = spike_path + '/' + data_folder_name + '/'
            sorting_folder = '/sorting_files/'
            data_path = 'data/'

        if os.path.exists(current_folder_continuous) is False:
            os.makedirs(current_folder_continuous)
        try:
            copyfile(main_path + sorting_folder + 'params.json', current_folder_continuous + 'params.json')
            copyfile(main_path + sorting_folder + 'params.json', current_folder_continuous + 'params.json')
            copyfile(main_path + sorting_folder + 'mountainsort3.mlp', current_folder_continuous + 'mountainsort3.mlp')

            copyfile(main_path + sorting_folder + 'params.json', current_folder_continuous + data_path + 'params.json')
            copyfile(main_path + sorting_folder + 'geom.csv', current_folder_continuous + data_path + 'geom.csv')
        except FileNotFoundError:
            print('Something is wrong with the sorting_files folder. '
                  'It should be in the same folder as the dataset, '
                  'and is should have params.json in there so that is can be copied to all folders.')

    write_bash_script_for_sorting(prm)


def create_sorting_folder_structure(prm):
    dead_channels.remove_dead_channels_from_geom_file_all_tetrodes(prm)
    main_path = file_utility.get_main_path(prm)

    spike_path = prm.get_spike_path()
    current_folder = ''
    data_path = ''
    sorting_folder = ''

    if prm.get_is_windows():
        current_folder = spike_path + '\\all_tetrodes\\'
        sorting_folder = '\\sorting_files\\'
        data_path = 'data\\'
    if prm.get_is_ubuntu():
        current_folder = spike_path + '/all_tetrodes/'
        sorting_folder = '/sorting_files/'
        data_path = 'data/'

    if os.path.exists(current_folder) is False:
        os.makedirs(current_folder)
    try:
        copyfile(main_path + sorting_folder + 'params.json', current_folder + 'params.json')
        copyfile(main_path + sorting_folder + 'params.json', current_folder + 'params.json')
        copyfile(main_path + sorting_folder + 'mountainsort3.mlp', current_folder + 'mountainsort3.mlp')

        copyfile(main_path + sorting_folder + 'params.json', current_folder + data_path + 'params.json')
        copyfile(main_path + sorting_folder + 'geom_all_tetrodes.csv', current_folder + data_path + 'geom.csv')
    except FileNotFoundError:
        print('Something is wrong with the sorting_files folder. '
              'It should be in the same folder as the dataset, '
              'and is should have params.json in there so that is can be copied to all folders.')

    write_bash_script_for_sorting_all_tetrodes(prm)
