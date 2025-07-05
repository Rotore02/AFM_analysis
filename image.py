import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np

SCANNING_RATE = 1e6
IMAGE_WIDTH = 256e6

def read_tiff(file_):
    tif = tiff.TiffFile(file_)
    return tif.asarray()
