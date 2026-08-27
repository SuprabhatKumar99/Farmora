import numpy as np


def _safe_divide(numerator, denominator):
    numerator = np.asarray(numerator, dtype=np.float32)
    denominator = np.asarray(denominator, dtype=np.float32)

    with np.errstate(divide="ignore", invalid="ignore"):
        result = np.divide(numerator, denominator)

    return np.ma.masked_invalid(result)


def normalized_difference(numerator_band, denominator_band):
    """Compute (A - B) / (A + B), masking invalid divisions."""
    return _safe_divide(
        np.asarray(numerator_band) - np.asarray(denominator_band),
        np.asarray(numerator_band) + np.asarray(denominator_band),
    )


def ndvi(nir, red):
    """Normalized Difference Vegetation Index: (NIR - Red)/(NIR + Red)."""
    return normalized_difference(nir, red)


def ndwi(nir, green):
    """Normalized Difference Water Index variant using NIR and Green."""
    return normalized_difference(green, nir)


def ndmi(nir, swir):
    """Normalized Difference Moisture Index: (NIR - SWIR)/(NIR + SWIR)."""
    return normalized_difference(nir, swir)


def summarize_array(index_name, array):
    masked = np.ma.asarray(array)
    valid = ~np.ma.getmaskarray(masked)
    values = np.asarray(masked)[valid]

    if values.size == 0:
        return {
            "index_name": index_name,
            "value": None,
            "valid_pixels": 0,
            "total_pixels": int(masked.size),
        }

    return {
        "index_name": index_name,
        "value": float(np.mean(values)),
        "valid_pixels": int(values.size),
        "total_pixels": int(masked.size),
    }
