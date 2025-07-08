import numpy as np

data_shift='minimum'

if data_shift == "minimum":
    def shift_min(
        height_values : np.ndarray
        ) -> np.ndarray:
        minimum_height = min(height_values)
        return height_values - minimum_height #the minimum height value is set to zero
elif data_shift == "mean":
    def shift_mean(
            height_values : np.ndarray
            ) -> np.ndarray:
        mean_height = sum(height_values)
        return height_values- mean_height #the mean height is set to zero
else:
    raise TypeError("The inserted data shift option is not valid. Please insert 'minimum' or 'mean'.")

def mean_plane_subtraction(
    height_values : np.ndarray
    ) -> np.ndarray:
    minimum_height, maximum_height = min(height_values), max(height_values)