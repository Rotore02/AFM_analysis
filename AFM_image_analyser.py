import argparse
import os
import json
import image
import data_analysis

parser = argparse.ArgumentParser("AFM image analyser")
parser.add_argument('--log', help="Generate a .log file with the image analysis results and parameters")
