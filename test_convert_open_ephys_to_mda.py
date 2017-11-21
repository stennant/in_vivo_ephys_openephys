import convert_open_ephys_to_mda
import numpy as np


def test_pad_event():
    waveforms = np.array([[[1, 1, 1, 1], [2, 2, 2, 9], [3, 3, 3, 3]], [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]])
    channel = 0
    samples_per_spike = 3
    event = 0

    desired_result = np.array([1, 2, 3, 0, 0, 0])
    result = convert_open_ephys_to_mda.pad_event(waveforms, channel, samples_per_spike, event)


def test_get_padded_array():
    waveforms = np.array([[[1, 1, 1, 1], [2, 2, 2, 9], [3, 3, 3, 3]], [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]])
    samples_per_spike = 3

    desired_result = np.array([[0, 0, 0, 1, 2, 3, 0, 0, 0, 1, 2, 3, 0, 0, 0, 1, 2, 3, 0, 0, 0, 1, 2, 9], [0, 0, 0, 4, 5, 6, 0, 0, 0, 4, 5, 6, 0, 0, 0, 4, 5, 6, 0, 0, 0, 4, 5, 6]])
    result = convert_open_ephys_to_mda.get_padded_array(waveforms, samples_per_spike)

    assert np.allclose(result, desired_result, rtol=1e-05, atol=1e-08)


def test_get_peak_indices():
    waveforms = np.array([[[1, 1, 1, 1], [2, 2, 2, 9], [3, 3, 3, 3]], [[4, 4, 4, 4], [5, 11, 5, 5], [6, 6, 6, 17]]])
    samples_per_spike = 3

    desired_result = np.array([1, 2])
    result = convert_open_ephys_to_mda.get_peak_indices(waveforms, samples_per_spike)

    assert np.allclose(result, desired_result, rtol=1e-05, atol=1e-08)

