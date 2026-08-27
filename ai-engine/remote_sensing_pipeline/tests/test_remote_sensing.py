from pathlib import Path
import numpy as np

from app.remote_sensing.processing.indices import ndmi, ndvi, ndwi


def test_ndvi():
    nir = np.array([[0.8, 0.6]])
    red = np.array([[0.2, 0.4]])

    result = ndvi(nir, red)

    assert np.allclose(result, [[0.6, 0.2]], equal_nan=False)


def test_ndwi():
    nir = np.array([[0.8, 0.6]])
    green = np.array([[0.4, 0.3]])

    result = ndwi(nir, green)

    assert np.allclose(
        result,
        [[-0.33333334, -0.33333334]],
        atol=1e-6,
    )


def test_ndmi():
    nir = np.array([[0.8, 0.6]])
    swir = np.array([[0.2, 0.4]])

    result = ndmi(nir, swir)

    assert np.allclose(result, [[0.6, 0.2]], equal_nan=False)


def test_zero_denominator_is_masked():
    nir = np.array([[0.0]])
    red = np.array([[0.0]])

    result = ndvi(nir, red)

    assert result.mask[0, 0]
