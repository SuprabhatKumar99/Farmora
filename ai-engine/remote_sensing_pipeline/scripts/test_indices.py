import numpy as np

from app.remote_sensing.processing.indices import ndmi, ndvi, ndwi

nir = np.array([[0.8, 0.6]], dtype=np.float32)
red = np.array([[0.2, 0.4]], dtype=np.float32)
green = np.array([[0.4, 0.3]], dtype=np.float32)
swir = np.array([[0.2, 0.4]], dtype=np.float32)

print("NDVI:", ndvi(nir, red))
print("NDWI:", ndwi(nir, green))
print("NDMI:", ndmi(nir, swir))
