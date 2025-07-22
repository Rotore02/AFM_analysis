import warnings
import image_correction
from functools import partial

def build_image_correction_pipeline(settings, results_file):
    pipeline = []

    # Mapping for plane subtraction
    plane_sub_options = {
        "yes": partial(image_correction.common_plane_subtraction, results_file=results_file),
        "no": None
    }

    # Drift correction strategies (require logic due to dependency)
    drift_correction_map = {
        "linear": lambda ps: [
            partial(image_correction.common_plane_subtraction, results_file=results_file)
        ] * (ps == "no") + [
            partial(image_correction.linear_drift_subtraction, results_file=results_file)
        ],
        "mean": lambda ps: [
            partial(image_correction.common_plane_subtraction, results_file=results_file)
        ] * (ps == "no") + [
            partial(image_correction.mean_drift_subtraction, results_file=results_file)
        ],
        "no": lambda ps: []
    }

    # Data shift
    data_shift_map = {
        "minimum": image_correction.shift_min,
        "mean": image_correction.shift_mean,
        "no": None
    }

    # Parse settings
    plane_sub = settings["image_correction"]["common_plane_subtraction"].lower()
    drift_corr = settings["image_correction"]["line_drift_correction"].lower()
    data_shift = settings["image_correction"]["data_shift"].lower()

    # Apply plane subtraction if specified
    if plane_sub not in plane_sub_options:
        raise TypeError("Invalid value for 'common_plane_subtraction'. Use 'yes' or 'no'.")
    if plane_sub_options[plane_sub]:
        pipeline.append(plane_sub_options[plane_sub])

    # Apply drift correction
    if drift_corr not in drift_correction_map:
        raise TypeError("Invalid value for 'line_drift_correction'. Use 'linear', 'mean' or 'no'.")
    drift_steps = drift_correction_map[drift_corr](plane_sub)
    if drift_corr != "no" and plane_sub == "no":
        warnings.warn("Drift correction requested without plane subtraction. Plane subtraction was added automatically.", UserWarning)
    pipeline.extend(drift_steps)

    # Apply data shift
    if data_shift not in data_shift_map:
        raise TypeError("Invalid value for 'data_shift'. Use 'minimum', 'mean' or 'no'.")
    if data_shift_map[data_shift]:
        pipeline.append(data_shift_map[data_shift])

    return pipeline