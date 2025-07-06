import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

scanning_rate = 1e6 
image_width = 256e-6
file = 'pn_junction.tiff'
color_map = 'viridis'

def read_tiff(file):
    tiff_file = tiff.TiffFile(f"input_files/{file}")
    return tiff_file.asarray()

def create_image_grid(scanning_rate, image_width):
    N_points = int(image_width * scanning_rate)
    x_scan_direction = np.linspace(0, image_width, N_points)
    y_scan_direction = np.linspace(0, image_width, N_points)
    return np.meshgrid(x_scan_direction,y_scan_direction)

def plot_afm_image(z, real_space_coordinates, color_map, output_file_name):
    """
    Plot AFM data as a 2D color map.

    Plot the data stored in the z 2-d grid labeling the x and y axis of the plot with the data stored in real_space_coordinates

    Parameters:
    x, y: 1D arrays of real-space coordinates (µm or nm)
    - z: 2D array of height values with shape (len(y), len(x))
    - cmap: colormap for surface (e.g., 'viridis', 'inferno', 'plasma')
    - figsize: size of the figure
    - zlabel: label for the colorbar (typically height)
    - title: plot title
    - show_scale_bar: whether to draw a scale bar in bottom left
    - scale_bar_length: scale bar size in same units as x (e.g. µm)
    """

    x,y = real_space_coordinates
    real_space_map = [x.min(), x.max(), y.max(), y.min()]

    fig, ax = plt.subplots(figsize=(8,6))
    im = ax.imshow(z, extent=real_space_map, cmap=color_map, aspect='auto')

    ax.set_xlabel('X (µm)')
    ax.set_ylabel('Y (µm)')

    color_bar = plt.colorbar(im, ax=ax)
    color_bar.set_label("Height (nm)")

    plt.tight_layout()
    plt.savefig(f"output_files/{output_file_name}")
