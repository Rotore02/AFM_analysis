import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np

def read_tiff(
    file : str  
    ) -> np.ndarray:
    """
    Reads the tiff file.

    Reads an input tiff file and returns as output a 2-d array where each value is a corrisponding color in the tiff image.

    Parameters
    -----------
    file: str
          Tiff file that needs to be read.

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
    """
    if not file.lower().endswith((".tiff", ".tif")):
        raise TypeError("Input file is not a tiff file or the typed input name does not end with .tiff or .tif. Please make sure the input file type is tiff and its name contains the .tiff or .tif extension (non case-sensitive).")
    try:
        tiff_file = tiff.TiffFile(f"input_files/{file}")
    except FileNotFoundError:
        raise FileNotFoundError("Input file not found in 'input_files/' directory. Please check that the file exists and is in the 'input_files/' directory.")
    tiff.TiffFile.close()
    return tiff_file.asarray()

def create_image_grid(
                    scanning_rate : float,  #number of aquired points per unit length [m^(-1)], is set manually in the AFM
                    image_width : float  #total length of the image [m], is set manually in the AFM
                    ) -> np.ndarray:
    """
    Creates the image grid in real space.

    Takes as inputs the scanning rate [m^(-1)] and the image width [m] and produces a 2-d array with the real space dimensions of the image.

    Parameters
    ----------
    scanning_rate: float
                   number of points per unit length.
    image_width: float
                 edge length of the image.
    
    Returns
    -------
    ndarray
            2-d grid with the dimensions of the real space image.

    Raises
    ------
    ValueError
              If the two inputs Image_width and scanning_rate does not produce an integer number after multiplication.
    """
    N_points = int(round(image_width * scanning_rate))
    if not isinstance(N_points, int):
        raise ValueError("Scanning rate and image width product is not an integer number. Please check if those values are inserted correctly")
    else:
        x_scan_direction = np.linspace(0, image_width, N_points)
        y_scan_direction = np.linspace(0, image_width, N_points)
        return np.meshgrid(x_scan_direction,y_scan_direction)

def plot_afm_image(output_file_name, height_values, real_space_coordinates, color_map='grey'):
    """
    Plots AFM data as a 2D color map.

    Plots the data stored in the z 2-d grid labeling the x and y axis of the plot with the data stored in real_space_coordinates

    Parameters:
    -----------
    output_file_name: str
                      Name of the output file that will be saved in the folder 'output_files/'.
    height_values: ndarray
                   2-d grid with z height values to be represented in the image.
    real_space_coordinates
    """

    x,y = real_space_coordinates
    real_space_map = [x.min(), x.max(), y.max(), y.min()]

    fig, ax = plt.subplots(figsize=(8,6))
    im = ax.imshow(height_values, extent=real_space_map, cmap=color_map, aspect='auto')

    ax.set_xlabel('X (µm)')
    ax.set_ylabel('Y (µm)')

    color_bar = plt.colorbar(im, ax=ax)
    color_bar.set_label("Height (nm)")

    plt.tight_layout()
    plt.savefig(f"output_files/{output_file_name}")