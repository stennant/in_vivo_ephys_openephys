'''
Saves the corresponding signal arrays for beaconed, non-beaconed and probe trials.
In our virtual reality task, every every tenth trial is a probe trial, and every fifth trial that is not a probe trial
 is a non-beaconed trial. The rest of the trials are beaconed. In these functions, the indices for the different
trial types are separated and saved into beaconed, nbeaconed and probe arrays. If the arrays already exist, then the
data is loaded from the file (the location of this file is specified in init_params in main).
'''

import numpy as np
import os
import matplotlib.pylab as plt
import vr_process_movement
import file_reader
import parameters
import signal_for_indices


fr = file_reader.FileReader()

beaconed = None
nbeaconed = None
probe = None
trial_num = None


def keep_first_from_close_series(array, threshold):
    num_delete = 1
    while num_delete > 0:
        diff = np.ediff1d(array, to_begin= threshold + 1)
        to_delete = np.where(diff <= threshold)
        num_delete = len(to_delete[0])

        if num_delete > 0:
            array = np.delete(array, to_delete)

    return array

'''
Finds indices for beginning of outbound journey
input
    prm : object, parameters
    location : numpy array, location of animal
output
    output beginnings : numpy array, first indices in outbound region
'''


def get_outbound_beginning(prm, location):
    filepath = prm.get_filepath()
    if os.path.isfile(filepath + "Behaviour\\Data\\outbound.npy") is False:
        outbound_beginnings = get_outbound_beginning_indices(prm, location)
        np.save(filepath + "Behaviour\\Data\\outbound", outbound_beginnings)

    else:
        outbound_beginnings = np.load(filepath + "Behaviour\\Data\\outbound.npy")
    return outbound_beginnings


def get_outbound_beginning_indices(prm, location):
    outbound_border = prm.get_beginning_of_outbound()
    outbound = np.where((location >= outbound_border) & (location <= outbound_border + 4))
    outbound = np.asanyarray(outbound)
    outbound_plus_one = outbound + 1
    outbound_plus_one = np.asanyarray(outbound_plus_one)
    outbound_beginnings = np.setdiff1d(outbound, outbound_plus_one)
    return outbound_beginnings


def get_beginning_of_track_positions(prm, location):
    filepath = prm.get_filepath()
    if os.path.isfile(filepath + "Behaviour\\Data\\beginning_of_track.npy") is False:
        position = 0
        beginning_of_track = np.where((location >= position) & (location <= position + 4))
        beginning_of_track = np.asanyarray(beginning_of_track)
        beginning_plus_one = beginning_of_track + 1
        beginning_plus_one = np.asanyarray(beginning_plus_one)
        track_beginnings = np.setdiff1d(beginning_of_track, beginning_plus_one)
        track_beginnings = keep_first_from_close_series(track_beginnings, 30000)
        np.save(filepath + "Behaviour\\Data\\beginning_of_track", track_beginnings)

    else:
        track_beginnings = np.load(filepath + "Behaviour\\Data\\beginning_of_track.npy")

    return track_beginnings



'''
# Save indices for beaconed, non-beaconed, and probe trials separately
def beaconed_nbeaconed_probe(location):
    global beaconed
    global nbeaconed
    global probe
    global trial_num
    if beaconed is None:
        if os.path.isfile(prm.get_filepath() + "beaconed.npy") is False:
            beaconed = []
            nbeaconed = []
            probe = []
            trial_num = 1
            for i in range(len(location)):
                if i > 0 and (location[i-1]-location[i]) > 150:
                    trial_num += 1
                if trial_num % 10 == 0:
                    probe.append(i)
                elif trial_num % 5 == 0:
                    nbeaconed.append(i)
                else:
                    beaconed.append(int(i))
            np.save(prm.get_filepath() + "beaconed.npy", beaconed)
            np.save(prm.get_filepath() + "nbeaconed.npy", nbeaconed)
            np.save(prm.get_filepath() + "probe.npy", probe)
            np.save(prm.get_filepath() + "trial_num.npy", trial_num)
        else:
            beaconed = np.load(prm.get_filepath() + "beaconed.npy")
            nbeaconed = np.load(prm.get_filepath() + "nbeaconed.npy")
            probe = np.load(prm.get_filepath() + "probe.npy")
            trial_num = np.load(prm.get_filepath() + "trial_num.npy")
    return beaconed, nbeaconed, probe, trial_num
'''


