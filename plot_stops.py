import itertools
import matplotlib.pylab as plt
import numpy as np
import os
import trial_types
import parameters
import plot_utility
import stops


def get_stops_on_trials(prm):
    location, number_of_trials, all_stops, track_beginnings = stops.get_data_for_stops_on_trials(prm)
    stops_on_trials = stops.get_stops_on_trials_find_stops(location, number_of_trials, all_stops, track_beginnings)
    return stops_on_trials


def make_plot(prm, stops_on_trials):
    plot_utility.draw_reward_zone()
    plot_utility.draw_black_boxes()
    stops_raster = plt.subplot(111)

    plt.xlim(0, 200)

    for ith, trial in enumerate(stops_on_trials):
        if trial.size == 0:
            continue

        if ith % 5 == 0 and ith > 0:
            color_of_stop = 'r'
            plt.plot(trial, ith, 'ko', markersize=3, c=color_of_stop, markeredgewidth=0.0)
        else:
            color_of_stop = 'k'
            plt.plot(trial, ith, 'ko', markersize=3, c=color_of_stop, markeredgewidth=0.0)
    plt.ylim(.5, len(stops_on_trials) + .5)
    plt.xlabel('$Location\ on\ track\ (cm)$', fontsize=20)
    plt.ylabel('$Stops\ on\ trials$', fontsize=20)
    stops_raster.spines['right'].set_visible(False)
    stops_raster.spines['top'].set_visible(False)
    stops_raster.yaxis.set_ticks_position('left')
    stops_raster.xaxis.set_ticks_position('bottom')
    plt.savefig(prm.get_behaviour_analysis_path() + '\\stops_on_track.png')

    plt.close()


def make_plot_with_stages(prm, stops_on_trials, stage_1, stage_2, stage_3):
    plot_utility.draw_reward_zone()
    plot_utility.draw_black_boxes()
    stops_raster = plt.subplot(111)

    if stage_1 != 0:
        plt.axhline(stage_1, color='k', linewidth=10)
    if stage_2 != 0:
        plt.axhline(stage_2, color='r', linewidth=10)
    if stage_3 != 0:
        plt.axhline(stage_3, color='k', linewidth=10)


    plt.xlim(0, 200)

    for ith, trial in enumerate(stops_on_trials):
        if trial.size == 0:
            continue

        if ith % 5 == 0 and ith > 0:
            color_of_stop = 'r'
            plt.plot(trial, ith, 'ko', markersize=3, c=color_of_stop, markeredgewidth=0.0)
        else:
            color_of_stop = 'k'
            plt.plot(trial, ith, 'ko', markersize=3, c=color_of_stop, markeredgewidth=0.0)
    plt.ylim(.5, len(stops_on_trials) + .5)
    plt.xlabel('$Location\ on\ track\ (cm)$', fontsize=20)
    plt.ylabel('$Stops\ on\ trials$', fontsize=20)
    stops_raster.spines['right'].set_visible(False)
    stops_raster.spines['top'].set_visible(False)
    stops_raster.yaxis.set_ticks_position('left')
    stops_raster.xaxis.set_ticks_position('bottom')
    plt.savefig(prm.get_behaviour_analysis_path() + '\\stops_on_track.png')

    plt.close()





def plot_stops(prm):
    plt.gcf().clear()
    stops_on_trials = get_stops_on_trials(prm)
    make_plot(prm, stops_on_trials)

    return stops_on_trials


def plot_first_stops(prm, first_stops, location):
    analysis_path = prm.get_behaviour_analysis_path()
    plt.gcf().clear()
    plot_utility.draw_reward_zone()
    plot_utility.draw_black_boxes()
    first_stops = np.asanyarray(first_stops, dtype=int)
    first_stop_locations = np.take(location, first_stops)
    weights = np.ones_like(first_stop_locations)/float(len(first_stop_locations))
    first_stop_hist = plt.subplot(111)
    first_stop_hist.hist(first_stop_locations, 20, color='r', range=[0, 200], weights=weights)
    first_stop_hist.spines['right'].set_visible(False)
    first_stop_hist.spines['top'].set_visible(False)
    first_stop_hist.yaxis.set_ticks_position('left')
    first_stop_hist.xaxis.set_ticks_position('bottom')

    plt.xlabel('$Location\ on\ track\ (cm)$', fontsize=20)
    plt.ylabel('$Frequency\ of\ first\ stops\ (histogram)$', fontsize=20)

    if os.path.exists(analysis_path) is False:
        os.makedirs(analysis_path)

    plt.savefig(analysis_path + '\\first_stops.png')
    plt.close()


def plot_first_stops_location(prm, first_stop_locations):
    analysis_path = prm.get_behaviour_analysis_path()
    plt.gcf().clear()
    plot_utility.draw_reward_zone()
    plot_utility.draw_black_boxes()
    weights = np.ones_like(first_stop_locations)/float(len(first_stop_locations))
    first_stop_hist = plt.subplot(111)
    first_stop_hist.hist(first_stop_locations, 20, color='r', range=[0, 200], weights=weights)
    first_stop_hist.spines['right'].set_visible(False)
    first_stop_hist.spines['top'].set_visible(False)
    first_stop_hist.yaxis.set_ticks_position('left')
    first_stop_hist.xaxis.set_ticks_position('bottom')

    plt.xlabel('$Location\ on\ track\ (cm)$', fontsize=20)
    plt.ylabel('$Frequency\ of\ first\ stops\ (histogram)$', fontsize=20)

    if os.path.exists(analysis_path) is False:
        os.makedirs(analysis_path)

    plt.savefig(analysis_path + '\\first_stops.png')
    plt.close()


def main():
    prm = parameters.Parameters()
    analysis_path = 'C:\\Users\\s1466507\\Documents\\Ephys\\deep MEC\\test\\2017-03-27_09-46-34\\Behaviour\\Analysis\\'
    location = np.load('C:\\Users\\s1466507\\Documents\\Ephys\\deep MEC\\test\\2017-03-27_09-46-34\\Behaviour\\Data\\location.npy')
    first_stops = np.load('C:\\Users\\s1466507\\Documents\\Ephys\\deep MEC\\test\\2017-03-27_09-46-34\\Behaviour\\Data\\first_stops.npy')

    prm.set_behaviour_data_path('C:\\Users\\s1466507\\Documents\\Ephys\\deep MEC\\test\\2017-03-27_09-46-34\\Behaviour\\Data\\')
    prm.set_behaviour_analysis_path('C:\\Users\\s1466507\\Documents\\Ephys\\deep MEC\\test\\2017-03-27_09-46-34\\Behaviour\\Analysis\\')

    plot_first_stops(prm, first_stops, location)

    plot_stops(prm)


if __name__ == '__main__':
    main()