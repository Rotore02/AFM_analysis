import numpy as np
from scipy.odr import ODR, Model, RealData
import image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def mean_plane_subtraction(
    height_values : np.ndarray[float],
    coordinate_grid : tuple[np.ndarray[float]]
    ) -> np.ndarray[float]:
    X, Y = coordinate_grid
    x_flat = X.ravel()
    y_flat = Y.ravel()
    z_flat = height_values.ravel()
    A = np.vstack([x_flat, y_flat, np.ones_like(x_flat)]).T 
    coeffs, _, _, _ = np.linalg.lstsq(A, z_flat)
    a,b,c = coeffs
    return height_values - (a*X + b*Y)

def shift_min(
    height_values : np.ndarray[float]
    ) -> np.ndarray[float]:
    minimum_height = np.min(height_values)
    return height_values - minimum_height #the minimum height value is set to zero

def shift_mean(
    height_values : np.ndarray
    ) -> np.ndarray:
    mean_height = np.mean(height_values)
    return height_values- mean_height #the mean height is set to zero