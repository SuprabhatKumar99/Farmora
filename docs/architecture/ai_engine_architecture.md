# AI Engine Architecture

the AI engine is a **separate Python-based inference platform** responsible only for computer vision, model inference, video/image processing, post-processing, and AI-specific analytics.

The clean separation is:

**React → Spring Boot → Kafka/AI Gateway → AI Engine → Kafka → Spring Boot → React**

The AI engine should **not directly access PostgreSQL or the frontend**.

---

# 1. AI Engine Technology Stack

| Layer               | Technology                 |
| ------------------- | -------------------------- |
| Language            | **Python 3.11+**           |
| API                 | **FastAPI**                |
| ASGI Server         | Uvicorn                    |
| Deep Learning       | **PyTorch**                |
| Object Detection    | **YOLO / Ultralytics**     |
| Computer Vision     | **OpenCV**                 |
| Numerical Computing | **NumPy**                  |
| Data Processing     | **Pandas**                 |
| Image Processing    | Pillow                     |
| Augmentation        | Albumentations             |
| ML Utilities        | scikit-learn               |
| Model Tracking      | MLflow                     |
| Model Storage       | MinIO / S3                 |
| Messaging           | Apache Kafka               |
| Kafka Client        | aiokafka / confluent-kafka |
| Validation          | Pydantic                   |
| GPU                 | NVIDIA CUDA                |
| Optimization        | ONNX Runtime / TensorRT    |
| Testing             | PyTest                     |
| Logging             | Python logging / structlog |
| Metrics             | Prometheus client          |
| Tracing             | OpenTelemetry              |
| Containerization    | Docker                     |
| Orchestration       | Kubernetes                 |

---

# 2. High-Level AI Architecture

```text
                         SPRING BOOT
                              │
                     ┌────────┴────────┐
                     │                 │
                  REST API           Kafka
                     │                 │
                     │       ai.inference.request
                     │                 │
                     ▼                 ▼
              ┌─────────────────────────────┐
              │         AI ENGINE            │
              │                              │
              │ ┌──────────────────────────┐ │
              │ │       API / Worker       │ │
              │ └────────────┬─────────────┘ │
              │              │               │
              │ ┌────────────▼─────────────┐ │
              │ │      Preprocessing       │ │
              │ │ OpenCV • NumPy • Pillow │ │
              │ └────────────┬─────────────┘ │
              │              │               │
              │ ┌────────────▼─────────────┐ │
              │ │      Model Inference     │ │
              │ │ PyTorch • YOLO           │ │
              │ └────────────┬─────────────┘ │
              │              │               │
              │ ┌────────────▼─────────────┐ │
              │ │      Post Processing     │ │
              │ │ NMS • Filtering • Track │ │
              │ └────────────┬─────────────┘ │
              │              │               │
              │ ┌────────────▼─────────────┐ │
              │ │      Result Formatter    │ │
              │ └────────────┬─────────────┘ │
              └──────────────┼───────────────┘
                             │
                             ▼
                      Kafka / REST
                             │
                             ▼
                       SPRING BOOT
```

---

# 3. AI Engine Responsibilities

The AI engine should own:

```text
Image processing
Video processing
Frame extraction
Object detection
Object classification
Object tracking
Confidence filtering
Bounding-box processing
Model inference
Model versioning
AI result generation
AI performance metrics
```

The backend should own:

```text
Users
Authentication
Authorization
Business rules
Database
Reports
Notifications
Audit
API orchestration
```

This separation is extremely important.

---

# 4. AI Engine Architecture Layers

Use a layered architecture:

```text
┌─────────────────────────────────────────────┐
│             API / CONSUMER LAYER            │
│                                             │
│ FastAPI • Kafka Consumer • Health APIs      │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│            APPLICATION LAYER                │
│                                             │
│ Inference Service • Job Manager             │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│              PIPELINE LAYER                 │
│                                             │
│ Preprocess → Inference → Postprocess        │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│                MODEL LAYER                  │
│                                             │
│ YOLO • PyTorch • Model Registry             │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│          HARDWARE / RUNTIME LAYER           │
│                                             │
│ CPU • CUDA • GPU • TensorRT • ONNX          │
└─────────────────────────────────────────────┘
```

---

# 5. Recommended Folder Structure

