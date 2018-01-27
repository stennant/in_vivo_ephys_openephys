import glob
import os
import shutil
import subprocess
import sys
import time

import pre_process_ephys_data

sorting_folder = '/home/nolanlab/to_sort/recordings/'
server_path_first_half = '/run/user/1001/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=cmvm/sbms/groups/mnolan_NolanLab/ActiveProjects/'


def check_folder():
    sorting_path = sorting_folder
    to_sort = False
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
    parameters_path = recording_directory + '/parameters.txt'
    param_file_reader = open(parameters_path, 'r')
    parameters = param_file_reader.readlines()
    parameters = list([x.strip() for x in parameters])
    session_type = parameters[0]
    if session_type == 'vr':
        is_vr = True
        is_open_field = False
    elif session_type == 'openfield':
        is_vr = False
        is_open_field = True
    else:
        print('Session type is not specified. '
              'You need to write vr or openfield in the first line of the parameters.txt file. '
              'You put {} there.'.format(session_type))
        is_vr = False
        is_open_field = False
    return is_vr, is_open_field


def get_location_on_server(recording_directory):
    parameters_path = recording_directory + '/parameters.txt'
    param_file_reader = open(parameters_path, 'r')
    parameters = param_file_reader.readlines()
    parameters = list([x.strip() for x in parameters])
    location_on_server = parameters[1]
    return location_on_server


def call_spike_sorting_analysis_scripts(recording_to_sort):
    try:
        is_vr, is_open_field = get_session_type(recording_to_sort)
        location_on_server = get_location_on_server(recording_to_sort)  # I can give this to Tizzy

        sys.stdout = open(server_path_first_half + location_on_server + '/sorting_log.txt', 'w')

        pre_process_ephys_data.pre_process_data(recording_to_sort)

        print('I finished pre-processing the first recording. I will call MountainSort now.')
        os.chmod('/home/nolanlab/to_sort/run_sorting.sh', 484)

        subprocess.call('/home/nolanlab/to_sort/run_sorting.sh', shell=True)
        os.remove('/home/nolanlab/to_sort/run_sorting.sh')

        print('MS is done')
        # call matlab. input: vr/not vr, location on server + file location on sorting computer
        print('Post-processing in Matlab is done.')

        if is_vr:
            print('This is a VR session, so I will run the VR related analyses now.')
            # todo if vr, call Sarah's script
            pass
    except Exception as ex:
        print('There is a problem with this file. '
              'I will move on to the next one. This is what Python says happened:')
        print(ex)
        shutil.rmtree(recording_to_sort)


def monitor_to_sort():
    start_time = time.time()
    time_to_wait = 60.0
    while True:
        print('I am checking whether there is something to sort.')
        to_sort = check_folder()

        if to_sort is True:
            recording_to_sort = find_sorting_directory()
            # todo: look at checksum and only proceed if it's okay, otherwise wait
            call_spike_sorting_analysis_scripts(recording_to_sort)

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