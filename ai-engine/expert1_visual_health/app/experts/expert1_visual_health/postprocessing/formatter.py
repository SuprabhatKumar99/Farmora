def normalize_detection(class_id, class_name, confidence, bbox=None):
    result = {
        "class_id": int(class_id),
        "class_name": str(class_name),
        "confidence": float(confidence),
    }
    if bbox is not None:
        result["bbox"] = {
            "x1": float(bbox[0]), "y1": float(bbox[1]),
            "x2": float(bbox[2]), "y2": float(bbox[3]),
        }
    return result