```text
ai-engine/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── inference.py
│   │   │   ├── health.py
│   │   │   ├── models.py
│   │   │   └── jobs.py
│   │   │
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── security.py
│   │   └── exceptions.py
│   │
│   ├── schemas/
│   │   ├── inference.py
│   │   ├── detection.py
│   │   ├── model.py
│   │   └── job.py
│   │
│   ├── services/
│   │   ├── inference_service.py
│   │   ├── video_service.py
│   │   ├── image_service.py
│   │   └── job_service.py
│   │
│   ├── pipeline/
│   │   ├── pipeline.py
│   │   ├── preprocessing.py
│   │   ├── inference.py
│   │   └── postprocessing.py
│   │
│   ├── models/
│   │   ├── base.py
│   │   ├── yolo_detector.py
│   │   ├── model_loader.py
│   │   └── model_registry.py
│   │
│   ├── tracking/
│   │   ├── tracker.py
│   │   └── object_tracker.py
│   │
│   ├── preprocessing/
│   │   ├── image.py
│   │   ├── video.py
│   │   ├── resize.py
│   │   └── augmentation.py
│   │
│   ├── postprocessing/
│   │   ├── confidence.py
│   │   ├── nms.py
│   │   ├── filtering.py
│   │   └── formatter.py
│   │
│   ├── kafka/
│   │   ├── producer.py
│   │   ├── consumer.py
│   │   └── topics.py
│   │
│   ├── storage/
│   │   ├── object_storage.py
│   │   └── model_storage.py
│   │
│   ├── monitoring/
│   │   ├── metrics.py
│   │   └── tracing.py
│   │
│   └── utils/
│       ├── image_utils.py
│       ├── video_utils.py
│       └── performance.py
│
├── models/
│   ├── production/
│   ├── staging/
│   └── archived/
│
├── datasets/
│   ├── raw/
│   ├── processed/
│   └── validation/
│
├── training/
│   ├── train.py
│   ├── evaluate.py
│   └── export.py
│
├── notebooks/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── inference/
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 6. AI Inference Pipeline

The core pipeline should be:

```text
             INPUT
               │
               ▼
       ┌─────────────────┐
       │ Input Validator  │
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │  Preprocessing   │
       │                 │
       │ OpenCV          │
       │ NumPy           │
       │ Pillow          │
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │ Frame / Image    │
       │ Preparation      │
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │  YOLO Model      │
       │  PyTorch         │
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │ Raw Predictions  │
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │ Post Processing  │
       │                 │
       │ Confidence       │
       │ NMS              │
       │ Filtering        │
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │ Tracking         │
       │ Optional         │
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │ Result Formatter │
       └────────┬────────┘
                ▼
              JSON
```

---

# 7. Image Detection Flow

For a single image:

```text
Image
 │
 ▼
OpenCV
 │
 ▼
Resize
 │
 ▼
Normalize
 │
 ▼
NumPy Array
 │
 ▼
PyTorch Tensor
 │
 ▼
YOLO
 │
 ▼
Predictions
 │
 ▼
Confidence Filtering
 │
 ▼
NMS
 │
 ▼
Bounding Boxes
 │
 ▼
JSON Result
```

---

# 8. Video Detection Flow

For video processing:

```text
                VIDEO
                  │
                  ▼
           OpenCV VideoCapture
                  │
                  ▼
            Frame Extraction
                  │
        ┌─────────┴─────────┐
        │                   │
      Frame 1             Frame N
        │                   │
        ▼                   ▼
     Preprocess          Preprocess
        │                   │
        ▼                   ▼
       YOLO                YOLO
        │                   │
        ▼                   ▼
    Detection            Detection
        │                   │
        └─────────┬─────────┘
                  ▼
             Tracking
                  │
                  ▼
          Temporal Analysis
                  │
                  ▼
           Final Results
```

For real-time applications, process frames in batches or use controlled frame skipping when appropriate rather than attempting to infer every frame regardless of hardware capacity.

---

# 9. Model Architecture

Keep model loading separate from inference logic.

```text
                  Model Registry
                       │
                       ▼
                 Model Loader
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        YOLO Model           Other Model
             │                   │
             ▼                   ▼
          PyTorch             PyTorch
             │
             ▼
          GPU / CPU
```

Example:

```text
models/
│
├── yolo_detector.py
├── model_loader.py
└── model_registry.py
```

The inference service should not care whether the model is:

```text
YOLOv8
YOLO11
YOLO custom model
ONNX model
TensorRT engine
```

It should communicate through a common model interface.

---

# 10. Model Interface

Conceptually:

```text
Model
 │
 ├── load()
 ├── predict()
 ├── unload()
 ├── metadata()
 └── health()
```

This lets you replace models without rewriting the entire AI pipeline.

---

# 11. Model Versioning

Every inference result should contain the model version.

```text
Model Registry
     │
     ├── model-v1
     ├── model-v2
     ├── model-v3
     │
     └── production → model-v3
