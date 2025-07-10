import argparse
import os
import json
import image
import data_analysis

parser = argparse.ArgumentParser("AFM image analyser")
parser.add_argument('--log', help="Generate a .log file with the image analysis results and parameters")

with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

height_values = image.read_tiff(settings["file_specifications"]["input_file_name"])
coordinate_grid = image.create_coordinate_grid(settings["file_specifications"]["scanning_rate"], settings["file_specifications"]["image_width"])

if settings["data_analysis"]["common_plane_subtraction"].lower() == "y":
    height_values = data_analysis.common_plane_subtraction(height_values, coordinate_grid)

