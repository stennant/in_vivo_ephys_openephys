import os


def write_dataset_txt_file(prm):
    create_sorting_folder_structure(prm)
    name_of_dataset = prm.get_date()
    file_path = prm.get_filepath()
    main_folder_name = file_path.rsplit('\\', 3)[-3]
    main_path = file_path.rsplit('\\', 3)[-4]

    if os.path.isfile(main_folder_name + '_sort' + "\\datasets.txt") is False:
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
