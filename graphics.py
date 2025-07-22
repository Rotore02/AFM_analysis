import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np
import os

def read_tiff(
    file_name : str  
    ) -> np.ndarray:
    """
    Reads the tiff file.

    Reads an input tiff file and returns as output a 2-d array where each value is a corrisponding color in the tiff image.

    Parameters
    -----------
    file_name: str
          Name of the tiff file that needs to be read.

    Returns
    --------
    ndarray
            2-d grid containing numerical values representing each pixel color.
    
    Raises
    ------
    TypeError
              If the file does is not a tiff file or does not have the .tiff or .tif extensions (non case-sensitive).
    FileNotFoundError
                     If the input file does not exist or is not in the 'input_files/' directory.

    See Also
    --------
    tiff.TiffFile: class that reads the tiff file.
    tiff.TiffFile.asarray: method that converts the image in a numpy array.
    """
    input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input_files", file_name)
    if not input_file_path.lower().endswith((".tiff", ".tif")):
        raise TypeError("Input file is not a tiff file or the typed input name does not end with .tiff or .tif. " \
                        "Please make sure the input file type is tiff and its name contains the .tiff or .tif extension " \
                        "(extension is non case-sensitive).")
    
    if not os.path.isfile(input_file_path):
        raise FileNotFoundError(f"File {file_name} not found")

    return tiff.TiffFile(input_file_path).asarray()

def create_coordinate_grid(
    scanning_rate : float, #Number of aquired points per unit length [m^(-1)], is set manually in the AFM
    image_width : float #Total length of the image [m], is set manually in the AFM
    ) -> tuple[np.ndarray,np.ndarray]:
    """
    Creates the coordinate grid in real space.

    Takes as inputs the scanning rate [m^(-1)] and the image width [m] and produces a couple of coordinate
    matrices of the image in real space. This is done to create a set of coordinates that represent the actual 
    area scanned by the AFM, where to each coordinate corresponds an height value.

    Parameters
    ----------
    scanning_rate: float
                   Number of acquired points per unit length.
    image_width: float
                 Edge length of the image.
    
    Returns
    -------
    tuple of two ndarray
            A couple of 2-d coordinate matrices with the dimensions of the scanned area of the sample.

    See Also
    --------
    np.meshgrid : Generates coordinate matrices from coordinate vectors.
    """
    N_points = int(round(image_width * scanning_rate))
    scan_direction = np.linspace(0, image_width, N_points)
    return np.meshgrid(scan_direction,scan_direction)

def plot_2d_image(
    output_file_name : str,
    height_values : np.ndarray, #This is a 2-d array
    coordinate_grid : tuple[np.ndarray, np.ndarray], #This is a couple of 2-d arrays
    color_map='Greys') -> None:
    """
    Plots AFM data as a 2D color map.

    Makes a 2-d plot of the height values stored in the 2-d grid labeling the x and y axis of the plot with the 
    coordinates stored in `coordinate_grid`.

    Parameters
    -----------
    output_file_name: str
                      Name of the output file that will be saved in the folder 'output_files/'.
    height_values: ndarray
                   2-d grid with height values to be represented in the image.
    coordinate_grid: tuple of two ndarray
                            Couple of 2-d arrays representing the x and y real space coordinates for each image pixel.
    color_map: str
               Set of colors to plot the image. Default is `Greys`.

    Raises
    ------
    TypeError
             If the inserted color map does not exist.
    ValueError
              If the scanning rate and the image length are not correct.

    See Also
    --------
    plt.colormaps: register with a list of all colormaps aviable from matplotlib.
    """
    if color_map not in plt.colormaps():
        raise TypeError("The inserted color map does not exist. You can find all the valid color maps at " \
                        "https://matplotlib.org/stable/users/explain/colors/colormaps.html")
    if not coordinate_grid[0].shape == height_values.shape or not coordinate_grid[1] .shape == height_values.shape:
        raise ValueError("Coordinate matrix and height values array have different shapes. " \
                         "Please check that the scanning rate and the image length are inserted correctly.")
    x,y = coordinate_grid
    real_space_map = [x.min(), x.max(), y.max(), y.min()]
    fig, ax = plt.subplots(figsize=(8,6))
    im = ax.imshow(height_values, extent=real_space_map, cmap=color_map, aspect='auto')
    ax.set_xlabel('X (µm)')
    ax.set_ylabel('Y (µm)')
    color_bar = plt.colorbar(im, ax=ax)
    color_bar.set_label("Height (nm)")
    plt.tight_layout()
    output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_files", output_file_name)
    plt.savefig(output_file_path)

