import argparse
import json
import os
from afm_analysis import graphics
from .image_correction import image_correction_pipeline
from .data_analysis import data_analysis_pipeline
from afm_analysis import smart_file as sm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))        

parser = argparse.ArgumentParser("AFM image analyser")
parser.add_argument('--results', nargs='?', const='results.txt', 
    help="Write analysis results to a file (default: results.txt). " \
    "You can optionally specify the file name.")
args = parser.parse_args()
results_file = sm.SmartFile()
if args.results:
    output_dir = os.path.join(BASE_DIR, "output_files")
    os.makedirs(output_dir, exist_ok=True)
    results_path = os.path.join(output_dir, args.results)
    results_file.setup(results_path)

settings_path = os.path.join(BASE_DIR, 'settings.json')
with open(settings_path, 'r') as settings_file:
    settings = json.load(settings_file)

height_values = graphics.read_tiff(
    settings["files_specifications"]["input_file_name"]
)

im_corr_pipeline = image_correction_pipeline.build_image_correction_pipeline(
    settings, results_file
)
for function in im_corr_pipeline:
    height_values = function(height_values)
data_an_pipeline = data_analysis_pipeline.build_data_analysis_pipeline(
    settings, results_file, height_values
)
for function in data_an_pipeline:
    function()

coordinate_grid = graphics.create_coordinate_grid(
    settings["files_specifications"]["scanning_rate"], 
    settings["files_specifications"]["image_length"]
)
graphics.plot_2d_image(
    settings["files_specifications"]["2D_image_output_file_name"], 
    height_values, coordinate_grid, settings["graphics"]["color_map"]
)
graphics.plot_3d_image(
    settings["files_specifications"]["3D_image_output_file_name"], 
    height_values, coordinate_grid, settings["graphics"]["color_map"]
)

results_file.close()