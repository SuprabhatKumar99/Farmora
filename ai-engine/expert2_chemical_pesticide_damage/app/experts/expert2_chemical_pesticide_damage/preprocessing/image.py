from pathlib import Path
import cv2
class ImagePreprocessor:
    SUPPORTED={".jpg",".jpeg",".png",".bmp",".webp",".tif",".tiff"}
    def load(self,path):
        p=Path(path)
        if not p.exists(): raise FileNotFoundError(str(p))
        if p.suffix.lower() not in self.SUPPORTED: raise ValueError("Unsupported image extension.")
        x=cv2.imread(str(p))
        if x is None: raise ValueError("IMAGE_DECODE_FAILED")
        if x.size==0: raise ValueError("EMPTY_IMAGE")
        return x
    def quality(self,image):
        h,w=image.shape[:2]
        return "LOW" if min(h,w)<64 else "ACCEPTABLE"
