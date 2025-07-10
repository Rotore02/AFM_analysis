import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np

def read_tiff(
    file_name : str  
    ) -> np.ndarray[float]:
    """
    Reads the tiff file.

    Reads an input tiff file and returns as output a 2-d array where each value is a corrisponding color in the tiff image.

    Parameters
    -----------
    file: str
          Name of the tiff file that needs to be read.

    Returns
    --------
    ndarray[float]
            2-d grid containing numerical values representing each pixel color.
    
    Raises
    ------
    TypeError
              If the file does is not a tiff file or does not have the .tiff or .tif extensions (non case-sensitive).
    FileNotFoundError
                     If the input file does not exist or is not in the 'input_files/' directory.
    """
    if not file_name.lower().endswith((".tiff", ".tif")):
        raise TypeError("Input file is not a tiff file or the typed input name does not end with .tiff or .tif. Please make sure the input file type is tiff and its name contains the .tiff or .tif extension (non case-sensitive).")
    try:
        tiff_file = tiff.TiffFile(f"input_files/{file_name}")
    except FileNotFoundError:
        raise FileNotFoundError("Input file not found in 'input_files/' directory. Please check that the file exists and is in the 'input_files/' directory.")
    return tiff_file.asarray()

def create_coordinate_grid(
    scanning_rate : float, #Number of aquired points per unit length [m^(-1)], is set manually in the AFM
    image_width : float #Total length of the image [m], is set manually in the AFM
    ) -> tuple[np.ndarray[float],...]:
    """
    Creates the coordinate grid in real space.

    Takes as inputs the scanning rate [m^(-1)] and the image width [m] and produces a couple of the coordinate matrices of the image in real space.

    Parameters
    ----------
    scanning_rate: float
                   number of points per unit length.
    image_width: float
                 edge length of the image.
    
    Returns
    -------
    tuple[ndarray[float]]
            a couple of 2-d coordinate matrices with the dimensions of the real space image.

    Raises
    ------
    ValueError
              If the two inputs Image_width and scanning_rate does not produce an integer number after multiplication.
    """
    N_points = int(round(image_width * scanning_rate))
    if not isinstance(N_points, int):
        raise ValueError("Scanning rate and image width product is not an integer number. Please check if those values are inserted correctly")
    scan_direction = np.linspace(0, image_width, N_points)
    return np.meshgrid(scan_direction,scan_direction)

def plot_2d_image(
    output_file_name : str,
    height_values : np.ndarray[float], #This is a 2-d array
    coordinate_grid, #This is a couple of 2-d arrays
    color_map='Greys') -> None:
    """
    Plots AFM data as a 2D color map.

    Makes a 2-d plot of the height values stored in the 2-d grid labeling the x and y axis of the plot with the coordinates stored in coordinate_grid

    Parameters:
    -----------
    output_file_name: str
                      Name of the output file that will be saved in the folder 'output_files/'.
    height_values: ndarray[float]
                   2-d grid with height values to be represented in the image.
    coordinate_grid: tuple(ndarray[float])
                            Couple of 2-d arrays representing the x and y real space coordinates for each image pixel.
    color_map: str
               Set of colors to plot the image. Default is 'Greys'.
    """
    if color_map not in plt.colormaps():
        raise TypeError("The inserted color map does not exist. You can find all the valid color maps at ...(link to documentation)...)")
    x,y = coordinate_grid
    real_space_map = [x.min(), x.max(), y.max(), y.min()]
    fig, ax = plt.subplots(figsize=(8,6))
    im = ax.imshow(height_values, extent=real_space_map, cmap=color_map, aspect='auto')
    ax.set_xlabel('X (µm)')
    ax.set_ylabel('Y (µm)')
    color_bar = plt.colorbar(im, ax=ax)
    color_bar.set_label("Height (nm)")
    plt.tight_layout()
    plt.savefig(f"output_files/{output_file_name}")

def plot_3d_image(
    output_file_name : str,
    height_values : np.ndarray[float], #This is a 2-d array
    coordinate_grid, #This is a couple of 2-d arrays
    color_map='Greys') -> None:
    """
    Plots AFM data as a 3D color map.

    Makes a 3-d plot of the height values stored in the 2-d grid labeling the x and y axis of the plot with the coordinates stored in coordinate_grid

    Parameters:
    -----------
    output_file_name: str
                      Name of the output file that will be saved in the folder 'output_files/'.
    height_values: ndarray[float]
                   2-d grid with height values to be represented in the image.
    coordinate_grid: tuple(ndarray[float])
                            Couple of 2-d arrays representing the x and y real space coordinates for each image pixel.
    color_map: str
               Set of colors to plot the image. Default is 'Greys'.
    """
    if color_map not in plt.colormaps():
        raise TypeError("The inserted color map does not exist. You can find all the valid color maps at ...(link to documentation)...)")
    x,y = coordinate_grid
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, height_values, alpha=0.9, label='Dati', cmap=color_map)
    ax.set_xlabel('X (µm)')
    ax.set_ylabel('Y (µm)')
    ax.set_zlabel('Z (nm)')
    color_bar = plt.colorbar(ax, ax=ax)
    color_bar.set_label("Height (nm)")
    plt.tight_layout()
    plt.savefig(f"output_files/{output_file_name}")