from __future__ import division
import file_utility
import matplotlib.pylab as plt
import numpy as np
import os
import open_ephys_IO


# This is necessary because of artefacts at the beginning and end of the recordings. 5 seconds are removed
def remove_beginning_and_end(prm, raw_location_data):
    sampling_rate = prm.get_sampling_rate()
    raw_location_trimmed = raw_location_data[sampling_rate*5:-sampling_rate*5]
    return raw_location_trimmed



'''
These functions calculate the location normalized to metric, the velocity, and the speed of the animal.

The arrays the functions create are saved to the folder specified in main. If the script is run more than once,
it will read the data from the file instead of calculating again.
'''


def get_raw_location(prm):
    file_path = prm.get_filepath() + prm.get_movement_ch()
    location = open_ephys_IO.get_data_continuous(prm, file_path)
    location = remove_beginning_and_end(prm, location)
    return location


'''
Normalizes recorded values from location channel to metric (cm)

input
    prm : object, parameters
    raw_data : array, electrophysiology and movement data file, contains recorded location values

output
    normalized_location_metric : array, contains normalized location values (in cm)

The standardization is computed by finding the minimum and maximum recorded location values (min, max), and then
subtracting min from max, to get the recorded track length (recorded_length). Then, this recorded_length is devided by
the real track length to get the distance unit that will be used for the conversion.

From every recorded location point, the recorded_startpoint (min) value is subtracted to make the first location = 0.
The recorded_startpoint may not be 0 due to the sampling rate. (Please note that this is not the beginning of the
ephys recording in time, but the smallest value recorded by the rotary encoder.) This value is then divided by the
distance unit calculated in the previous step to convert the rotary encoder values to metric.
'''


def get_normalised_location_metric(prm, raw_data):
    print('Calculating normalized location...')
    recorded_location = raw_data  # Get the list of locations from the appropriate channel
    # Recorded beginning of the track. This may be nonzero because of sampling rate.
    recorded_startpoint = min(recorded_location)

    recorded_endpoint = max(recorded_location)  # Recorded end of track.

    # Obtain recorded track length by subtracting end- and starting points obtained above
    recorded_track_length = recorded_endpoint - recorded_startpoint

    # Obtain distance unit (cm) by dividing recorded track length to actual track length
    distance_unit = recorded_track_length/prm.get_track_length()

    # Subtract starting point value from all locations so that the track starts at 0cm
    # (i.e., 'normalise' - it's more of a standardisation though) and convert to metric system (cm)
    normalised_location_metric = (recorded_location - recorded_startpoint) / distance_unit
    np.save(prm.get_filepath() + "Behaviour\\Data\\location", normalised_location_metric)

    print('Normalized location is saved.')

    return normalised_location_metric


'''
Corrects for the very small negative values that are calculated as velocity when the mouse 'teleports' back
to the beginning of the track - from the end of the track to 0.

input
    prm : obejct, parameters
    velocity : numpy array, instant velocity

output
    velocity : array, instant velocity without teleport artefacts

It finds the velocity values that are smaller than -track_length+max_velocity, and adds track_length to them. These
values will be around the beginning of the track after the mouse finished the previous trial and jumped back to the
beginning.

After the first iteration, it finds the values that are <-10 (it is highly unlikely for a mouse to have that speed), it
replaces them with the previous location value.

An alternative solution may be to nto analyze this data.

'''


def fix_teleport(prm, velocity):
    max_velocity = max(velocity)
    track_length = prm.get_track_length()
    # If the mouse goes from the end of the track to the beginning, the velocity would be a negative value
    # if velocity< (-1)*track_length + max_velocity, then track_length is added to the value
    too_small_indices = np.where(velocity < (-track_length + max_velocity))
    too_small_values = np.take(velocity, too_small_indices)
    to_insert = too_small_values + track_length

    np.put(velocity, too_small_indices, to_insert)  # replace small values with new correct value

    # if velocity is <-10 (due to the teleportation), the previous velocity value will be used
    small_velocity = np.where(velocity < -10)  # find where speed is < 10
    small_velocity = np.asanyarray(small_velocity)
    previous_velocity_index = small_velocity - 1  # find indices right before those in previous line
    previous_velocity = np.take(velocity, previous_velocity_index)
    np.put(velocity, small_velocity, previous_velocity)  # replace small speed values with previous value

    return velocity


'''
Calculates instant velocity for every sampling point

input
    prm : object, parameters
    location : numpy array, location values (metric)
    sampling_points_per200ms : number of sampling points in 200ms signal

output
    velocity : instant velocity

calls
    fix_teleport : function to fix issues arising from the fact that when the mouse restarts the trial, it is
    teleported back to the beginning of the track, and the velocity will be a very small negative value.

The location array is duplicated, and shifted in a way that it can be subtracted from the original to avoid loops.
(The shifted array is like : first 200ms data + first 200ms data again, rest of data without last 200ms, this is
subtracted from the original location array.)
'''


def get_instant_velocity(prm, location, sampling_points_per200ms):
    print('Calculating velocity...')
    # Rearrange arrays in a way that they just need to be subtracted from each other
    end_of_loc_to_subtr = location[:-sampling_points_per200ms]

    beginning_of_loc_to_subtr = location[:sampling_points_per200ms]

    location_to_subtract_from = np.append(beginning_of_loc_to_subtr, end_of_loc_to_subtr)
    velocity = location - location_to_subtract_from

    velocity = fix_teleport(prm, velocity)

    return velocity


