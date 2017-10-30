import os
import matplotlib.pylab as plt
import numpy as np
import trial_types

'''
Returns the first indices after the speed drops below threshold.
input
    prm : object, parameters
    speed : numpy array, speed
output
    stops : index where the mouse stopped (only first index after speed drops below threshold)
'''


def get_stop_times(prm, speed):
    stops = np.array([])
    filepath = prm.get_filepath()
    if os.path.isfile(prm.get_behaviour_data_path() + "\\stop_times.npy") is False:
        threshold = prm.get_stop_threshold()
        low_speed = np.where(speed < threshold)
        low_speed = np.asanyarray(low_speed)
        low_speed_plus_one = low_speed + 1
        intersect = np.intersect1d(low_speed, low_speed_plus_one)
        stops = np.setdiff1d(low_speed, intersect)
        np.save(prm.get_behaviour_data_path() + "\\stop_times", stops)

    else:
        stops = np.load(prm.get_behaviour_data_path() + "\\stop_times.npy")
    return stops


def print_first_stop_stats(prm, first_stops):
    location = np.load(prm.get_behaviour_data_path() + '\location.npy')
    first_stops = np.asanyarray(first_stops, dtype=int)
    locations_of_stops = (np.take(location, first_stops))
    plt.hist(locations_of_stops)

    average_first_stop = np.average(locations_of_stops)
    stdev_first_stops = np.std(locations_of_stops)

    print('Average first stop location is: {}'.format(average_first_stop))
    print('Standard deviation of first stop location is: {}'.format(stdev_first_stops))

'''
Returns an arrray of the indices where the animal first stopped after the beginning of the outbound journey
input
    outbound_beginnings : numpy array, indices where the outbound journeys began
    stops : numpy array, indices where the mouse stopped
output
    first_stops : numpy array, indices where the mouse first stopped after the beginning of every outbound journey.
If the mouse didn't stop for a whole trial, that index will be duplicated, as it is the first stop after two outbound
journeys.
'''


def get_first_stop_times(prm, outbound_beginnings, stops):
    movement_path = prm.get_filepath() + 'Behaviour'
    data_path = movement_path + '\\Data'
    analysis_path = movement_path + '\\Analysis'
    if os.path.exists(movement_path) is False:
        print('First stop data will be saved in {}.'.format(movement_path))
        os.makedirs(movement_path)
        os.makedirs(data_path)
        os.makedirs(analysis_path)

    filepath = prm.get_filepath()
    if os.path.isfile(filepath + "Behaviour\\Data\\first_stops.npy") is False:
        print('Finding stops and first stops.')
        # where stop is bigger, find nearest
        first_stops = np.array([])

        for i in range(len(outbound_beginnings)):
            stops_after = np.where(stops >= outbound_beginnings[i])
            stops_after = np.asanyarray(stops_after)
            if stops_after.size == 0:
                continue
            first_stop_index = int(stops_after[0][0])
            first_stop = stops[first_stop_index]
            first_stops = np.append(first_stops, first_stop)
        np.save(filepath + "Behaviour\\Data\\first_stops", first_stops)
        print_first_stop_stats(prm, first_stops)

    else:
        first_stops = np.load(filepath + "Behaviour\\Data\\first_stops.npy")

        print_first_stop_stats(prm, first_stops)
    return first_stops


def remove_extra_stops(min_distance, stops):
    to_remove = []
    for stop in range(len(stops) - 1):
        current_stop = stops[stop]
        next_stop = stops[stop + 1]
        if 0 <= (next_stop - current_stop) <= min_distance:
            to_remove.append(stop+1)

    filtered_stops = np.asanyarray(stops)
    np.delete(filtered_stops, to_remove)
    return filtered_stops


def get_data_for_stops_on_trials(prm):
    behaviour_path = prm.get_behaviour_data_path()
    number_of_trials = np.load(prm.get_behaviour_data_path() + '\\trial_num.npy')
    location = np.load(behaviour_path + '\\location.npy')
    all_stops = np.load(behaviour_path + '\\stop_times.npy')
    track_beginnings = trial_types.get_beginning_of_track_positions(prm, location)
    print('This mouse did {} trials.'.format(number_of_trials))

    return location, number_of_trials, all_stops, track_beginnings


def get_stops_on_trials_find_stops(location, number_of_trials, all_stops, track_beginnings):
    stops_on_trials = []
    location = np.asanyarray(location)
    number_of_trials = np.asanyarray(number_of_trials)
    all_stops = np.asanyarray(all_stops)
    track_beginnings = np.asanyarray(track_beginnings)

    for trial in range(number_of_trials - 1):
        beginning = track_beginnings[trial]
        end = track_beginnings[trial + 1]
        all_stops = np.asanyarray(all_stops)
        stops_on_trial_indices = (np.where((beginning <= all_stops) & (all_stops <= end)))

        stops_on_trial = np.take(all_stops, stops_on_trial_indices)

        if len(stops_on_trial) > 0:
            stops = np.take(location, stops_on_trial)

            stops_on_trials.append(stops)
    return stops_on_trials


def get_pooled_data(path, number_of_days):

    first_stop_locations = np.array([])
    stop_locations = np.array([])
    stop_times = np.array([])
    stops_on_trials = []
    trial_num = 0

    for day in range(number_of_days):

        if os.path.isfile(path + "\\location" + str(day + 1) + ".npy") is False:
            continue

        location_day = np.load(path + 'location' + str(day+1) + '.npy')
        trial_num_day = np.load(path + 'trial_num' + str(day+1) + '.npy')
        trial_num_day = np.asanyarray(trial_num_day)

        track_beginnings_day = np.load(path + 'beginning_of_track' + str(day+1) + '.npy')

        first_stops_day = np.load(path + 'first_stops' + str(day+1) + '.npy')
        first_stops = np.asanyarray(first_stops_day, dtype=int)
        first_stops = np.unique(first_stops)
        first_stop_locations_day = np.take(location_day, first_stops)
        first_stop_locations = np.append(first_stop_locations, first_stop_locations_day)

        stop_times_day = np.load(path + 'stop_times' + str(day+1) + '.npy')
        stop_locations_day = np.take(location_day, stop_times_day)
        stop_locations = np.append(stop_locations, stop_locations_day)
        stops_on_trials_day = get_stops_on_trials_find_stops(location_day, trial_num_day, stop_times_day, track_beginnings_day)

        for trial in range(len(stops_on_trials_day)):
            stops_on_trials.append(stops_on_trials_day[trial])

    stop_locations = np.asanyarray(stop_locations, dtype='int64')
    np.save(path + 'stop_locations.npy', stop_locations)

    np.save(path + 'first_stop_locations.npy', first_stop_locations)
    np.savetxt(path + 'first_stop_locations.txt', first_stop_locations)

    return stops_on_trials, first_stop_locations