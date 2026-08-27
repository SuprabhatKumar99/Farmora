# STEP 4 — Observation / Image / Video Pipeline

This package implements **only Step 4** of the AI Engine roadmap.

The project structure from Steps 1–3 is preserved. Step 4 adds the observation pipeline without renaming or replacing the existing knowledge/farm components.

## Dataset structure — unchanged

```text
crop_health_dataset/
├── 01_crop_knowledge/
├── 02_disease_pest_knowledge/
├── 03_farm/
└── 04_observations/
    ├── observations.csv
    └── media_metadata.csv
```

The exact Step 4 structure is preserved as:

```text
04_observations/
├── observations.csv
└── media_metadata.csv
```

If your actual Step 4 dataset contains additional files, keep them in the same directory; this implementation does not require renaming them.

## Why the application layer is separate from the dataset

The dataset stores observation records/metadata.

The application pipeline handles:

```text
Upload
  ↓
Temporary file
  ↓
Media validation
  ↓
Image/video decoding
  ↓
Metadata extraction
  ↓
Local object storage adapter
  ↓
Observation object
  ↓
Later AI inference
```

## Supported media

Images:
- JPG/JPEG
- PNG
- BMP
- WEBP
- TIFF

Videos:
- MP4
- AVI
- MOV
- MKV
- WEBM
- M4V

## Image validation

The image path is:

```text
Image upload
    ↓
Extension/content-type check
    ↓
File-size check
    ↓
OpenCV decode
    ↓
Width/height extraction
    ↓
Validated observation
```

No AI prediction occurs in Step 4.

## Video validation

The video path is:

```text
Video upload
    ↓
Extension/content-type check
    ↓
File-size check
    ↓
OpenCV VideoCapture
    ↓
FPS / frame count / resolution
    ↓
Readability check
    ↓
Validated observation
```

## Video frame extraction

For later Expert 1 video inference:

```text
Video
  ↓
OpenCV VideoCapture
  ↓
Controlled frame interval
  ↓
JPEG frames
  ↓
Expert inference
```

The extractor deliberately supports frame skipping. It does not assume every frame must be processed.

Example:

```bash
python scripts/extract_video_frames.py sample.mp4 1.0
```

This targets approximately one frame per second.

## API

Run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health:

```text
GET /health
GET /ready
```

Create observation:

```text
POST /api/v1/observations
multipart/form-data
```

Form fields:

```text
file
farm_id
zone_id
crop_id
variety_id
```

Example with curl:

```bash
curl -X POST http://localhost:8000/api/v1/observations   -F "file=@sample.jpg"   -F "farm_id=F001"   -F "zone_id=Z001"   -F "crop_id=C001"   -F "variety_id=V001"
```

Get observation:

```text
GET /api/v1/observations/{observation_id}
```

## Test without a real image

Create a sample image with Python/OpenCV or use one of your real images.

Then:

```bash
python scripts/test_image.py path/to/image.jpg
```

## Automated tests

```bash
pytest -q
```

## Storage boundary

Development uses:

```text
app/observation/storage/local.py
```

The storage interface is deliberately isolated so that the production implementation can later use:

```text
MinIO / S3
```

without changing the observation service.

Large image/video binaries should not be placed directly into Kafka messages. Later asynchronous inference messages should contain an object-storage reference plus observation metadata.

## Step 4 output

The observation service produces a normalized observation:

```text
observation_id
observation_type
status
original_filename
media_path
content_type
size_bytes
metadata
created_at
```

For video validation, media metadata can additionally include:

```text
width
height
frame_count
fps
duration_seconds
```

## Error handling

Current media errors include:

```text
MEDIA_NOT_FOUND
UNSUPPORTED_MEDIA_TYPE
MEDIA_TOO_LARGE
IMAGE_DECODE_FAILED
VIDEO_DECODE_FAILED
VIDEO_FRAME_READ_FAILED
```

Raw Python exceptions are not exposed as the API response.

## Important boundary

Step 4 does NOT implement:

- YOLO inference
- Expert 1
- disease classification
- severity prediction
- tracking
- farm risk scoring
- Kafka
- PostgreSQL
- Expert 8

Those belong to later steps.

The output of this step is the validated observation/media object that later expert pipelines consume.

## Important dataset rule

The six/four files from previous roadmap steps are not modified by this package.

Only the Step 4 directory is introduced:

```text
04_observations/
├── observations.csv
└── media_metadata.csv
```

The example CSV rows are placeholders for executable testing only. Replace them with the actual verified dataset records.
