import data_analysis
import smart_file as sm
import numpy as np

def noisy_plane(
        noise : bool = False
        ) -> np.ndarray:
    """
    Creates planar-distributed heights with or without noise.

    Generates a plane of equation: z = a * x + b * y + c, 
    where a = 0.5, b = 0.3, and c = 5. The result is a 2D NumPy array 
    representing height values over a 10x10 grid. If `noise` is True, 
    uniform random noise in the range [-0.01, 0.01] is added to the plane.

    Parameters
    ----------
    noise : bool
        Whether to add uniform random noise to the generated plane.

    Returns
    -------
    ndarray
        A 2D NumPy array of shape (10, 10) containing the computed z-values.

    See Also
    --------
    numpy.random.uniform : Function to generate uniform random numbers.
    numpy.random.seed : Function that sets the seed for random number generation.
    numpy.meshgrid : Generates coordinate matrices from coordinate vectors.

    Notes
    ------
    The function performs numpy.random.seed(0) in order to make the test deterministic.
    In this way, each time the function runs with the option `noise` = True, the same random numbers are 
    generated for each z value of the plane.
    """
    x = np.arange(10)
    y = np.arange(10)
    X, Y = np.meshgrid(x, y)
    if noise:
        np.random.seed(0)
        Z = 2.5 * X + 3.2 * Y + 5 + np.random.uniform(-0.01,0.01, size=X.shape)
    else:
        Z = 2.5 * X + 3.2 * Y + 5
    return Z

def test_plane_subtraction():
    """
    This function tests that the planar slope of the height data is correctly subtracted between a certain tolerance.

    Given the planar distributed height data generated using the `noisy_plane` function with and without noise,
    this test applies the `data_analysis.common_plane_subtraction` function to subtract this planar slope.
    The result should be a 2-d array of heights which are approximately zero within a certain tolerance.
    This tolerance is set to 1e-10 for the data without noise and to 0.1 for the data with noise.
    """
    results_file = sm.SmartFile()
    corrected_heights = data_analysis.common_plane_subtraction(noisy_plane(noise=False), results_file)
    assert np.allclose(corrected_heights, 0, atol=1e-10)

    corrected_noisy_heights = data_analysis.common_plane_subtraction(noisy_plane(noise=True), results_file)
    assert np.allclose(corrected_noisy_heights, 0, atol=0.1)  

def test_common_plane_subtraction_writes(tmp_path):
    """
    This function tests that the function `data_analysis.common_plane_subtraction` correctly writes on a `sm.SmartFile` object.

    Given the planar distributed height data generated using the `noisy_plane` function without noise, this test creates a temporary
    `sm.SmartFile` object using the `tmp_path` temporary directory provided by pytest. 
    Additionally, it applies the `data_analysis.common_plane_subtraction` function to the height values and checks that it correcly
    writes the expected output to the file.
    """
    file_path = tmp_path / "common_plane_subtraction_test_file.txt"
    results_file = sm.SmartFile()
    results_file.setup(str(file_path))

    data_analysis.common_plane_subtraction(noisy_plane(False), results_file)
    results_file.close()

    text = file_path.read_text()
    assert "COMMON PLANE SUBTRACTION" in text
    assert "plane equation:" in text
    assert "a =" in text and "b =" in text and "c =" in text

def test_line_drift_subtraction():
    """
    This function tests that the linear slope along the fast scan direction is correctly subtracted from the height data between a certain tolerance.

    Given the planar distributed height data generated using the `noisy_plane` function with and without noise,
    this test applies the `data_analysis.line_drift_subtraction` function to subtract the linear slope along the x direction (fast scan direction).
    The result should be a 2-d array of heights in which each line along the x axis is approximately zero within a certain tolerance.
    This tolerance is set to 1e-10 for the data without noise and to 0.1 for the data with noise.
    """
    results_file = sm.SmartFile()
    corrected_heights = data_analysis.line_drift_subtraction(noisy_plane(),results_file)
    assert np.allclose(corrected_heights[0], 0, atol=1e-10)
    assert np.allclose(corrected_heights[1], 0, atol=1e-10)

    corrected_noisy_heights = data_analysis.line_drift_subtraction(noisy_plane(True),results_file)
    assert np.allclose(corrected_noisy_heights[0], 0, atol=0.1)
    assert np.allclose(corrected_noisy_heights[1], 0, atol=0.1)

