import argparse
import json
import image
import data_analysis

parser = argparse.ArgumentParser("AFM image analyser")
parser.add_argument('--log', help="Generate a .log file with the image analysis results and parameters")

with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

height_values = image.read_tiff(settings["file_specifications"]["input_file_name"])
coordinate_grid = image.create_coordinate_grid(settings["file_specifications"]["scanning_rate"], settings["file_specifications"]["image_length"])

if settings["data_analysis"]["common_plane_subtraction"].lower() == "yes":
    height_values = data_analysis.common_plane_subtraction(height_values, coordinate_grid)
elif settings["data_analysis"]["common_plane_subtraction"].lower() == "no":
    height_values = height_values
else:
    raise TypeError("Variable inserted for 'common_plane_subtraction' in settings.json is not valid. Please insert 'yes' or 'no' (variable is not case-sensitive).")

if settings["data_analysis"]["data_shift"].lower() == "minimum":
    height_values = data_analysis.shift_min(height_values)
elif settings["data_analysis"]["data_shift"].lower() == "mean":
    height_values = data_analysis.shift_mean(height_values)
else:
    raise TypeError("Variable inserted for 'data_shift' in settings.json is not valid. Please insert 'minimum' or 'mean' (variable is not case-sensitive).")

image.plot_2d_image(settings["file_specifications"]["2D_image_output_file_name"], height_values, coordinate_grid, settings["graphics"]["color_map"])
image.plot_3d_image(settings["file_specifications"]["3D_image_output_file_name"], height_values, coordinate_grid, settings["graphics"]["color_map"])

