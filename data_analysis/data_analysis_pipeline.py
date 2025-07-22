from . import data_analysis_functions
from AFM_analisys import graphics

def build_data_analysis_pipeline(settings, results_file, height_values):
    pipeline = []

    dist_setting = settings["data_analysis"]["height_values_distribution"].lower()
    dist_map = {
        "yes": lambda: graphics.custom_plot(
            data_analysis_functions.height_distribution(height_values),
            ("height values (nm)", "counts"),
            "Height Values Distribution",
            output_file_name="output_files/height_values_distribution.pdf"
        ),
        "no": None
    }
    if dist_setting not in dist_map:
        raise TypeError("Invalid value for 'height_values_distribution'. Use 'yes' or 'no'.")
    
    dist_func = dist_map[dist_setting]
    if dist_func is not None:
        pipeline.append(dist_func)

    rough_setting = settings["data_analysis"]["roughness"].lower()
    rough_map = {
        "1d": lambda: data_analysis_functions.roughness_1d(height_values, results_file),
        "2d": lambda: data_analysis_functions.roughness_2d(height_values, results_file),
        "no": None
    }
    if rough_setting not in rough_map:
        raise TypeError("Invalid value for 'roughness'. Use '1d', '2d' or 'no'.")
    
    rough_func = rough_map[rough_setting]
    if rough_func is not None:
        pipeline.append(rough_func)

    return pipeline