def test_line_drift_subtraction_writes(tmp_path):
    """
    This function tests that the function `data_analysis.line_drift_subtraction` correctly writes on a `sm.SmartFile` object.

    Given the planar distributed height data generated using the `noisy_plane` function without noise, this test creates a temporary
    `sm.SmartFile` object using the `tmp_path` temporary directory provided by pytest. 
    Additionally, it applies the `data_analysis.line_drift_subtraction` function to the height values and checks that it correcly
    writes the expected output to the file.
    """
    file_path = tmp_path / "line_drift_subtraction_test_file.txt"
    results_file = sm.SmartFile()
    results_file.setup(str(file_path))

    data_analysis.line_drift_subtraction(noisy_plane(False), results_file)
    results_file.close()

    text = file_path.read_text()
    assert "LINE DRIFT SUBTRACTION" in text
    assert "line equation:" in text
    assert "average m value =" in text and "m values standard deviation =" in text
    assert "average q value =" in text and "q values standard deviation =" in text

def test_mean_drift_subtraction():
    """
    This function tests that the mean of each fast scan direction line is correctly subtracted from the height data between a certain tolerance.

    Given the planar distributed height data generated using the `noisy_plane` function with and without noise,
    this test applies the `data_analysis.mean_drift_subtraction` function to subtract the mean of each line along the x direction (fast scan direction).
    The result should be a 2-d array of heights in which each line along the x axis has the mean that is approximately zero within a certain tolerance.
    This tolerance is set to 1e-10 for the data without noise and to 0.01 for the data with noise.
    """
    results_file = sm.SmartFile()
    corrected_heights = data_analysis.mean_drift_subtraction(noisy_plane(),results_file)
    assert np.allclose(np.mean(corrected_heights), 0, atol=1e-10)
    assert np.allclose(np.mean(corrected_heights[1]), 0, atol=1e-10)

    corrected_noisy_heights = data_analysis.mean_drift_subtraction(noisy_plane(True),results_file)
    assert np.allclose(np.mean(corrected_noisy_heights[0]), 0, atol=0.01)
    assert np.allclose(np.mean(corrected_noisy_heights[1]), 0, atol=0.01)

def test_mean_drift_subtraction_writes(tmp_path):
    """
    This function tests that the function `data_analysis.mean_drift_subtraction` correctly writes on a `sm.SmartFile` object.

    Given the planar distributed height data generated using the `noisy_plane` function without noise, this test creates a temporary
    `sm.SmartFile` object using the `tmp_path` temporary directory provided by pytest. 
    Additionally, it applies the `data_analysis.mean_drift_subtraction` function to the height values and checks that it correcly
    writes the expected output to the file.
    """
    file_path = tmp_path / "mean_drift_subtraction_test_file.txt"
    results_file = sm.SmartFile()
    results_file.setup(str(file_path))

    data_analysis.mean_drift_subtraction(noisy_plane(False), results_file)
    results_file.close()

    text = file_path.read_text()
    assert "MEAN DRIFT SUBTRACTION" in text
    assert "average mean value =" in text
    assert "standard deviation =" in text

def test_data_shift():
    """
    This function tests that the height values are shifted correctly.

    Given the planar distributed height data generated using the `noisy_plane` function without noise, this test subtracts the mean height value
    using the `data_analysis.shift_mean` function and the minimum heght value using the `data_analysis.shift_min` function. Furthermore, it checks 
    that the mean height value and the minimum height of the shifted arrays are correctly set to zero under a certain tolerance, respectively.
    This tolerance is set to 1e-10.
    """
    mean_shifted_heights = data_analysis.shift_mean(noisy_plane())
    assert np.isclose(np.mean(mean_shifted_heights), 0, atol=1e-10)

    min_shifted_heights = data_analysis.shift_min(noisy_plane())
    assert np.isclose(min_shifted_heights.min(), 0, atol=1e-10)


