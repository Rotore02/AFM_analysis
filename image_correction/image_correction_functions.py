import numpy as np
import smart_file as sm

def common_plane_subtraction(
    height_values : np.ndarray,
    results_file : sm.SmartFile
    ) -> np.ndarray:
    """
    Cancels out the planar slope of the image.

    Starting from the plane equation z = a*x + b*y + c, this function subtracts A*x + B*y + C to the height values 
    of the AFM image, where the coefficients A and B are obtained by minimizing the square displacement between the 
    plane and the height values. This is done to eliminate any planar inclination due to sample positioning in the 
    AFM microscope. The plane parameters will be written in the results_file if its internal state `enabled` 
    is set to True.

    Parameters
    ----------
    height_values: ndarray
                   2-d grid containing the height values.
    results_file: SmartFile
                  File-like object that records results if its internal `enabled` flag is True.
                  

    Returns
    -------
    ndarray
            2-d grid with the height values subtracted by the common plane.

    See Also
    --------
    np.meshgrid : Generates coordinate matrices from coordinate vectors.
    np.linalg.lstsq: function that returns the least-squares solution to a linear matrix equation.
    sm.SmartFile: class to create files on which it is possible to write if their internal state `enabled` is set to True.
    Its methods internally check wether this condition is met.
    """
    nx, ny = height_values.shape
    x_ax = np.arange(nx)
    y_ax = np.arange(ny) #initialize the x and y axes as two 1d arrays of integers. They represent fictitious coordinates to do the calculations.
    X, Y = np.meshgrid(x_ax, y_ax) #create X and Y which are the fictitious coordinate matrices of the x and y axes.
    x_flat = X.ravel()
    y_flat = Y.ravel()
    z_flat = height_values.ravel()
    A = np.vstack([x_flat, y_flat, np.ones_like(x_flat)]).T 
    coeffs, _, _, _ = np.linalg.lstsq(A, z_flat)
    a,b,c = coeffs
    results_file.write("COMMON PLANE SUBTRACTION" + '\n' + 
                    "plane equation: z = a*x + b*y + c" + '\n' + 
                    f"a = {a}" + '\n' + 
                    f"b = {b}" + '\n' + 
                    f"c = {c}" + '\n' + 
                    "----------------------------" + '\n')
    return height_values - (a*X + b*Y + c)

def mean_drift_subtraction(
    height_values : np.ndarray,
    results_file : sm.SmartFile
    ) -> np.ndarray:
    """
    Cancels out the drift along the fast scan direction by mean subtraction.

    This function computes the mean value of each line along the fast scan direction (x axis) and subtracts this 
    values to each height value in the line. This is done to eliminate systematic drifts due to temperature 
    variations or friction between the sample and the cantilever. The average mean value and its standard deviation 
    are written in the results_file if its internal state `enabled` is set to True.

    Parameters
    ----------
    height_values: ndarray
                   2-d grid containing the height values.
    results_file: SmartFile
                  File-like object that records results if its internal `enabled` flag is True.

    Returns
    -------
    ndarray
            2-d grid with the height values corrected by mean subtraction.

    See Also
    --------
    np.mean: function that computes the arithmetic mean along a certain axis.
    sm.SmartFile: class to create files on which it is possible to write if their internal state `enabled` is set to True.
    Its methods internally check wether this condition is met.
    line_drift_subtraction: function that cancels out the drift along the fast scan direction by line subtraction.
    """
    ny = height_values.shape[0]
    y_ax = np.arange(ny) #initialize the y axis as a 1d arrays of integers from 0 to ny. They represent fictitious coordinates to do the calculations.
    mean_set = []
    for y in y_ax:
        mean_height = np.mean(height_values[y])
        height_values[y] = height_values[y] - mean_height
        mean_set.append(mean_height)
    results_file.write("MEAN DRIFT SUBTRACTION" + '\n' + 
                    f"average mean value = {np.mean(mean_set)}" + '\n' + 
                    f"standard deviation = {np.std(mean_set)}" + '\n' + 
                    "----------------------------" + '\n')
    return height_values

def linear_drift_subtraction(
    height_values : np.ndarray,
    results_file : sm.SmartFile
    ) -> np.ndarray:
    """
    Cancels out the drift along the fast scan direction by line subtraction.

    Starting from the line equation z = m*x + q, this function subtracts M*x + Q to the height values
    of each fast scan direction (x axis direction) of the AFM image, where the coefficients M and Q are
    obtained by minimizing the square displacement between the line and the height values.
    This is done to eliminate systematic drifts due to temperature variations or friction between the 
    sample and the cantilever. The average values of M and Q and their standard deviation are written in 
    the `results_file` if its internal state `enabled` is set to True.

    Parameters
    ----------
    height_values: ndarray
                   2-d grid containing the height values.
    results_file: SmartFile
                  File-like object that records results if its internal `enabled` flag is True.

    Returns
    -------
    ndarray
            2-d grid with the height values corrected by line subtraction.
    
    See Also
    --------
    np.linalg.lstsq: function that returns the least-squares solution to a linear matrix equation.
    sm.SmartFile: class to create files on which it is possible to write if their internal state `enabled` is set to True.
    Its methods internally check wether this condition is met.
    mean_drift_subtraction: function that cancels out the drift along the fast scan direction by mean subtraction.
    """
    nx, ny = height_values.shape
    x_ax = np.arange(nx)
    y_ax = np.arange(ny)
    A = np.vstack([x_ax, np.ones_like(x_ax)]).T
    m_set = []
    q_set = []
    for y in y_ax:
        coeffs, _, _, _ = np.linalg.lstsq(A,height_values[y])
        m,q = coeffs
        height_values[y] = height_values[y] - (m*x_ax + q)
        m_set.append(m)
        q_set.append(q)
    results_file.write("LINE DRIFT SUBTRACTION" + '\n' + "line equation: z = m*z + q" + '\n' +
                    f"average m value = {np.mean(m_set)}" + '\n' + 
                    f"m values standard deviation = {np.std(m_set)}" + '\n' + 
                    f"average q value = {np.mean(q_set)}" + '\n' +
                    f"q values standard deviation = {np.std(q_set)}" + '\n' + 
                        "----------------------------" + '\n')
    
    return height_values

def shift_min(
    height_values : np.ndarray,
    ) -> np.ndarray:
    """
    Sets the minimum height value to zero.

    Finds the minimum height inside the height_values array and subtracts its value to each element of the array,
    thus shifting the image such that the minimum height corresponds to zero.
    
    Parameters
    ----------
    height_values: ndarray
                   2-d grid containing the height values.

    Returns
    -------
    ndarray
            2-d grid with the height values subtracted by the minimum height value.

    See Also
    --------
    shift_mean: function that sets the mean height to zero.
    """
    minimum_height = np.min(height_values)
    return height_values - minimum_height #the minimum height value is set to zero

def shift_mean(
    height_values : np.ndarray
    ) -> np.ndarray:
    """
    Sets the mean height value to zero.

    Computes the mean height inside the height_values array and subtracts its value to each element of the array, 
    thus shifting the image such that the mean height corresponds to zero.
    
    Parameters
    ----------
    height_values: ndarray
                   2-d grid containing the height values.

    Returns
    -------
    ndarray
            2-d grid with the height values subtracted by the mean height value.

    See Also
    --------
    np.mean: function that computes the arithmetic mean along a certain axis.
    shift_min: function that sets the minimum height value to zero.
    """
    mean_height = np.mean(height_values)
    return height_values - mean_height #the mean height is set to zero
    