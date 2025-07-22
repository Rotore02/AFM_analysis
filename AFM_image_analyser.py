import argparse
import json
import graphics
import data_analysis
import image_correction
import smart_file as sm
from functools import partial
import inspect

def build_image_correction_pipeline(full_function_list, results_file, settings_list):
    function_exe_list = [
        (func, cond) for func, cond in full_function_list if cond in settings_list
    ]

    def apply_pipeline(obj, function_exe_list, file_name):
        for function, cond in function_exe_list:
            n_args = len(inspect.signature(function).parameters)
            if n_args == 2:
                obj = function(obj, cond)
            elif n_args == 3:
                obj = function(obj, file_name, cond)
            else:
                raise ValueError(f"Function {function.__name__} must accept 2, or 3 arguments.")
        return obj
    
    return partial(
        apply_pipeline,
        function_exe_list=function_exe_list,
        file_name=results_file
    )

def main():
    parser = argparse.ArgumentParser("AFM graphics analyser")
    parser.add_argument('--results', nargs='?', const='results.txt', help="Write analysis results to a file (default: results.txt). You can optionally specify the file name.")
    args = parser.parse_args()

    results_file = sm.SmartFile()

    if args.results:
        results_file.setup(f"output_files/{args.results}")

    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)

    height_values = graphics.read_tiff(settings["files_specs_and_graphics"]["input_file_name"])
    
    correct_graphics = build_image_correction_pipeline(
    [
        (image_correction.common_plane_subtraction, "yes"),
        (image_correction.line_drift_subtraction, "linear"),
        (image_correction.mean_drift_subtraction, "mean"),
        (image_correction.shift_min, "minimum"),
        (image_correction.shift_mean, "mean"),
    ],
        results_file,
    [
        settings["image_correction"]["common_plane_subtraction"],
        settings["image_correction"]["line_drift_correction"],
        settings["image_correction"]["data_shift"]
    ]
    )
    corrected_heights = correct_graphics(height_values)
    
    coordinate_grid = graphics.create_coordinate_grid(settings["files_specs_and_graphics"]["scanning_rate"], settings["files_specs_and_graphics"]["image_length"])
    graphics.plot_2d_image(settings["files_specs_and_graphics"]["2D_image_output_file_name"], corrected_heights, coordinate_grid, settings["files_specs_and_graphics"]["color_map"])
    graphics.plot_3d_image(settings["files_specs_and_graphics"]["3D_image_output_file_name"], corrected_heights, coordinate_grid, settings["files_specs_and_graphics"]["color_map"])
    
    if settings["data_analysis"]["height_values_distribution"].lower() == "yes":
        histogram = data_analysis.height_distribution(height_values)
        ax_labels = ("height values (nm)", "counts")
        graphics.custom_plot(histogram, ax_labels, "Height Values Distribution", out_file_name="output_files/height_values_distribution.pdf")
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

    results_file.close()

if __name__ == "__main__":
    main()