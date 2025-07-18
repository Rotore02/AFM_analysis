import argparse
import json
import image
import data_analysis
import warnings
import smart_file as sm

parser = argparse.ArgumentParser("AFM image analyser")
parser.add_argument('--results', nargs='?', const='results.txt', help="Write analysis results to a file (default: results.txt). You can optionally specify the file name.")
args = parser.parse_args()

results_file = sm.SmartFile()

if args.results:
    results_file.setup(args.results)

with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

height_values = image.read_tiff(settings["file_specifications"]["input_file_name"])
coordinate_grid = image.create_coordinate_grid(settings["file_specifications"]["scanning_rate"], settings["file_specifications"]["image_length"])

if settings["data_analysis"]["common_plane_subtraction"].lower() == "yes":
    height_values = data_analysis.common_plane_subtraction(height_values, results_file)
elif settings["data_analysis"]["common_plane_subtraction"].lower() == "no":
    pass
else:
    raise TypeError("Variable inserted for 'common_plane_subtraction' in settings.json is not valid. Please insert 'yes' or 'no' (variable is not case-sensitive).")

if settings["data_analysis"]["line_drift_correction"].lower() == "linear":
    if settings["data_analysis"]["common_plane_subtraction"].lower() == "yes":
        height_values = data_analysis.line_drift_subtraction(height_values, results_file)
    else:
        height_values = data_analysis.common_plane_subtraction(height_values, results_file)
        height_values = data_analysis.line_drift_subtraction(height_values, results_file)
        warnings.warn("Linear drift correction was requested without plane subtraction. Common plane subtraction has been applied automatically to ensure accuracy.", UserWarning)
elif settings["data_analysis"]["line_drift_correction"].lower() == "mean":
    if settings["data_analysis"]["common_plane_subtraction"].lower() == "yes":
        height_values = data_analysis.mean_drift_subtraction(height_values, results_file)
    else:
        height_values = data_analysis.common_plane_subtraction(height_values, results_file)
        height_values = data_analysis.line_drift_subtraction(height_values, results_file)
        warnings.warn("Linear drift correction was requested without plane subtraction. Common plane subtraction has been applied automatically to ensure accuracy.", UserWarning)
elif settings["data_analysis"]["line_drift_correction"].lower() == "no":
    pass
else:
    raise TypeError("Variable inserted for 'linear_drift_subtraction' in settings.json is not valid. Please insert 'yes' or 'no' (variable is not case-sensitive).")

if settings["data_analysis"]["data_shift"].lower() == "minimum":
    height_values = data_analysis.shift_min(height_values)
elif settings["data_analysis"]["data_shift"].lower() == "mean":
    height_values = data_analysis.shift_mean(height_values)
elif settings["data_analysis"]["data_shift"].lower() == "no":
    pass
else:
    raise TypeError("Variable inserted for 'data_shift' in settings.json is not valid. Please insert 'minimum' or 'mean' (variable is not case-sensitive).")

if settings["data_analysis"]["height_values_distribution"].lower() == "yes":
    histogram = data_analysis.height_distribution(height_values)
    ax_labels = ("height values (nm)", "counts")
    image.custom_plot(histogram, ax_labels, "Height Values Distribution", out_file_name="output_files/height_values_distribution.pdf")
elif settings["data_analysis"]["height_values_distribution"].lower() == "no":
    pass
else:
    raise TypeError("Variable inserted for 'height_values_distribution' in settings.json is not valid. Please insert 'yes' or 'no' (variable is not case-sensitive).")

if settings["data_analysis"]["roughness"].lower() == "1d":
    data_analysis.roughness_1d(height_values, results_file)
elif settings["data_analysis"]["roughness"].lower() == "2d":
    data_analysis.roughness_2d(height_values, results_file)
elif settings["data_analysis"]["roughness"].lower() == "no":
    pass
else:
    raise TypeError("Variable inserted for 'roughness' in settings.json is not valid. Please insert '1d', '2d' or 'no' (variable is not case-sensitive).")


image.plot_2d_image(settings["file_specifications"]["2D_image_output_file_name"], height_values, coordinate_grid, settings["graphics"]["color_map"])
image.plot_3d_image(settings["file_specifications"]["3D_image_output_file_name"], height_values, coordinate_grid, settings["graphics"]["color_map"])

results_file.close()