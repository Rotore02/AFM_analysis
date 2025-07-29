"""
data_analysis_pipeline module
===================
This module contains a single function that creates the pipeline 
of functions to perform data analysis.

This module contains a function that, based on a settings 
dictionary, creates the pipeline of functions to perform the
data analysis of the AFM image data. The functions are taken 
from the 'data_analysis_functions' module.

Author: Alessandro Rotondi
"""

from . import data_analysis_functions
from afm_analysis import graphics
from functools import partial
from typing import TYPE_CHECKING
import numpy as np

def build_data_analysis_pipeline(
    settings : dict, 
    results_file : str, 
    height_values : np.ndarray
) -> list:
    """
    Builds the pipeline of execution of the data analysis functions.

    This functions defines a dictionary for each data analysis action. 
    For each action some keywords are defined and to each keyword is 
    associated a function (or a combination of them) inside the 
    `data_analysis_functions` module. For each action, a function is 
    added to the execution pipeline based on the keywords parsed from 
    the `settings` dictionary. Some functions write their results in 
    `results_file` (`sm.SmartFile` object), which internally can 
    select wether the writing is performed or not.

    Parameters
    ----------
    settings: dict
        File containing the keywords to choose the executed functions.
    results_file: SmartFile
        File-like object that records results if its internal `enabled` 
        flag is True.
    height_values: ndarray
        2-d grid containing the height values.

    Returns
    -------
    list
        list of the lambda functions to be executed based on the 
        `settings` file.

    Raises
    ------
    TypeError
        If the height distribution keyword in the `settings` file is 
        not valid.
    TypeError
        If the roughness keyword in the `settings` file is not valid.

    See Also
    --------
    data_analysis_functions: module with all the data analysis 
    functions.
    sm.SmartFile: class to create files on which it is possible to 
    write if their internal state `enabled` is set to True.
    functools.partial: class to create partial functions to fix some 
    arguments.
    """
    pipeline = []

    distribution_dict = {
        "yes": lambda: graphics.custom_plot(
            data_analysis_functions.height_distribution(height_values),
            ("height values (nm)", "counts"),
            "Height Values Distribution",
            output_file_name="height_values_distribution.pdf"
        ),
        "no": lambda: None
    }

    roughness_dict = {
        "1d": lambda: partial(
            data_analysis_functions.roughness_1d, 
            height_values, 
            results_file
        ),
        "2d": lambda: partial(
            data_analysis_functions.roughness_2d, 
            height_values, 
            results_file
        ),
        "no": lambda: None
    }

    dist_setting = settings[
        "data_analysis"
    ][
        "height_values_distribution"
    ].lower()
    rough_setting = settings[
        "data_analysis"
    ][
        "roughness"
    ].lower()

    try:
        dist_func = distribution_dict[dist_setting]()
    except KeyError:
        raise TypeError(
            "Invalid value for 'height_values_distribution'. " \
            "Use 'yes' or 'no'."
        ) from None
    if dist_func is not None:
        pipeline.append(dist_func)

    try:
        rough_func = roughness_dict[rough_setting]()
    except KeyError:
        raise TypeError(
            "Invalid value for 'roughness'. " \
            "Use '1d', '2d' or 'no'."
        ) from None
    if rough_func is not None:
        pipeline.append(rough_func)

    return pipeline