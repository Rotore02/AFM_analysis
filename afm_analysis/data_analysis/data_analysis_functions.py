import numpy as np
from afm_analysis import smart_file as sm

def height_distribution(
    height_values : np.ndarray
    ) -> tuple[np.ndarray, np.ndarray] :
    """
    Generates the x and y axis of the plot that represents the height distribution of the AFM image.

    This function returns the x and y axis of the plot that represents the distribution of the heights inside the 
    `height_values` array. The height values are subdivided into 100 bins ranging from `height_values.min()` to
    `height_values.max()` and the generated x axis of the distribution plot is an array containing the bin centers.
    The function `np.histogram` is used to generate the y axis, counting the amount of height values `z` falling in each bin. 
    The bins are defined as the intervals [n⋅bin_width, (n+1)⋅bin_width), (including the left edge and excluding the right edge) 
    if n⋅bin_width <= `z` < (n+1)⋅bin_width, with n integer that goes from 0 to 99.

    Parameters
    -----------
    height_values: ndarray
        2-d grid containing the height values.

    Returns
    -------
    tuple of two ndarray
        x and y axis of height distribution plot.

    See Also
    --------
    np.histogram : function that computes the histogram of a dataset.
    """
    n_bins = 100
    bin_edges = np.linspace(height_values.min(), height_values.max(), n_bins +1)
    histo, _ = np.histogram(height_values, bin_edges)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    assert np.size(bin_centers) == histo.size
    
    return bin_centers, histo

def roughness_1d(
    height_values : np.ndarray,
    results_file : sm.SmartFile
    ) -> None :
    """
    Computes the 1-d roughness of the image and its standard deviation.

    This function computes the 1-d roughness along each fast scan direction of the image (x axis) and then
    it returns the mean of all these roughness values. This way of computing the roughness allows to return also
    the standard deviation, which is often taken as the uncertainty associated to the mean roughness value.
    Finally, the mean of each 1-d roughness values and its standard deviation are written in `results_file` if its internal 
    state `enabled` is set to True.

    Parameters
    -----------
    height_values: ndarray
        2-d grid containing the height values.
    results_file: SmartFile
        File-like object that records results if its internal `enabled` flag is True.

    See Also
    --------
    np.std: function that computes the standard deviation along a certain axis.
    np.mean: function that computes the arithmetic mean along a certain axis.
    sm.SmartFile: class to create files on which it is possible to write if their internal state `enabled` is set to True.
    roughness_2d: computes the roughness by exploiting the standard deviation of all the image data.

    Notes
    -----
    The 1-d roughness expression for one fast scan direction is equal to the standard deviation computed for the data
    in that line, this is the reason for which the numpy standard deviation function is used to return the roughness
    in that direction.
    """
    roughness_array = np.std(height_values, axis=1) #used because it returns the same expression as the roughness expression
    roughness = np.mean(roughness_array)
    standard_deviation = np.std(roughness_array)

    results_file.write("1D ROUGHNESS\n" +
                       f"roughness = {roughness} nm\n" +
                       f"standard deviation = {standard_deviation} nm\n" +
                       "----------------------------\n")
    
def roughness_2d(
    height_values : np.ndarray,
    results_file : sm.SmartFile
    ) -> None :
    """
    Computes the 2-d roughness of the image.

    This function computes the 2-d roughness of the image by exploiting the `np.std` function.
    The roughness value computed in this way is than written in `results_file` if its internal 
    state `enabled` is set to True.

    Parameters
    -----------
    height_values: ndarray
        2-d grid containing the height values.
    results_file: SmartFile
        File-like object that records results if its internal `enabled` flag is True.

    See Also
    --------
    np.std: function that computes the standard deviation along a certain axis.
    sm.SmartFile: class to create files on which it is possible to write if their internal state `enabled` is set to True.
    roughness_1d: computes the roughness by mediating the 1-d roughness values of each fast scan line.

    Notes
    -----
    The 2-d roughness expression is equal to the standard deviation computed for all the data stored in the image, 
    this is the reason for which the numpy standard deviation function is used to return the roughness
    in that direction.
    """
    roughness = np.std(height_values) #used because it returns the same expression as the roughness expression

    results_file.write("2D ROUGHNESS\n" +
                       f"roughness = {roughness} nm\n" +
                       "----------------------------\n"
                       )