```

Example:

```text
model_name:
target-detector

version:
3.2.0

framework:
PyTorch

architecture:
YOLO

input_size:
640x640

classes:
[...]

status:
PRODUCTION
```

---

# 12. MLflow Architecture

For model experimentation:

```text
                 DATASET
                    │
                    ▼
                Training
                    │
                    ▼
                 PyTorch
                    │
                    ▼
               Evaluation
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       mAP       Precision   Recall
          │         │         │
          └─────────┼─────────┘
                    ▼
                  MLflow
                    │
                    ▼
              Model Registry
                    │
                    ▼
             Production Model
```

Track:

```text
Training parameters
Dataset version
Model version
mAP
Precision
Recall
F1
Training loss
Validation loss
Inference latency
```

---

# 13. Training Architecture

Training should be separated from the production inference service.

```text
                   DATASET
                      │
                      ▼
                Data Cleaning
                      │
                      ▼
                 Annotation
                      │
                      ▼
             Train / Validation
                      │
                      ▼
               Augmentation
                      │
                      ▼
              YOLO / PyTorch
                      │
                      ▼
                  Training
                      │
                      ▼
                 Evaluation
                      │
                      ▼
                MLflow
                      │
                      ▼
              Model Registry
                      │
                      ▼
             Production Model
                      │
                      ▼
               AI Inference
```

Don't train models inside your production API container.

---

# 14. Dataset Pipeline

```text
Raw Images
    │
    ▼
Data Cleaning
    │
    ▼
Duplicate Removal
    │
    ▼
Annotation
    │
    ▼
Quality Check
    │
    ▼
Train / Validation / Test
    │
    ▼
Augmentation
    │
    ▼
YOLO Dataset
```

Useful libraries:

* OpenCV
* NumPy
* Pandas
* Pillow
* Albumentations

---

# 15. Kafka Integration

The AI engine should support asynchronous inference.

```text
                    KAFKA
                      │
                      ▼
             ai.inference.request
                      │
                      ▼
               Kafka Consumer
                      │
                      ▼
              Inference Service
                      │
                      ▼
                AI Pipeline
                      │
                      ▼
              Result Formatter
                      │
                      ▼
             Kafka Producer
                      │
                      ▼
            ai.inference.completed
                      │
                      ▼
                Spring Boot
```

Failure:

```text
AI Pipeline
    │
    ▼
Exception
    │
    ▼
ai.inference.failed
    │
    ▼
Spring Boot
```

---

# 16. AI Job Lifecycle

```text
CREATED
   │
   ▼
QUEUED
   │
   ▼
PROCESSING
   │
   ├───────────────┐
   ▼               ▼
COMPLETED        FAILED
   │               │
   ▼               ▼
RESULT          RETRY / ERROR
```

Each job should have:

```text
jobId
requestId
modelVersion
inputType
createdAt
startedAt
completedAt
status
errorCode
processingTime
```

---

# 17. AI API

FastAPI can expose endpoints such as:

```text
POST /api/v1/inference
POST /api/v1/inference/image
POST /api/v1/inference/video

GET  /api/v1/jobs/{jobId}

GET  /api/v1/models
GET  /api/v1/models/{modelId}

GET  /health
GET  /ready
GET  /metrics
```

For example:

```text
POST /api/v1/inference/image
```

Input:

```text
image
modelVersion
confidenceThreshold
```

Output:

```json id="w7c9qj"
{
  "jobId": "job-123",
  "modelVersion": "3.2.0",
  "processingTimeMs": 142,
  "detections": [
    {
      "classId": 1,
      "className": "target",
      "confidence": 0.96,
      "bbox": {
        "x": 120,
        "y": 85,
        "width": 240,
        "height": 310
      }
    }
  ]
}
```

---

# 18. Preprocessing Layer

The preprocessing module should handle:

```text
Image validation
Image decoding
Resize
Normalization
Color conversion
Frame extraction
Noise handling
Optional augmentation
```

Architecture:

```text
Input
 │
 ▼
Validator
 │
 ▼
Decoder
 │
 ▼
Resize
 │
 ▼
Normalize
 │
 ▼
Model Input
```

Use:

```text
OpenCV
NumPy
Pillow
Albumentations
```

---

# 19. Postprocessing Layer

Raw YOLO output shouldn't immediately go to the backend.

```text
YOLO Output
    │
    ▼
Confidence Filtering
    │
    ▼
Non-Maximum Suppression
    │
    ▼
Class Filtering
    │
    ▼
