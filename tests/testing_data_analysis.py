from AFM_analisys.data_analysis import data_analysis_functions
from AFM_analisys.image_correction import image_correction_functions
import numpy as np
from AFM_analisys.tests.testing_image_correction import noisy_plane
from AFM_analisys import smart_file as sm

def test_height_distribution_axis():
    """
    This function tests that the x axis (height values axis) of the height distribution is generated as expected.

    Given a simple 2-d array composed of 2 rows and 2 columns, this test generates the x (height values) and 
    y (number of occurrences) axis of the heights distribution using the `data_analysis.data_analysis_functions.height_distribution`
    function. First of all, it checks that the extremes of the x axis correspond to the minimum height plus half the bin width
    and to the maximum height minus the bin width, respectively. Furthermore, it checks that all the 100 points in the 
    x axis correspond to the expected centers of each bin. 
    """
    height_values = np.array([[-1.3, 0.5], [0.2, 4.5]])
    bin_width = (height_values.max() - height_values.min())/100
    histo = data_analysis_functions.height_distribution(height_values)
    assert np.allclose(histo[0].min(), height_values.min() + bin_width/2)
    assert np.allclose(histo[0].max(), height_values.max() - bin_width/2)

    n_bins = 100
    bin_edges = np.linspace(height_values.min(), height_values.max(), n_bins + 1)
    expected_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    assert np.allclose(histo[0], expected_centers)

def test_height_distribution_count():
    """
    This function tests that the y axis (number of occurrences) of the height distribution is generated as expected.

    Given a simple 2-d array composed of 2 rows and 2 columns, this test generates the x (height values) and 
    y (number of occurrences) axis of the heights distribution using the `data_analysis.data_analysis_funcions.height_distribution` 
    function. Then, it checks that each height value `z` is correctly placed in the bin defined as [n⋅bin_width, (n+1)⋅bin_width), 
    (including the left edge and excluding the right edge) if n⋅bin_width <= `z` < (n+1)⋅bin_width, with n integer that 
    goes from 0 to 99. The maximum height is placed in the 99-th bin. In the test, particular attention is paid to the 
    extremes and to the values at the bin edges.
    """
    height_values = np.array([[0, 0.353], [0.5, 1]])
    histo = data_analysis_functions.height_distribution(height_values)
    print(histo[0])
    assert histo[1][0] == 1
    assert histo[1][35] == 1
    assert histo[1][50] == 1 #correctly check that 0.5, which is between bin 50 and bin 51, is put in bin 50 and not in bin 51.
    assert histo[1][51] == 0
    assert histo[1][99] == 1

def test_height_distribution_shape():
    """
    This function tests that the shape of the x and y axis of the height distribution histogram is consistent with the data.

    Given the planar distributed height data generated using the `noisy_plane` function without noise, 
    this test generates the x (height values) and y (number of occurrences) axis of the heights distribution using the 
    `data_analysis.data_analysis_functions.height_distribution` function. After that, it checks that the x axis is exactly 
    composed of 100 values (bin centers) and that the sum of all the y axis values is equal to the amount of height data 
    stored in the `height_values` 2-d array. This is to make sure that none of the height values is 
    left apart in the distribution.
    """
    height_values = noisy_plane()
    histo = data_analysis_functions.height_distribution(height_values)
    assert histo[0].size == 100
    assert np.sum(histo[1]) == height_values.size

def test_1d_roughness(tmp_path):
    """
    This function tests that the 1-d roughness is computed correctly.

    Given a simple 2-d array of 2 rows and 2 columns, this function creates a temporary `sm.SmartFile` object using the
    `tmp_path` temporary directory provided by pytest and executes the `data_analysis.data_analysis_functions.roughness_1d` 
    function to write the roughness and its standard deviation to the file. Afterward, the test checks that the expected 
    values of roughness and standard deviation have been written in the file.
    """
    file_path = tmp_path / "1d_roughness_test_file.txt"
    results_file = sm.SmartFile()
    results_file.setup(str(file_path))

    height_values = np.array([[1,4],[-3,-1]])
    data_analysis_functions.roughness_1d(height_values, results_file)

    results_file.close()

    text = file_path.read_text()
    for line in text.splitlines():
        if line.startswith("roughness ="):
            roughness = float(line.split('=')[1].strip().split()[0])
            assert np.isclose(roughness, 1.25)
        if line.startswith("standard deviation ="):
            standard_deviation = float(line.split('=')[1].strip().split()[0])
            assert np.isclose(standard_deviation, 0.25)

