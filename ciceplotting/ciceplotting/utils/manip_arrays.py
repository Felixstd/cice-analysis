import numpy as np


def pad_array(array):
    """
    Array is a list of lists with different lengths

    """

    max_length = max(len(arr) for arr in array)
    padded  = np.full((len(array), max_length), np.nan)
    for i, cycle in enumerate(array):
        padded[i, :len(cycle)] = cycle

    return padded 
