# check what's in to_sort
# put progress.txt in there if it doesn't exist, and indicate stage
# look at checksum and only progress if that is good
# call main_kzg to do pre-processing, update progress.txt
# call run_sorting.sh
# update progress.txt
# call matlab script - this will remove the file

import os
import subprocess
import time

import pre_process_ephys_data


def check_folder():
    sorting_path = '/home/nolanlab/to_sort/recordings/'
    for dir, sub_dirs, files in os.walk(sorting_path):
        if not files:
            to_sort = False
        else:
            to_sort = True
            print('I found something, and I will try to sort it now.')
            return to_sort
    return to_sort


def monitor_to_sort():
    start_time = time.time()
    time_to_wait = 60.0
    to_sort = False
    while True:
        print('I am checking whether there is something to sort.')
        to_sort = check_folder()

        if to_sort is True:
            pre_process_ephys_data.main()
            print('I finished pre-processing the first recording. I will call MountainSort now.')
            os.chmod('/home/nolanlab/to_sort/run_sorting.sh', 484)

            subprocess.call('/home/nolanlab/to_sort/run_sorting.sh', shell=True)
            os.remove('/home/nolanlab/to_sort/run_sorting.sh')

            print('MS is done')
            # call matlab
            # if vr call Sarah's script
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