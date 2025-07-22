import warnings
from . import image_correction_functions
from functools import partial

def build_image_correction_pipeline(settings, results_file):
    pipeline = []

    # Plane subtraction
    plane_sub_dict = {
        "yes": partial(image_correction_functions.common_plane_subtraction, results_file=results_file),
        "no": None
    }

    # Drift correction
    drift_correction_dict = {
        "linear": lambda plane_subtraction: [
            partial(image_correction_functions.common_plane_subtraction, results_file=results_file) # If plane_subtraction is not performed while line drift is,
        ] * (plane_subtraction == "no") + [                                                         # than plane subtraction is also added to pipeline[]
            partial(image_correction_functions.linear_drift_subtraction, results_file=results_file)
        ],
        "mean": lambda plane_subtraction: [
            partial(image_correction_functions.common_plane_subtraction, results_file=results_file)
        ] * (plane_subtraction == "no") + [
            partial(image_correction_functions.mean_drift_subtraction, results_file=results_file)
        ],
        "no": lambda plane_subtraction: []
    }

    # Data shift
    data_shift_dict = {
        "minimum": image_correction_functions.shift_min,
        "mean": image_correction_functions.shift_mean,
        "no": None
    }

    # Parse settings
    plane_sub = settings["image_correction"]["common_plane_subtraction"].lower()
    drift_corr = settings["image_correction"]["line_drift_correction"].lower()
    data_shift = settings["image_correction"]["data_shift"].lower()

    # Apply plane subtraction if specified
    if plane_sub not in plane_sub_dict:
        raise TypeError("Invalid value for 'common_plane_subtraction'. " \
        "Use 'yes' or 'no' (variable is not case-sensitive).")
    if plane_sub_dict[plane_sub]:
        pipeline.append(plane_sub_dict[plane_sub])

    # Apply drift correction
    if drift_corr not in drift_correction_dict:
        raise TypeError("Invalid value for 'line_drift_correction'. " \
        "Use 'linear', 'mean' or 'no' (variable is not case-sensitive).")
    drift_steplane_subtraction = drift_correction_dict[drift_corr](plane_sub)
    if drift_corr != "no" and plane_sub == "no":
        warnings.warn("Drift correction requested without plane subtraction. " \
        "Plane subtraction was added automatically to ensure correct results.", UserWarning)
    pipeline.extend(drift_steplane_subtraction)

    # Apply data shift
    if data_shift not in data_shift_dict:
        raise TypeError("Invalid value for 'data_shift'. " \
        "Use 'minimum', 'mean' or 'no' (variable is not case-sensitive).")
    if data_shift_dict[data_shift]:
        pipeline.append(data_shift_dict[data_shift])

    return pipeline