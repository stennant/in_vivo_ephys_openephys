import gc
import glob
import os
import shutil
import subprocess
import sys
import time

import pre_process_ephys_data

mountainsort_tmp_folder = '/tmp'
sorting_folder = '/home/nolanlab/to_sort/recordings/'
server_path_first_half = '/run/user/1001/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=cmvm/sbms/groups/mnolan_NolanLab/ActiveProjects/'
# server_path_fist_half_matlab = 'smb://cmvm.datastore.ed.ac.uk/cmvm/sbms/groups/mnolan_NolanLab/ActiveProjects/'
matlab_params_file_path = '/home/nolanlab/PostClustering/'


def check_folder():
    sorting_path = sorting_folder
    recording_to_sort = False
    for dir, sub_dirs, files in os.walk(sorting_path):
        if not sub_dirs and not files:
            return recording_to_sort
        if not files:
            print('I am looking here: ', dir, sub_dirs)

        else:
            print('I found something, and I will try to sort it now.')
            recording_to_sort = find_sorting_directory()
            if recording_to_sort is False:
                return recording_to_sort
            else:
                return recording_to_sort


def find_sorting_directory():
    for name in glob.glob(sorting_folder + '*'):
        os.path.isdir(name)
        if check_if_recording_was_copied(name) is True:
            return name
        else:
            print('This recording was not copied completely, I cannot find copied.txt')
    return False


def check_if_recording_was_copied(recording_to_sort):
    if os.path.isfile(recording_to_sort + '/copied.txt') is True:
        return True
    else:
        return False


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


def write_param_file_for_matlab(file_to_sort, path_to_server, is_openfield, is_vr):
    if is_openfield:
        openfield = 1
    else:
        openfield = 0
    opto = 1
    params_for_matlab_file = open(matlab_params_file_path + "PostClusteringParams.txt", "w")
    params_for_matlab_file.write(file_to_sort + ',\n')
    params_for_matlab_file.write(server_path_first_half + path_to_server + ',\n')
    params_for_matlab_file.write(str(openfield) + ',\n')
    params_for_matlab_file.write(str(opto))
    params_for_matlab_file.close()


def write_shell_script_to_call_matlab(file_to_sort):
    script_path = file_to_sort + '/run_matlab.sh'
    batch_writer = open(script_path, 'w', newline='\n')
    batch_writer.write('#!/bin/bash\n')
    batch_writer.write('echo "-----------------------------------------------------------------------------------"\n')
    batch_writer.write('echo "This is a shell script that will call matlab."\n')
    batch_writer.write('export MATLABPATH=/home/nolanlab/PostClustering\n')

    batch_writer.write('matlab -r PostClusteringAuto')


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
        write_param_file_for_matlab(recording_to_sort, location_on_server, is_open_field, is_vr)
        write_shell_script_to_call_matlab(recording_to_sort)
        gc.collect()
        os.chmod(recording_to_sort + '/run_matlab.sh', 484)
        subprocess.call(recording_to_sort + '/run_matlab.sh', shell=True)

        # call matlab. input: vr/not vr, location on server + file location on sorting computer
        # matlab -r 'PostClusteringAuto(path,outfile,OpenField,Opto)

        print('Post-processing in Matlab is done.')
        shutil.rmtree(recording_to_sort)
        shutil.rmtree(mountainsort_tmp_folder)

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
        recording_to_sort = check_folder()

        if recording_to_sort is not False:
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