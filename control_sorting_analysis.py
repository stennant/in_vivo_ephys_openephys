# check what's in to_sort
# put progress.txt in there if it doesn't exist, and indicate stage
# look at checksum and only progress if that is good
# call main_kzg to do pre-processing, update progress.txt
# call run_sorting.sh
# update progress.txt
# call matlab script - this will remove the file

import glob
import os
import subprocess
import time

import pre_process_ephys_data

sorting_folder = '/home/nolanlab/to_sort/recordings/'


def check_folder():
    sorting_path = sorting_folder
    for dir, sub_dirs, files in os.walk(sorting_path):
        if not files:
            to_sort = False
        else:
            to_sort = True
            print('I found something, and I will try to sort it now.')
            return to_sort
    return to_sort


def find_sorting_directory():
    for name in glob.glob(sorting_folder + '*'):
        os.path.isdir(name)
        return name


def checksum():
    pass


# return whether it is vr or openfield
def get_session_type(recording_directory):
    parameters_path = recording_directory + 'parameters.txt'
    param_file_reader = open(parameters_path, 'r')
    parameters = param_file_reader.readlines()
    parameters = list([x.strip() for x in parameters])
    if parameters[0][0] == 'vr':
        is_vr = True
        is_open_field = False
    else:
        is_vr = False
        is_open_field = True
    return is_vr, is_open_field


def get_location_on_server(recording_directory):
    parameters_path = recording_directory + 'parameters.txt'
    param_file_reader = open(parameters_path, 'r')
    parameters = param_file_reader.readlines()
    parameters = list([x.strip() for x in parameters])
    location_on_server = parameters[0][1]
    return location_on_server


def call_spike_sorting_analysis_scripts():
    # read param file and check session type and location on server

    recording_to_sort = find_sorting_directory()
    is_vr, is_open_field = get_session_type(recording_to_sort)
    location_on_server = get_location_on_server(recording_to_sort)


    pre_process_ephys_data.pre_process_data(recording_to_sort)
    print('I finished pre-processing the first recording. I will call MountainSort now.')
    os.chmod('/home/nolanlab/to_sort/run_sorting.sh', 484)

    subprocess.call('/home/nolanlab/to_sort/run_sorting.sh', shell=True)
    os.remove('/home/nolanlab/to_sort/run_sorting.sh')

    print('MS is done')
    # call matlab
    # if vr call Sarah's script


def monitor_to_sort():
    start_time = time.time()
    time_to_wait = 60.0
    while True:
        print('I am checking whether there is something to sort.')
        to_sort = check_folder()

        if to_sort is True:
            # look at checksum and only proceed if it's okay, otherwise wait

            call_spike_sorting_analysis_scripts()
        else:
            print('Nothing to sort. I will check again in 1 minute.')
            time.sleep(time_to_wait - ((time.time() - start_time) % time_to_wait))


def main():
    print('-------------------------------------------------------------')
    print('This is a script that controls running the spike sorting analysis.')
    print('-------------------------------------------------------------')

    monitor_to_sort()


if __name__ == '__main__':
    main()