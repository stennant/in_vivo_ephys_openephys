'''
Tests for the functions in movement.py
'''

import process_movement
import numpy as np
import parameters

prm = parameters.Parameters()
prm.set_track_length(8)
prm.set_stop_threshold(3)
track_length = prm.get_track_length()


def test_get_instant_velocity():

    location = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1]
    sampling_points_per200ms = 2

    desired_result = [0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    result = process_movement.get_instant_velocity(prm, location, sampling_points_per200ms)

    assert np.allclose(result, desired_result, rtol=1e-05, atol=1e-08)


def test_get_avg_speed_200ms():
    velocity = [1, 1, 1, 1, 1, 1]
    sampling_points_per200ms = 2

    desired_result = [0., 0., 1., 1., 1., 1.]
    result = process_movement.get_avg_speed_200ms(prm, velocity, sampling_points_per200ms)
    assert np.allclose(result, desired_result, rtol=1e-05, atol=1e-08)
