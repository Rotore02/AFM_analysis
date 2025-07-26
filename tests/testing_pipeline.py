from afm_analysis.image_correction import image_correction_pipeline
from afm_analysis.data_analysis import data_analysis_pipeline
from .testing_image_correction import noisy_plane
from functools import partial

def get_func_name(
    func_list : list
    ) -> list:
    """
    Returns a list of strings with the path of the functions inside.

    This function generates a list with the path of the functions inside `func_list` converted to strings.
    It internally checks wether the function is a partial function or not.

    Parameters
    ----------
    func_list : list
        list containing the callable functions

    Returns
    --------
    list
        list containing the function names converted in strings
    """
    function_name_list = []
    for func in func_list:
        if isinstance(func, partial):
            function_name_list.append(func.func.__module__ + "." + func.func.__name__)
        else:
            function_name_list.append(func.__module__ + "." + func.__name__)
    return function_name_list

settings = {
    "image_correction": {
        "common_plane_subtraction": "yes",
        "line_drift_correction": "mean",
        "data_shift": "no"
    },

    "data_analysis": {
        "height_values_distribution": "no",
        "roughness": "1d"
    },
}

def test_pipeline_is_correct(tmp_path):
    """
    This function tests that the image correction pipeline and the data analysis pipeline contain the correct functions, 
    according to the selected keys inside the `settings` dictionary.

    Given the planar distributed height data generated using the `noisy_plane` function without noise and given the 
    `settings` dictionary, this test applies the `image_correction_pipeline.build_image_correction_pipeline` and 
    the `data_analysis_pipeline.build_data_analysis_pipeline` functions to generate the two pipelines.
    Than, it checks that the name and the path of the functions inside the generated pipeline corresponds to the expected ones.
    In order to convert the pipelines of callable functions into lists of names, this test relies on the `get_func_name`
    function.
    """
    height_values = noisy_plane()

    im_corr_pipeline = image_correction_pipeline.build_image_correction_pipeline(settings,tmp_path)
    im_corr_names_pipeline = get_func_name(im_corr_pipeline)
    expected_im_corr_pipeline = [
        "afm_analysis.image_correction.image_correction_functions.common_plane_subtraction",
        "afm_analysis.image_correction.image_correction_functions.mean_drift_subtraction"
    ]

    assert im_corr_names_pipeline == expected_im_corr_pipeline

    data_an_pipeline = data_analysis_pipeline.build_data_analysis_pipeline(settings, tmp_path, height_values)
    data_an_names_pipeline = get_func_name(data_an_pipeline)
    expected_data_an_pipeline = [
        "afm_analysis.data_analysis.data_analysis_functions.roughness_1d"
    ]
    assert data_an_names_pipeline == expected_data_an_pipeline

shifted_settings = {
        "image_correction": {
            "data_shift": "no",
            "line_drift_correction": "mean",
            "common_plane_subtraction": "yes",
        },

        "data_analysis": {
            "roughness": "1d",
            "height_values_distribution": "no"
        }
    }

def test_settings_order_invariance(tmp_path):
    """
    This function tests that the image correction and data analysis pipelines remain invariant to the order 
    of keys in the `settings` dictionary.

    This test relies on the `settings` and `shifted_settings` dictionaries, where the latter has the same keys but 
    in a different oreder than the former. Given the planar distributed height data generated using the `noisy_plane` 
    function without noise and given both the `settings` and `shifted_settings` dictionaries, this test applies the 
    `image_correction_pipeline.build_image_correction_pipeline` and the `data_analysis_pipeline.build_data_analysis_pipeline`
    functions to generate the pipelines. Than, it checks that the names and paths of the functions inside the pipelines 
    generated from the `shifted_settings` and from the `settings` dictionaries correspond. In order to convert the pipelines of callable functions into lists of names, this test relies on the `get_func_name`
    function.
    """
    im_corr_pipeline = image_correction_pipeline.build_image_correction_pipeline(settings,tmp_path)
    im_corr_names_pipeline = get_func_name(im_corr_pipeline)

    im_corr_shifted_pipeline = image_correction_pipeline.build_image_correction_pipeline(shifted_settings,tmp_path)
    im_corr_shifted_names_pipeline = get_func_name(im_corr_shifted_pipeline)

    assert im_corr_shifted_names_pipeline == im_corr_names_pipeline

    data_an_pipeline = data_analysis_pipeline.build_data_analysis_pipeline(settings,tmp_path, noisy_plane())
    data_an_names_pipeline = get_func_name(data_an_pipeline)

    data_an_shifted_pipeline = data_analysis_pipeline.build_data_analysis_pipeline(shifted_settings,tmp_path, noisy_plane())
    data_an_shifted_names_pipeline = get_func_name(data_an_shifted_pipeline)

    assert data_an_shifted_names_pipeline == data_an_names_pipeline