def test_2d_roughness(tmp_path):
    """
    This function tests that the 2-d roughness is computed correctly.

    Given a simple 2-d array of 2 rows and 2 columns, this function creates a temporary `sm.SmartFile` object using the
    `tmp_path` temporary directory provided by pytest and executes the `data_analysis.data_analysis_functions.roughness_2d`
    function to write the roughness. Afterward, the test checks that the expected roughness value has been written correctly
    in the file. Note that, differently from the `data_analysis.roughness_1d`, the `data_analysis.roughness_2d` function does not 
    provide a value for the standard deviation. 
    """
    file_path = tmp_path / "2d_roughness_test_file.txt"
    results_file = sm.SmartFile()
    results_file.setup(str(file_path))

    height_values = np.array([[2,4],[0,2]])
    data_analysis_functions.roughness_2d(height_values, results_file)

    results_file.close()

    text = file_path.read_text()
    for line in text.splitlines():
        if line.startswith("roughness ="):
            roughness = float(line.split('=')[1].strip().split()[0])
            assert np.isclose(roughness, 1.4142)

def test_roughness_is_shifting_indep(tmp_path):
    """
    This function checks that the roughness value and its standard deviation is independent from any height shift.

    Given the planar distributed height data generated using the `tests.testing_image_correction.noisy_plane` function 
    without noise, this test creates a temporary `sm.SmartFile` object using the `tmp_path` temporary directory provided 
    by pytest and executes both the `image_correction.image_correction_functions.shift_mean` function and the 
    `image_correction.image_correction_functions.shift_min` function to shift the height values. Afterward, both the 
    `data_analysis.data_analysis_functions.roughness_1d` and the `data_analysis.data_analysis.funcions.roughness_2d` 
    functions are applied to the unshifted data and to the shifted data, in order to write on the temporary file all the values 
    of roughness and standard deviation (this latter only for the 1-d case). Finally, this function checks from the file that the 
    roughness of the shifted heights equals the roughness of the unshifted heights, for both the 1-d and the 2-d calculations. 
    For the 1-d case, also the invariance of the standard deviation is tested. The independency of the roughness from the 
    height shifting allows performing the roughness analysis after shifting the data in the `AFM_image_analyser.py` module.
    """
    file_path = tmp_path / "roughness_is_shifting_indep_test_file.txt"
    results_file = sm.SmartFile()
    results_file.setup(str(file_path))

    height_values = noisy_plane()
    mean_shifted_heights = image_correction_functions.shift_mean(height_values)
    min_shifted_heights = image_correction_functions.shift_min(height_values)

    data_analysis_functions.roughness_1d(height_values, results_file)
    data_analysis_functions.roughness_1d(mean_shifted_heights, results_file)
    data_analysis_functions.roughness_1d(min_shifted_heights, results_file)

    data_analysis_functions.roughness_2d(height_values, results_file)
    data_analysis_functions.roughness_2d(mean_shifted_heights, results_file)
    data_analysis_functions.roughness_2d(mean_shifted_heights, results_file)

    results_file.close()

    text = file_path.read_text()
    roughness_values = []
    for line in text.splitlines():
        if line.startswith("roughness ="):
            roughness = float(line.split('=')[1].strip().split()[0])
            roughness_values.append(roughness)

    print(roughness_values)
            
    assert np.isclose(roughness_values[1], roughness_values[0])
    assert np.isclose(roughness_values[2], roughness_values[0])
    
    assert np.isclose(roughness_values[4], roughness_values[3])
    assert np.isclose(roughness_values[5], roughness_values[3])