Coordinate Conversion
    │
    ▼
Tracking
    │
    ▼
Business-neutral AI Result
```

Output should contain only AI-related information.

---

# 20. Object Tracking

For video/live camera scenarios:

```text
Frame 1
  │
  ▼
YOLO Detection
  │
  ▼
Tracker
  │
  ▼
Object ID = 17

Frame 2
  │
  ▼
YOLO Detection
  │
  ▼
Tracker
  │
  ▼
Object ID = 17
```

This lets the system distinguish between:

```text
New object
Existing object
Object disappeared
Object reappeared
```

You can introduce a suitable tracker depending on the project's requirements, such as ByteTrack or another compatible tracking implementation.

---

# 21. AI Engine Communication With Backend

There should be two paths.

### Synchronous

For quick image inference:

```text
Spring Boot
     │
     │ HTTP
     ▼
FastAPI
     │
     ▼
YOLO
     │
     ▼
JSON
     │
     ▼
Spring Boot
```

### Asynchronous

For videos and heavy workloads:

```text
Spring Boot
     │
     ▼
Kafka
     │
     ▼
AI Worker
     │
     ▼
YOLO
     │
     ▼
Kafka
     │
     ▼
Spring Boot
```

---

# 22. GPU Architecture

For production inference:

```text
              AI ENGINE POD
                    │
                    ▼
              NVIDIA Runtime
                    │
                    ▼
                  CUDA
                    │
                    ▼
                 PyTorch
                    │
                    ▼
                  YOLO
                    │
                    ▼
                  GPU
```

Kubernetes:

```text
AI Deployment
      │
      ▼
GPU Node
      │
      ▼
NVIDIA Device Plugin
      │
      ▼
AI Pod
      │
      ▼
nvidia.com/gpu: 1
```

---

# 23. Model Optimization

Initial implementation:

```text
PyTorch
   ↓
YOLO
   ↓
CUDA
   ↓
GPU
```

For higher performance:

```text
PyTorch YOLO
      │
      ▼
ONNX Export
      │
      ▼
ONNX Runtime
      │
      ▼
GPU
```

or:

```text
YOLO
 │
 ▼
TensorRT
 │
 ▼
NVIDIA GPU
```

Use optimization only after establishing baseline accuracy and latency.

---

# 24. AI Performance Metrics

Expose metrics for:

```text
Inference requests
Inference failures
Inference latency
Preprocessing latency
Postprocessing latency
Model load time
GPU utilization
GPU memory
CPU utilization
Queue length
Frames processed
Frames dropped
Model version
```

Example:

```text
AI Metrics
│
├── inference_requests_total
├── inference_failures_total
├── inference_latency_ms
├── preprocessing_latency_ms
├── postprocessing_latency_ms
├── model_load_seconds
└── frames_processed_total
```

Prometheus collects these.

---

# 25. AI Observability

```text
              AI ENGINE
                  │
       ┌──────────┼───────────┐
       │          │           │
       ▼          ▼           ▼
    Metrics      Logs       Traces
       │          │           │
       ▼          ▼           ▼
 Prometheus    Promtail    OpenTelemetry
                  │           │
                  ▼           ▼
                 Loki        Tempo
                  │           │
                  └─────┬─────┘
                        ▼
                     Grafana
```

This allows you to answer:

> Why did this particular detection take 4 seconds?

by following the request through preprocessing → model inference → postprocessing.

---

# 26. AI Error Handling

Errors should be classified.

```text
AI Errors
│
├── INPUT_INVALID
├── IMAGE_DECODE_FAILED
├── VIDEO_DECODE_FAILED
├── MODEL_NOT_FOUND
├── MODEL_LOAD_FAILED
├── GPU_UNAVAILABLE
├── INFERENCE_FAILED
├── OUT_OF_MEMORY
└── PROCESSING_TIMEOUT
```

Example:

```text
YOLO
 │
 ▼
CUDA Out Of Memory
 │
 ▼
Catch Exception
 │
 ├── Log details
 ├── Update job status
 └── Publish ai.inference.failed
```

Don't expose raw Python stack traces to the frontend.

---

# 27. AI Security

The AI engine should be treated as an internal service.

```text
Internet
   │
   X
   │
AI Engine
```

Only the backend should be able to access it:

```text
Spring Boot
     │
     ▼
Internal Kubernetes Service
     │
     ▼
