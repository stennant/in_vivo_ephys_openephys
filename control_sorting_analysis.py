# check what's in to_sort
# put progress.txt in there if it doesn't exist, and indicate stage
# look at checksum and only progress if that is good
# call main_kzg to do pre-processing, update progress.txt
# call run_sorting.sh
# update progress.txt
# call matlab script - this will remove the file

from os.path import isfile, join
from os import listdir
import time

import pre_process_ephys_data


def check_folder():
    sorting_path = '/home/nolanlab/to_sort/recordings'
    if any(isfile(join(sorting_path, i)) for i in listdir(sorting_path)):
        to_sort = True
    else:
        to_sort = False
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

            # call run_sorting
            # call matlab
            # if vr call Sarah's script
        else:
            print('Nothing to sort. I will check again in 1 minute.')
            time.sleep(time_to_wait - ((time.time() - start_time) % time_to_wait))


