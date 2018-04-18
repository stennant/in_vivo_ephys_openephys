from scipy.signal import argrelextrema
import os
import filter
import matplotlib.pyplot as plt
import numpy as np
import power_spectrum


def power_spectra_for_phases(phase, signal, prm, location, sampling_rate):
    high_indices = np.where(phase == 1)
    low_indices = np.where(phase == 0)

    print('high indices {}'.format(high_indices))
    print('low indices {}'.format(low_indices))
    print('sampling rate {}'.format(sampling_rate))
    print('signal {}'.format(signal))

    signal = filter.gamma_filter(signal, sampling_rate)

    outbound1 = np.where(prm.get_beginning_of_outbound() < location)
    outbound2 = np.where(prm.get_reward_zone() > location)

    outbound = np.intersect1d(outbound1, outbound2)

    print('outbound {}'.format(outbound))

    outbound_high_phase_indices = np.intersect1d(outbound, high_indices[0], True)
    outbound_low_phase_indices = np.intersect1d(outbound, low_indices[0], True)



    high_phase_outbound = np.take(signal, outbound_high_phase_indices)
    low_phase_outbound = np.take(signal, outbound_low_phase_indices)




    print('high phase {}'.format(outbound_high_phase_indices))
    print('low phase {}'.format(outbound_low_phase_indices))

    #################################################
    #  Figure
    ################################################
    filename = 'ps_gamma_theta_phases'
    fig, ax = plt.subplots()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    plt.xticks([0, 50, 100, 150])
    plt.yticks([10, 100, 1000])

    plt.plot((100, 110), (700, 700), 'k', linewidth=5)
    plt.plot((100, 110), (500, 500), 'b', linewidth=5)

    plt.text(115, 670, '$low phase$')
    plt.text(115, 470, '$high phase$')

    power_spectrum.power_spectrum_log(prm, low_phase_outbound, sampling_rate, 'k', filename,
                                      title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')
    power_spectrum.power_spectrum_log(prm, high_phase_outbound, sampling_rate, 'b', filename,
                                      title="$Power spectrum$", x_lim=150, line_width=15, legend='movement')
    plt.close(fig)
    # plt.show()













'''
Finds local minima and maxima by comparing element to neighbours. order means tha number of neighbours on both
sides that is needs to be bigger/smaller than to be considered an extrema. I set this to be 500 for now,
because I will use this for theta oscillations with a sampling rate of 30000.

input
    signal : numpy array, signal to find extrema for

output
    local minima : numpy array, local minima
    local maxima : numpy array, local maxima
Note: The values that are found in both mimima and maxima arrays are plateaus.

'''


def find_local_extrema(signal):
    local_maxima = argrelextrema(signal, np.greater) # set this to be 500 for theta oscillations
    local_minima = argrelextrema(signal, np.less)

    return local_minima, local_maxima


def remove_inflexion_points(local_minima, local_maxima):
    inflex_points = np.intersect1d(local_maxima[0], local_minima[0], True)
    print(inflex_points)
    # remove inflexion points
    minima = np.setdiff1d(local_minima[0], inflex_points)
    maxima = np.setdiff1d(local_maxima[0], inflex_points)
    return minima, maxima


def make_arrays_same_length(minima, maxima):
    if len(minima) < len(maxima):
        maxima = maxima[:len(minima)]
    else:
        minima = minima[:len(maxima)]

    return minima, maxima


def check_starting_extrema(minima, maxima):
    if minima[0] < maxima[0]:
        starts_with_min = True
    else:
        starts_with_min = False
    return starts_with_min


def create_mask_for_phases(middle_points, starts_with_min):
    phase = np.array([])
    every_second = middle_points[1::2]
    for middle in range(len(middle_points) - 1):
        if middle_points[middle] not in every_second:
            # print('middle: {}'.format(middle_points[middle]))
            # print('middle plus one: {}'.format(middle_points[middle+1]))

            if starts_with_min:
                interval = middle_points[middle + 1] - middle_points[middle]
                phase = np.append(phase, np.full(interval, 1))
            else:
                interval = middle_points[middle + 1] - middle_points[middle]
                phase = np.append(phase, np.full(interval, 0))

        else:
            if starts_with_min:
                interval = middle_points[middle + 1] - middle_points[middle]
                phase = np.append(phase, np.full(interval, 0))
            else:
                interval = middle_points[middle + 1] - middle_points[middle]
                phase = np.append(phase, np.full(interval, 1))
    return phase


def separate_phases(local_minima, local_maxima, channel_name, prm):
    starts_with_min = None
    middle_points = np.array([])
    filepath = prm.get_filepath()
    if os.path.isfile(filepath + "phase_" + str(channel_name) + ".npy") is False:
        print('Theta phases for channel {} are saved in {}.'.format(filepath, channel_name))
        print(local_minima)
        print(local_maxima)

        minima, maxima = remove_inflexion_points(local_minima, local_maxima)
        minima, maxima = make_arrays_same_length(minima, maxima)
        starts_with_min = check_starting_extrema(minima, maxima)  # true when first local extremum is a minimum

        middle_points = ((maxima - minima)/2 + minima)
        middle_points = np.asanyarray(middle_points, int)

        phase = create_mask_for_phases(middle_points, starts_with_min)

        np.save(filepath + "phase_" + str(channel_name), phase)
    else:
        phase = np.load(filepath + "phase_" + str(channel_name) + ".npy")

    return phase


def gamma_powers_for_theta(signal, channel_name, prm, location, sampling_rate):
    print('Processing theta and gamma filtered data...')
    # signal = signal[30000:]
    theta = filter.theta_filter(signal, sampling_rate)
    theta_minima, theta_maxima = find_local_extrema(theta)
    # plt.plot(theta)
    print('This is happening')
    phase = separate_phases(theta_minima, theta_maxima, channel_name, prm)
    power_spectra_for_phases(phase, signal, prm, location, sampling_rate)

    # These two lines were to visually check tha minima and maxima are found correctly
    #plt.scatter(theta_maxima, np.take(theta, theta_maxima), s=np.pi*100, c='r', alpha=0.5)
    #plt.scatter(theta_minima, np.take(theta, theta_minima), s=np.pi*100, c='k', alpha=0.5)

    # plt.plot(filter.custom_filter(signal, 70, 200, sampling_rate))
    # plt.plot(filter.custom_filter(signal, 100, 200, sampling_rate))

    plt.show()