def plot_3d_image(
    output_file_name : str,
    height_values : np.ndarray, #This is a 2-d array
    coordinate_grid : tuple[np.ndarray, np.ndarray], #This is a couple of 2-d arrays
    color_map='Greys') -> None:
    """
    Plots AFM data as a 3D color map.

    Makes a 3-d plot of the height values stored in the 2-d grid labeling the x and y axis of the plot with the 
    coordinates stored in `coordinate_grid`.

    Parameters:
    -----------
    output_file_name: str
                      Name of the output file that will be saved in the folder 'output_files/'.
    height_values: ndarray
                   2-d grid with height values to be represented in the image.
    coordinate_grid: tuple of two ndarray
                            Couple of 2-d arrays representing the x and y real space coordinates for each image pixel.
    color_map: str
               Set of colors to plot the image. Default is `Greys`.

    Raises
    ------
    TypeError
             If the inserted color map does not exist.
    ValueError
              If the scanning rate and the image length are not correct.

    See Also
    --------
    plt.colormaps: register with a list of all colormaps aviable from matplotlib.
    """
    if color_map not in plt.colormaps():
        raise TypeError("The inserted color map does not exist. You can find all the valid color maps at " \
                        "https://matplotlib.org/stable/users/explain/colors/colormaps.html")
    if not coordinate_grid[0].shape == height_values.shape or not coordinate_grid[1] .shape == height_values.shape:
        raise ValueError("Coordinate matrix and height values array have different shapes. " \
                         "Please check that the scanning rate and the image length are inserted correctly.")
    x,y = coordinate_grid
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, height_values, alpha=0.9, cmap=color_map)
    ax.set_xlabel('X (µm)')
    ax.set_ylabel('Y (µm)')
    ax.set_zlabel('Z (nm)')
    color_bar = plt.colorbar(surf, ax=ax)
    color_bar.set_label("Height (nm)")
    plt.tight_layout()
    output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_files", output_file_name)
    plt.savefig(output_file_path)

def custom_plot(
    data : tuple[np.ndarray, np.ndarray],
    ax_labels = ("x", "y"),
    title = "Plot",
    color = "black",
    output_file_name = "output_plot.pdf"
    ) -> None:
    """
    Plots the values stored in `data`.

    This function generates a plot of the data stored in `data`, where `data[0]` is the x axis and `data[1]` is the y axis.

    Parameters
    ----------
    data: tuple of two ndarray
          Data of the x and y axis of the plot, respectively.
    ax_labels: tuple of two strings
               labels for the x and y axis, respectively. Default is `("x", "y")`.
    title: str
           Title of the plot. Default is `"Plot"`.
    color: str
           Color of the plotted data. Default is `"black"`.
    out_file_name: str
                   Name of the output plot file. Default is `"output_plot.pdf"`.

    See Also
    --------
    plt.plot: function used to plot the data.
    """
    if data is None or data[0] is None or data[1] is None:
        return
    plt.figure(figsize=(10, 6))
    plt.plot(data[0], data[1], color=color)
    plt.title(title)
    plt.xlabel(ax_labels[0])
    plt.ylabel(ax_labels[1])
    plt.grid("True")
    plt.tight_layout()
    output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file_name)
    plt.savefig(output_file_path)