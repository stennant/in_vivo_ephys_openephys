import os
from shutil import copyfile


# this is for the 2017 November version of ms
def organize_files_for_ms(prm):
    file_path = prm.get_filepath()
    main_path = file_path.rsplit('\\', 3)[-4]
    spike_path = prm.get_spike_path()
    mountain_path = spike_path + '\\all_tetrodes'
    mountain_path_data = mountain_path + '\\data\\'


    try:
        copyfile(main_path + '\\sorting_files\\params.json', mountain_path + '\\params.json')
        copyfile(main_path + '\\sorting_files\\mountainsort3.mlp', mountain_path + '\\mountainsort3.mlp')

        copyfile(main_path + '\\sorting_files\\params.json', mountain_path_data + '\\params.json')
        copyfile(main_path + '\\sorting_files\\geom.csv', mountain_path_data + '\\geom.csv')

    except FileNotFoundError:
        print('Something is wrong with the sorting_files folder. '
              'It should be in the same folder as the dataset. ')





# ms3 version
def write_batch_file_for_sorting(prm):
    # /run/user/1000/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=cmvm/sbms/groups/mnolan_NolanLab/ActiveProjects/Klara/open_field_setup/test_recordings/sorting_test
    create_sorting_folder_structure(prm)
    name_of_dataset = prm.get_date()
    file_path_win = prm.get_filepath()
    file_path_linux = file_path_win.split('\\', 3)[3]
    file_path_linux = '/run/user/1000/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=' + file_path_linux

    main_folder_name = file_path_win.rsplit('\\', 3)[-3]
    main_path_win = file_path_win.rsplit('\\', 3)[-4]
    main_path = main_path_win.split('\\', 3)[3]
    main_path = '/run/user/1000/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=' + main_path

    if os.path.isfile(main_path_win + "\\run_sorting.sh") is False:
        batch_writer = open(main_path_win + '\\run_sorting.sh', 'w', newline='\n')
        batch_writer.write('#!/bin/bash\n')
        batch_writer.write('echo "-----------------------------------------------------------------------------------"\n')
        batch_writer.write('echo "This is a shell script that will run mountain sort on all recordings in the folder."\n')

        export_path = 'export PATH=~/mountainlab/bin:$PATH\n'
        batch_writer.write(export_path)
    else:
        batch_writer = open(main_path_win + '\\run_sorting.sh', 'a', newline='\n')

    for tetrode in range(4):
        data_folder_name = 't' + str(tetrode + 1) + '_' + name_of_dataset
        data_folder_name_continuous = 't' + str(tetrode + 1) + '_' + name_of_dataset + '_continuous'

        tetrode_mda_path = file_path_linux + '/Electrophysiology/Spike_sorting/' + data_folder_name
        tetrode_mda_path_continuous = file_path_linux + '/Electrophysiology/Spike_sorting/' + data_folder_name + '_continuous'

        tetrode_prv_path = main_path + '/datasets/' + data_folder_name
        tetrode_prv_path_continuous = '/datasets/' + data_folder_name + '_continuous'

        mda_file_name = '/raw.nt' + str(tetrode + 1) + '.mda'
        prv_file_name = '/raw.mda.prv'

        batch_writer.write('echo "I am making prv files now."\n')

        create_prv = 'prv-create ' + tetrode_mda_path + mda_file_name + ' ' + tetrode_prv_path + prv_file_name + '\n'
        create_prv = create_prv.replace("\\", "/")
        create_prv = create_prv.replace("//", "/")
        batch_writer.write(create_prv)

        create_prv_continuous = 'prv-create ' + tetrode_mda_path_continuous + mda_file_name + ' ' + tetrode_prv_path_continuous + prv_file_name + '\n'
        create_prv_continuous = create_prv_continuous.replace("\\", "/")
        create_prv_continuous = create_prv_continuous.replace("//", "/")
        batch_writer.write(create_prv_continuous)

        batch_writer.write('echo "I am calling mountainsort now."\n')
        batch_writer.write('kron-run ms3 ' + data_folder_name + '\n')

        batch_writer.write('kron-run ms3 ' + data_folder_name_continuous + '\n')


def write_dataset_txt_file(prm):
    create_sorting_folder_structure(prm)
    name_of_dataset = prm.get_date()
    file_path = prm.get_filepath()
    main_folder_name = file_path.rsplit('\\', 3)[-3]
    main_path = file_path.rsplit('\\', 3)[-4]

    if os.path.isfile(main_path + "\\datasets.txt") is False:
        datasets_writer = open(main_path + '\\datasets.txt', 'w')
    else:
        datasets_writer = open(main_path + '\\datasets.txt', 'a')

    for tetrode in range(4):
        data_folder_name = 't' + str(tetrode + 1) + '_' + name_of_dataset
        line = data_folder_name + ' ' + 'datasets/' + data_folder_name
        line_continuous = data_folder_name + '_continuous ' + 'datasets/' + data_folder_name + '_continuous '

        print(line)
        datasets_writer.write(line)
        datasets_writer.write('\n')
        datasets_writer.write(line_continuous)
        datasets_writer.write('\n')

    datasets_writer.close()
    return


def create_sorting_folder_structure(prm):
    file_path = prm.get_filepath()
    name_of_dataset = prm.get_date()
    main_folder_name = file_path.rsplit('\\', 3)[-3]
    main_path = file_path.rsplit('\\', 3)[-4]
    mountain_sort_folders = main_path + '\\' + '/datasets/'
    prm.set_mountain_sort_path(mountain_sort_folders)
    spike_path = prm.get_spike_path()

    if os.path.exists(mountain_sort_folders) is False:
        os.makedirs(mountain_sort_folders)

    # copyfile(main_path + '\\sorting_files\\curation.script', main_path + '\\curation.script')
    # copyfile(main_path + '\\sorting_files\\pipelines.txt', main_path + '\\pipelines.txt')

    for tetrode in range(4):
        data_folder_name = 't' + str(tetrode + 1) + '_' + name_of_dataset
        current_folder = spike_path + '\\' + data_folder_name
        current_folder_continuous = spike_path + '\\' + data_folder_name + '_continuous'

        if os.path.exists(current_folder_continuous) is False:
            os.makedirs(current_folder)
            os.makedirs(current_folder_continuous)
        try:
            copyfile(main_path + '\\sorting_files\\params.json', current_folder + '\\params.json')
            copyfile(main_path + '\\sorting_files\\params.json', current_folder_continuous + '\\params.json')
            copyfile(main_path + '\\sorting_files\\params.json', current_folder_continuous + '\\params.json')
            copyfile(main_path + '\\sorting_files\\mountainsort3.mlp', current_folder_continuous + '\\mountainsort3.mlp')

            copyfile(main_path + '\\sorting_files\\params.json', current_folder_continuous + '\\data\\params.json')
            copyfile(main_path + '\\sorting_files\\geom.csv', current_folder_continuous + '\\data\\geom.csv')
        except FileNotFoundError:
            print('Something is wrong with the sorting_files folder. '
                  'It should be in the same folder as the dataset, '
                  'and is should have params.json in there so that is can be copied to all folders.')


def create_sorting_environment(prm):
    write_dataset_txt_file(prm)
    write_batch_file_for_sorting(prm)