'''
Calculates moving average

input
    a : array,  to calculate averages on
    n : integer, number of points that is used for one average calculation

output
    array, contains rolling average values (each value is the average of the previous n values)
'''


def moving_average(a, n):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n:] / n


'''
Calculate average speed for the last 200ms at each particular sampling point, based on velocity

input
    prm : object, parameters
    velocity : numpy array, instant velocity values
    sampling_points_per200ms : number of sampling points in 200ms

output
    avg_speed : numpy array, contains average speed for each location. The first 200ms are filled with 0s.

'''


def get_avg_speed_200ms(prm, velocity, sampling_points_per200ms):
    print('Calculating average speed...')
    avg_speed = np.empty(len(velocity), dtype=float)
    # Calculate average speed at each point by averaging instant velocities
    #  of all preceding points up to 200ms, including given point
    avg_speed[:sampling_points_per200ms] = 0
    avg_speed[sampling_points_per200ms:] = moving_average(velocity, sampling_points_per200ms)
    np.save(prm.get_filepath() + "Behaviour\\Data\\speed", avg_speed)
    print('Speed is saved.')
    return avg_speed


'''
Makes an array with the indices when the animal moves (speed>=speed_threshold) and one when is doesn't.
The mouse is considered to stop when the speed is below speed_threshold (speed<speed_threshold).

input
    prm : object, parameters
    speed : numpy array, average speed calculated from instant velocity

output
    stationary : numpy array, indices where speed is <= threshold
    moves : numpy array, indices where speed is <= threshold

'''


def moves_or_stationary(prm, speed):
    print('Separating movement and stationary data...')

    threshold = prm.get_stop_threshold()
    moves = np.where(abs(speed) > threshold)
    stationary = np.where(abs(speed) <= threshold)

    np.save(prm.get_filepath() + "Behaviour\\Data\\stationary", stationary)
    np.save(prm.get_filepath() + "Behaviour\\Data\\moves", moves)
    print('Stationary and movement data are saved.')
    return stationary, moves

'''
If the arrays for location, velocity and speed don't exist, it calls the functions to create them and saves them.

input
    prm : object, parameters
    filepath : string, location of file

output
    location : numpy array, location of the animal (in cm)
    speed : numpy array, average speed based on instant velocity
    velocity : numpy array, instant velocity without teleportation arefacts

'''


def cached_calculate_movement(prm):
    data_path = prm.get_behaviour_data_path()
    if os.path.isfile(data_path + "\\location.npy") is False:
        location_raw = get_raw_location(prm)
        plt.plot(location_raw)
        plt.show()
        location = get_normalised_location_metric(prm, location_raw)
        np.save(data_path + "\\location", location)
    else:
        location = np.load(data_path + "\\location.npy")
    if os.path.isfile(data_path + "\\velocity.npy") is False:
        sampling_points_per200ms = int(prm.get_sampling_rate()/5)
        velocity = get_instant_velocity(prm, location, sampling_points_per200ms)
        np.save(data_path + "\\velocity", velocity)
        print('Instant velocity is saved.')
    else:
        velocity = np.load(data_path + "\\velocity.npy")
    if os.path.isfile(data_path + "\\speed.npy") is False:
        sampling_points_per200ms = int(prm.get_sampling_rate()/5)
        speed = get_avg_speed_200ms(prm, velocity, sampling_points_per200ms)
        np.save(data_path + "\\speed", speed)
    else:
        speed = np.load(data_path + "\\speed.npy")

    return location, speed, velocity


'''
If the arrays for stationary and movement state don't exist, it calls the functions to create them and saves them.

input
    prm : object, parameters
    filepath : string, location of file
    speed : numpy array, average speed based on instant velocity

output
    stationary : numpy array, indices where speed is <= threshold
    moves : numpy array, indices where speed is <= threshold

'''


def cached_stationary_movement(prm, speed):
    file_utility.create_folder_structure(prm)

    data_path = prm.get_behaviour_data_path()

    if os.path.isfile(data_path + "\\stationary.npy") is False or os.path.isfile(data_path + "\\moves.npy") is False:
        stationary, moves = moves_or_stationary(prm, speed)
        np.save(data_path + "\\stationary", stationary)
        np.save(data_path + "\\moves", moves)
    else:
        stationary = np.load(data_path + "\\stationary.npy")
        moves = np.load(data_path + "\\moves.npy")
    return moves, stationary


'''
Calculate location, velocity, speed, stationary and movement indices and save them, or open if they exist

input
    prm : object, parameters
    filepath : string, location of file

output
    location : numpy array, location of the animal (in cm)
    velocity : numpy array, instant velocity without teleportation arefacts
    speed : numpy array, average speed based on instant velocity
    stationary_indices : numpy array, indices where speed is <= threshold
    moves_indices : numpy array, indices where speed is <= threshold

'''


def save_or_open_movement_arrays(prm):
    file_utility.create_folder_structure(prm)

    for file in os.listdir(prm.get_filepath()):
        os.chdir(prm.get_filepath())
        if file.endswith(".npy") and os.path.getsize(file) == 0:
            print('---FILE ERROR: The size of ' + file + ' is 0, something is wrong.---')

    location, speed, velocity = cached_calculate_movement(prm)
    moves_indices, stationary_indices = cached_stationary_movement(prm, speed)
    os.chdir('..')
    return

