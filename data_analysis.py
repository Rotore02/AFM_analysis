import numpy as np

def shift_min(
        height_values : np.ndarray
        ) -> np.ndarray:
    minimum_height = min(height_values)
    return height_values - minimum_height #the minimum height value is set to zero

def shift_mean(
        height_values : np.ndarray
        ) -> np.ndarray:
    mean_height = sum(height_values)
    return height_values- mean_height #the mean height is set to zero