AI Engine
```

Apply:

```text
NetworkPolicy
Authentication between services
Request validation
File-size limits
Timeouts
Resource limits
Container security
```

---

# 28. Docker Architecture

Use a separate Docker image for inference.

```text
                    Docker
                      │
             ┌────────┴────────┐
             │                 │
        CPU Image          GPU Image
             │                 │
       FastAPI + YOLO     CUDA + PyTorch
             │                 │
             └────────┬────────┘
                      ▼
                  AI Engine
```

A GPU image should include compatible CUDA/PyTorch runtime dependencies.

---

# 29. Kubernetes AI Architecture

```text
                         KUBERNETES
                              │
                              ▼
                       AI Deployment
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
              AI Pod       AI Pod       AI Pod
                 │            │            │
                GPU          GPU          GPU
                 │            │            │
                 └────────────┼────────────┘
                              │
                              ▼
                         Kafka Queue
```

Separate AI workers from normal backend pods.

This means:

```text
More API traffic
    ↓
Scale Spring Boot

More AI jobs
    ↓
Scale AI workers
```

---

# 30. AI Training vs Inference

Keep these completely separate.

```text
                 AI PLATFORM
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
       TRAINING             INFERENCE
          │                     │
          ▼                     ▼
    Dataset Pipeline       FastAPI
          │                     │
          ▼                     ▼
      PyTorch/YOLO           YOLO
          │                     │
          ▼                     ▼
       MLflow              Production
          │
          ▼
    Model Registry
          │
          ▼
   Production Model
```

Training can happen on dedicated GPU infrastructure and should never consume the resources of your production inference service.

---

# 31. Complete AI Engine Architecture

```text id="6x3gwl"
                           SPRING BOOT
                                │
                     ┌──────────┴──────────┐
                     │                     │
                   HTTP                   Kafka
                     │                     │
                     ▼                     ▼
          ┌────────────────────────────────────────┐
          │              AI ENGINE                  │
          │                                         │
          │  ┌───────────────────────────────────┐  │
          │  │         API / CONSUMER            │  │
          │  │ FastAPI • Kafka Consumer           │  │
          │  └────────────────┬──────────────────┘  │
          │                   │                     │
          │  ┌────────────────▼──────────────────┐  │
          │  │       APPLICATION SERVICE        │  │
          │  │       Inference / Job Manager    │  │
          │  └────────────────┬──────────────────┘  │
          │                   │                     │
          │  ┌────────────────▼──────────────────┐  │
          │  │         AI PIPELINE               │  │
          │  │                                   │  │
          │  │  Preprocess                       │  │
          │  │       ↓                           │  │
          │  │  Inference                        │  │
          │  │       ↓                           │  │
          │  │  Postprocess                      │  │
          │  │       ↓                           │  │
          │  │  Tracking                         │  │
          │  └────────────────┬──────────────────┘  │
          │                   │                     │
          │  ┌────────────────▼──────────────────┐  │
          │  │           MODEL LAYER             │  │
          │  │                                   │  │
          │  │ YOLO • PyTorch • Model Registry  │  │
          │  └────────────────┬──────────────────┘  │
          │                   │                     │
          │          ┌────────┴─────────┐           │
          │          ▼                  ▼           │
          │        CUDA               CPU          │
          │          │                              │
          │          ▼                              │
          │        GPU                              │
          └──────────┬──────────────────────────────┘
                     │
                     ▼
             ai.inference.completed
                     │
                     ▼
                SPRING BOOT
                     │
                     ▼
                 PostgreSQL
                     │
                     ▼
               React Frontend


          ┌─────────────────────────────────────────┐
          │            MODEL LIFECYCLE              │
          │                                         │
          │ Dataset → Training → Evaluation        │
          │              ↓                          │
          │            MLflow                      │
          │              ↓                          │
          │       Model Registry                   │
          │              ↓                          │
          │       Production Model                │
          └─────────────────────────────────────────┘


          ┌─────────────────────────────────────────┐
          │             OBSERVABILITY               │
          │                                         │
          │ Prometheus → Metrics                    │
          │ Promtail → Loki → Logs                 │
          │ OpenTelemetry → Tempo → Traces        │
          │                    ↓                    │
          │                  Grafana                │
          └─────────────────────────────────────────┘
```

## Final AI-engine principle

The AI engine should follow this pipeline:

**Input → Validation → Preprocessing → YOLO/PyTorch Inference → Post-processing → Tracking → Result → Kafka/REST**

while the surrounding ML lifecycle follows:

**Dataset → Training → Evaluation → MLflow → Model Registry → Production Model → Inference**.

This gives a clean separation where **Spring Boot manages the application/business world and Python manages the AI world**, while Kafka connects the two asynchronously for scalable image/video processing.
