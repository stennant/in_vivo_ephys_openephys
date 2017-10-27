import convert_open_ephys_to_mda
import numpy as np


def test_get_padded_array():
    waveforms = np.array([[[1, 1, 1, 1], [2, 2, 2, 9], [3, 3, 3, 3]], [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]])
    samples_per_spike = 3

    desired_result = np.array([[[0, 0, 0, 1, 2, 3], [0, 0, 0, 4, 5, 6]], [[0, 0, 0, 1, 2, 3], [0, 0, 0, 4, 5, 6]], [[0, 0, 0, 1, 2, 3], [0, 0, 0, 4, 5, 6]], [[0, 0, 0, 1, 9, 3], [0, 0, 0, 4, 5, 6]]])
    result = convert_open_ephys_to_mda.get_padded_array(waveforms, samples_per_spike)

    assert np.allclose(result, desired_result, rtol=1e-05, atol=1e-08)