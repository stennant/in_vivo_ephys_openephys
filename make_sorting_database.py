import os
from shutil import copyfile


def write_batch_file_for_sorting(prm):
    # /run/user/1000/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=cmvm/sbms/groups/mnolan_NolanLab/ActiveProjects/Klara/open_field_setup/test_recordings/sorting_test
    create_sorting_folder_structure(prm)
    name_of_dataset = prm.get_date()
    file_path = prm.get_filepath()
    main_folder_name = file_path.rsplit('\\', 3)[-3]
    main_path = file_path.rsplit('\\', 3)[-4]

    if os.path.isfile(main_path + main_folder_name + "\\" + "\\run_sorting.sh") is False:
        batch_writer = open(main_path + '\\run_sorting.sh', 'w', newline='\n')
        batch_writer.write('#!/bin/bash\n')
        batch_writer.write('echo "-----------------------------------------------------------------------------------"\n')
        batch_writer.write('echo "This is a shell script that will run mountain sort on all recordings in the folder."\n')

        export_path = 'export PATH=~/mountainlab/bin:$PATH\n'
        batch_writer.write(export_path)
    else:
        batch_writer = open(main_path + '\\run_sorting.sh', 'a', newline='\n')

    for tetrode in range(4):
        data_folder_name = 't' + str(tetrode + 1) + '_' + name_of_dataset

        tetrode_mda_path = file_path + '/Electrophysiology/Spike_sorting/' + data_folder_name
        tetrode_prv_path = main_path + '/' + main_folder_name + '_sort/' + data_folder_name
        mda_file_name = '/raw.nt' + str(tetrode + 1) + '.mda'
        prv_file_name = '/raw.mda.prv'

        batch_writer.write('echo "I am making prv files now."\n')

        create_prv = 'prv-create ' + tetrode_mda_path + mda_file_name + ' ' + tetrode_prv_path + prv_file_name + '\n'
        create_prv = create_prv.replace("\\", "/")
        batch_writer.write(create_prv)

        batch_writer.write('echo "I am calling mountainsort now."\n')
        batch_writer.write('kron-run ms3 ' + main_folder_name + '_sort\n')


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
        line = data_folder_name + ' ' + main_folder_name + '_sort/' + data_folder_name
        print(line)
        datasets_writer.write(line)
        datasets_writer.write('\n')

    datasets_writer.close()
    return


def create_sorting_folder_structure(prm):
    file_path = prm.get_filepath()
    name_of_dataset = prm.get_date()
    main_folder_name = file_path.rsplit('\\', 3)[-3]
    main_path = file_path.rsplit('\\', 3)[-4]
    mountain_sort_folders = main_path + '\\' + main_folder_name + '_sort'
    prm.set_mountain_sort_path(mountain_sort_folders)

    if os.path.exists(mountain_sort_folders) is False:
        os.makedirs(mountain_sort_folders)

    for tetrode in range(4):
        data_folder_name = 't' + str(tetrode + 1) + '_' + name_of_dataset
        current_folder = main_path + '\\' + main_folder_name + '_sort\\' + data_folder_name

        if os.path.exists(current_folder) is False:
            os.makedirs(current_folder)
            try:
                copyfile(main_path + '\\sorting_files\\params.json', current_folder + '\\params.json')
            except FileNotFoundError:
                print('Something is wrong with the sorting_files folder. '
                      'It should be in the same folder as the dataset, '
                      'and is should have params.json in there so that is can be copied to all folders.')


def create_sorting_environment(prm):
    write_dataset_txt_file(prm)
    write_batch_file_for_sorting(prm)
