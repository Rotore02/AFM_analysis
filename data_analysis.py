import numpy as np
from scipy.odr import ODR, Model, RealData
import image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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


#z = image.read_tiff("pn_junction.tiff")
#coordinate_grid = image.create_coordinate_grid(256,1)
#z = shift_mean(z)
#z = mean_plane_subtraction(z, coordinate_grid)
#image.plot_afm_image("output1.pdf", z, coordinate_grid, "viridis")

#X, Y = coordinate_grid


#fig = plt.figure(figsize=(10, 6))
#ax = fig.add_subplot(111, projection='3d')

#ax.plot_surface(X, Y, z, cmap='viridis', alpha=0.9, label='Dati')


#ax.set_title("Superficie corretta + piano di fit")
#ax.set_xlabel("X")
#ax.set_ylabel("Y")
#ax.set_zlabel("Z")

#plt.show()