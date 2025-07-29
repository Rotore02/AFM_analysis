"""
image_correction_pipeline module
===================
This module contains a single function that creates a pipeline 
of functions to perform image correction.

This module contains a function that, based on a settings 
dictionary, creates the pipeline of functions to correct
the AFM image data. The functions are taken from the
'image_correction_functions' module.

Author: Alessandro Rotondi
"""

import warnings
from . import image_correction_functions
from functools import partial

def build_image_correction_pipeline(
    settings : dict, 
    results_file : str
    ) -> list:
    """
    Builds the pipeline of execution of the image correction 
    functions.

    This functions defines a dictionary for each image correction 
    action. For each action some keywords are defined and to each 
    keyword is associated a function (or a combination of them) inside
    the `image_correction_functions` module. For each action, a 
    function is added to the execution pipeline based on the keywords 
    parsed from the `settings` dictionary. Some functions write their 
    results in `results_file` (`sm.SmartFile` object), which 
    internally can select wether the writing is performed or not.

    Parameters
    ----------
    settings: dict
        File containing the keywords to choose the executed functions
    results_file: SmartFile
        File-like object that records results if its internal 
        `enabled` flag is True.

    Returns
    -------
    list
        list of the functions to be executed based on the `settings` 
        file.

    Raises
    ------
    TypeError
        If the plane subtraction keyword in the `settings` file is 
        not valid.
    TypeError
        If the line subtraction keyword in the `settings` file is 
        not valid.
    TypeError
        If the data shift keyword in the `settings` file is not 
        valid.
    UserWarning
        If any kind of line drift correction is requested without 
        plane subtraction.

    See Also
    --------
    image_correction_functions: module with all the image correcting 
    functions.
    sm.SmartFile: class to create files on which it is possible to 
    write if their internal state `enabled` is set to True.
    functools.partial: class to create partial functions to fix some 
    arguments.
    """
    pipeline = []

    plane_subtraction_dict = {
        "yes": lambda: partial(
            image_correction_functions.common_plane_subtraction, 
            results_file=results_file
            ),
        "no": lambda: None
    }

    # If plane_subtraction is not performed while line drift is, 
    # than plane subtraction is also added to pipeline[]
    drift_correction_dict = {
        "linear": lambda plane_subtraction: [
            partial(
                image_correction_functions.common_plane_subtraction, 
                results_file=results_file
            ) 
        ] * (plane_subtraction == "no") + [                                                         
            partial(
                image_correction_functions.linear_drift_subtraction, 
                results_file=results_file
            )
        ],
        "mean": lambda plane_subtraction: [
            partial(
                image_correction_functions.common_plane_subtraction, 
                results_file=results_file
            )
        ] * (plane_subtraction == "no") + [
            partial(
                image_correction_functions.mean_drift_subtraction, 
                results_file=results_file
            )
        ],
        "no": lambda plane_subtraction: None
    }

    data_shift_dict = {
        "minimum":lambda: image_correction_functions.shift_min,
        "mean": lambda: image_correction_functions.shift_mean,
        "no": lambda: None
    }

    plane_setting = settings[
        "image_correction"
    ][
        "common_plane_subtraction"
    ].lower()
    drift_setting = settings[
        "image_correction"
    ][
        "line_drift_correction"
    ].lower()
    data_shift_setting = settings[
        "image_correction"
    ][
        "data_shift"
    ].lower()

    try:
        plane_sub = plane_subtraction_dict[plane_setting]()
    except KeyError:
        raise TypeError(
            "Invalid value for 'common_plane_subtraction'. " \
            "Use 'yes' or 'no' (variable is not case-sensitive)."
        ) from None
    if plane_sub is not None:
        pipeline.append(plane_sub)

    try:
        drift_corr = drift_correction_dict[drift_setting](plane_setting)
    except KeyError:
        raise TypeError(
            "Invalid value for 'line_drift_correction'. " \
            "Use 'linear', 'mean' or 'no' (variable is not case-sensitive)."
        ) from None
    if drift_corr is not None:
        pipeline.extend(drift_corr)

    if drift_setting != "no" and plane_setting == "no":
        warnings.warn(
            "Drift correction requested without plane subtraction. " \
            "Plane subtraction was added automatically to " \
            "ensure correct results.", UserWarning
        )

    try:
        data_shift_corr = data_shift_dict[data_shift_setting]()
    except KeyError:
        raise TypeError(
            "Invalid value for 'data_shift'. " \
            "Use 'minimum', 'mean' or 'no' (variable is not case-sensitive)."
        ) from None
    if data_shift_corr is not None:
        pipeline.append(data_shift_corr)

    return pipeline