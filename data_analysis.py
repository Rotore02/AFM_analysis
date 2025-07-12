import numpy as np
from scipy.odr import ODR, Model, RealData
import image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def common_plane_subtraction(
    height_values : np.ndarray[float]
    ) -> np.ndarray[float]:
    """
    Cancels out the planar slope of the image

    Starting from the plane equation z = a*x + b*y + c, this function subtracts z = A*x + B*y to the height values of the AFM image, where the coefficients A and B are obtained by minimizing the square displacement between the plane and the height values. Note that this function does not subtract the whole plane z = A*x + B*y + C.

    Parameters
    ----------
    height_values: ndarray[float]
                   2-d grid with height values.

    Returns
    -------
    ndarray[float]
                   2-d grid with the height values subtracted by the common plane.
    """
    nx, ny = height_values.shape
    x = np.arange(nx)
    y = np.arange(ny) #initialize the x and y axis as two 1d arrays of integers. They represent fictitious coordinates to do the calculations.
    X, Y = np.meshgrid(x, y) #create X and Y which are the fictitious coordinate matrices of the x and y axes.
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
    """
    Sets the minimum height value to zero.

    Finds the minimum height inside the height_values array and subtracts its value to each element of the array, thus shifting the image such that the minimum height corresponds to zero.
    
    Parameters
    ----------
    height_values: ndarray[float]
                   2-d grid with height values.

    Returns
    -------
    ndarray[float]
                   2-d grid with the height values subtracted by the minimum height value. 
    """
    minimum_height = np.min(height_values)
    return height_values - minimum_height #the minimum height value is set to zero

def shift_mean(
    height_values : np.ndarray
    ) -> np.ndarray:
    """
    Sets the mean height value to zero.

    Computes the mean height inside the height_values array and subtracts its value to each element of the array, thus shifting the image such that the mean height corresponds to zero.
    
    Parameters
    ----------
    height_values: ndarray[float]
                   2-d grid with height values.

    Returns
    -------
    ndarray[float]
                   2-d grid with the height values subtracted by the mean height value. 
    """
    mean_height = np.mean(height_values)
    return height_values- mean_height #the mean height is set to zero


    

#def linear(P,x):
 #   return 1/(((80*50*10**(-5)*P[0])/20)*(x - P[1]))

#realdata = RealData(gate_voltages[2:7], resistance[2:7])
#model = Model(linear)
#odr = ODR(realdata, model, beta0=[10**(-1), 0.5])
#output = odr.run()
#mu, V_t = output.beta[0], output.beta[1]
#d_mu, d_V_t = output.sd_beta[0], output.sd_beta[1]