def beaconed_nbeaconed_probe(prm, location):
    global beaconed
    global nbeaconed
    global probe
    global trial_num
    if os.path.isfile(prm.get_behaviour_data_path() + "\\beaconed.npy") is False:
        beaconed = []
        nbeaconed = []
        probe = []
        trial_num = 1
        for i in range(len(location)):
            if i > 0 and (location[i-1]-location[i]) > 150:
                trial_num += 1
            if trial_num % 10 == 0:
                probe.append(i)
            elif trial_num % 5 == 0:
                nbeaconed.append(i)
            else:
                beaconed.append(int(i))
        print(len(beaconed))
        print(len(nbeaconed))
        print(len(probe))
        np.save(prm.get_filepath() + "Behaviour\\Data\\beaconed.npy", beaconed)
        np.save(prm.get_filepath() + "Behaviour\\Data\\nbeaconed.npy", nbeaconed)
        np.save(prm.get_filepath() + "Behaviour\\Data\\probe.npy", probe)
        np.save(prm.get_filepath() + "Behaviour\\Data\\trial_num.npy", trial_num)
    else:
        beaconed = np.load(prm.get_filepath() + "Behaviour\\Data\\beaconed.npy")
        nbeaconed = np.load(prm.get_filepath() + "Behaviour\\Data\\nbeaconed.npy")
        probe = np.load(prm.get_filepath() + "Behaviour\\Data\\probe.npy")
        trial_num = np.load(prm.get_filepath() + "Behaviour\\Data\\trial_num.npy")
    return beaconed, nbeaconed, probe, trial_num




# If beaconed, non-beaconed and probe arrays don't exist, the functions to create them are called here
def cached_trial_type(prm, channel, filepath, location, raw_data):
    if os.path.isfile(prm.get_filepath() + "Behaviour\\Data\\beaconed.npy") is False or os.path.isfile(filepath + "Behaviour\\Data\\probe.npy") is False:
        beaconed_trials, nbeaconed_trials, probe_trials, trial_number = beaconed_nbeaconed_probe(location)
        np.save(prm.get_filepath() + "Behaviour\\Data\\beaconed", beaconed_trials)
        np.save(prm.get_filepath() + "Behaviour\\Data\\nbeaconed", nbeaconed_trials)
        np.save(prm.get_filepath() + "Behaviour\\Data\\probe", probe_trials)
        beaconed_signal = signal_for_indices.signal_for_indices(channel, raw_data, beaconed_trials)
        nbeaconed_signal = signal_for_indices.signal_for_indices(channel, raw_data, nbeaconed_trials)
        probe_signal = signal_for_indices.signal_for_indices(channel, raw_data, probe_trials)
        np.save(prm.get_filepath() + "Behaviour\\Data\\beaconed_signal", beaconed_signal)
        np.save(prm.get_filepath() + "Behaviour\\Data\\nbeaconed_signal", nbeaconed_signal)
        np.save(prm.get_filepath() + "Behaviour\\Data\\probe_signal", probe_signal)
    else:
        beaconed_trials = np.load(prm.get_filepath() + "Behaviour\\Data\\beaconed.npy")
        nbeaconed_trials = np.load(prm.get_filepath() + "Behaviour\\Data\\nbeaconed.npy")
        probe_trials = np.load(prm.get_filepath() + "Behaviour\\Data\\probe.npy")
        beaconed_signal = np.load(prm.get_filepath() + "Behaviour\\Data\\beaconed_signal.npy")
        nbeaconed_signal = np.load(prm.get_filepath() + "Behaviour\\Data\\nbeaconed_signal.npy")
        probe_signal = np.load(prm.get_filepath() + "Behaviour\\Data\\probe_signal.npy")
    return beaconed_trials, beaconed_signal, nbeaconed_trials, nbeaconed_signal, probe_trials, probe_signal


# Calculate beaconed, non-beaconed and probe trial indices, and save them if they don't exist yet
def save_or_open_trial_arrays(prm, filepath, channel):
    # Check for empty files and delete them if there are any
    for file in os.listdir(filepath + 'Behaviour\\Data'):
        os.chdir(filepath)
        if file.endswith(".npy") and os.path.getsize(file) == 0:
            print('---FILE ERROR: The size of '+file+' is 0, something is wrong.---')

    beaconed_trials, beaconed_signal, nbeaconed_trials, nbeaconed_signal, probe_trials, probe_signal \
        = cached_trial_type(prm, channel, filepath, vr_process_movement.get_normalised_location_metric(fr.get_raw_data))

    return beaconed_trials, nbeaconed_trials, probe_trials, beaconed_signal, nbeaconed_signal, probe_signal
