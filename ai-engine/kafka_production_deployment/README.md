# STEP 20 — Kafka + Production Deployment

This package adds **STEP 20 — Kafka + Production Deployment** without
changing or removing the established Steps 1–19 structure.

The implementation connects the existing AI engine to Kafka and provides
container/Kubernetes deployment artifacts.

## Final architecture position

```text
React
  ↓
Spring Boot
  ↓
Kafka / AI Gateway
  ↓
ai.inference.request
  ↓
AI Engine
  ↓
Experts / Evidence Fusion / Expert 8
  ↓
Decision Outputs
  ↓
ai.inference.completed
  ↓
Spring Boot
  ↓
PostgreSQL / React

Failures
  ↓
ai.inference.failed
  ↓
Retry / DLQ

Follow-up
  ↓
followup.feedback.received
  ↓
Step 19 Follow-up & Feedback
```

# 1. Project structure

The existing structure remains intact:

```text
app/
├── experts/
├── evidence_fusion/
├── expert8_core_ai/
├── decision_outputs/
├── validation_ground_truth/
├── followup_feedback/
│
└── kafka_integration/
    ├── config/
    ├── schemas/
    ├── producer/
    ├── consumer/
    ├── handlers/
    ├── retry/
    ├── dlq/
    ├── serialization/
    └── health/

deploy/
├── docker/
├── kubernetes/
│   ├── base/
│   └── overlays/
│       ├── dev/
│       └── prod/
└── monitoring/
    ├── prometheus/
    ├── grafana/
    ├── loki/
    └── tempo/
```

# 2. Responsibility boundary

Kafka is the asynchronous transport.

Spring Boot remains responsible for:

```text
authentication
authorization
business rules
PostgreSQL
Redis
reports
notifications
API orchestration
audit
```

The Python AI engine remains responsible for:

```text
image/video processing
model inference
AI post-processing
Expert 1–7 inference
evidence fusion
Expert 8 reasoning
AI result generation
AI metrics
```

Step 20 does not move business logic into Kafka.

# 3. Kafka topics

The package defines:

```text
ai.inference.request
ai.inference.completed
ai.inference.failed
ai.inference.dlq
followup.feedback.received
```

## Request

```text
Spring Boot
    ↓
ai.inference.request
    ↓
AI Engine
```

## Completed

```text
AI Engine
    ↓
ai.inference.completed
    ↓
Spring Boot
```

## Failed

```text
AI Engine
    ↓
ai.inference.failed
    ↓
Spring Boot / retry workflow
```

## Dead-letter

```text
Unprocessable message
       ↓
ai.inference.dlq
```

## Follow-up

```text
Follow-up service
       ↓
followup.feedback.received
       ↓
Step 19
```

# 4. Request event contract

```json
{
  "request_id": "REQ-001",
  "job_id": "JOB-001",
  "case_id": "CASE-001",
  "input_type": "image",
  "input_uri": "object://input/image.jpg",
  "model_version": "production",
  "metadata": {}
}
```

The `input_uri` is an object reference.

Large images/videos should not be embedded directly in Kafka messages.

Use object storage and pass a reference.

# 5. Completed event

Conceptually:

```json
{
  "request_id": "REQ-001",
  "job_id": "JOB-001",
  "case_id": "CASE-001",
  "status": "COMPLETED",
  "result": {},
  "model_version": "3.2.0",
  "processing_time_ms": 142.0
}
```

The actual AI result is supplied by the existing inference service.

# 6. Failed event

```json
{
  "request_id": "REQ-001",
  "job_id": "JOB-001",
  "case_id": "CASE-001",
  "status": "FAILED",
  "error_code": "INFERENCE_FAILED",
  "error_message": "processing failed",
  "model_version": "3.2.0",
  "retryable": false
}
```

Raw Python stack traces must not be exposed to the frontend.

# 7. Message serialization

Kafka messages use JSON serialization through the provided codec.

The implementation validates events using Pydantic models.

Flow:

```text
Pydantic Event
      ↓
JSON
      ↓
Kafka
      ↓
JSON
      ↓
Pydantic Event
```

# 8. Consumer behavior

The consumer uses:

```text
enable.auto.commit = false
```

The conceptual processing sequence is:

```text
Poll
 ↓
Decode
 ↓
Validate event
 ↓
Execute handler
 ↓
Commit offset
```

This prevents the consumer from committing the message before the handler
has executed.

A complete production implementation should additionally make the downstream
operation idempotent using `request_id` / `job_id`.

# 9. Retry

Retryability is explicit.

The system does not assume every failure is safe to retry.

Conceptually:

```text
Failure
  ↓
retryable?
  ├── no  → failed / DLQ workflow
  └── yes
        ↓
      attempt
        ↓
      retry
```

The included policy defaults to a maximum of 3 attempts.

That number is configuration, not an agricultural rule.

# 10. Dead-letter queue

Messages that cannot be successfully processed can be routed to:

```text
ai.inference.dlq
```

DLQ records should be investigated rather than silently discarded.

Recommended operational metadata:

```text
request_id
job_id
original_topic
partition
offset
error_code
error_message
failed_at
attempt
```

# 11. Idempotency

Kafka provides at-least-once processing semantics unless the complete
deployment is configured otherwise.

Therefore:

```text
same event
   ↓
may be delivered more than once
```

Downstream services should use:

```text
request_id
job_id
```

as idempotency keys.

Do not create duplicate database records merely because a Kafka message was
redelivered.

# 12. Docker deployment

The package provides:

```text
deploy/docker/Dockerfile
deploy/docker/docker-compose.yml
```

Start:

```bash
docker compose   -f deploy/docker/docker-compose.yml   up --build
```

The compose file provides:

```text
Kafka
AI Engine
```

This is a local/integration deployment, not a complete HA production Kafka
cluster.

# 13. Important Kafka image note

The compose file uses a specific Bitnami Kafka image tag:

```text
bitnami/kafka:3.9
```

The project should pin and test the exact image tag used by the deployment
environment.

Do not silently substitute an unavailable image tag.

# 14. Kubernetes

The package provides:

```text
deploy/kubernetes/base/
├── kafka.yaml
├── ai-engine.yaml
├── topics-job.yaml
└── kustomization.yaml
```

Development overlay:

```text
deploy/kubernetes/overlays/dev/
```

Production overlay:

```text
deploy/kubernetes/overlays/prod/
```

# 15. Kubernetes deployment

Build the image:

```bash
docker build   -f deploy/docker/Dockerfile   -t agri-ai-engine:step20   .
```

Apply:

```bash
kubectl apply -k deploy/kubernetes/overlays/dev
```

For production:

```bash
kubectl apply -k deploy/kubernetes/overlays/prod
```

The production overlay increases the AI-engine deployment to two replicas.

Actual production image registries and GPU node configuration must be supplied
by the deployment environment.

# 16. AI GPU deployment

The base Step 20 manifest deliberately does not fabricate a GPU requirement.

For the actual GPU AI engine, add the existing project's GPU configuration,
for example:

```text
NVIDIA device plugin
GPU node pool
CUDA-compatible image
nvidia.com/gpu resource request
```

The exact CUDA/PyTorch/model combination must match the supplied model.

# 17. Kafka production caveat

The included Kubernetes Kafka manifest is a minimal deployment reference.

It is suitable for development/testing of the integration.

A real production Kafka cluster should provide, as required by the deployment
environment:

```text
multiple brokers
persistent storage
replication
rack/zone awareness
authentication
TLS
authorization
monitoring
backup/recovery
capacity planning
```

The project must not treat the single-broker manifest as a highly available
Kafka cluster.

# 18. Kafka security

The production environment should secure Kafka with the organization's
chosen:

```text
TLS
SASL
ACLs
network policies
secret management
```

The sample development configuration intentionally uses plaintext inside the
local container network.

Do not expose an unsecured Kafka listener to the public Internet.

# 19. Topic partitioning

The development topic initialization uses:

```text
3 partitions
```

This is only a deployment example.

Production partition count should be derived from:

```text
throughput
consumer concurrency
ordering requirements
retention
broker capacity
```

Do not assume three partitions is optimal for production.

# 20. Ordering

If ordering matters for a farm/case workflow, use a stable Kafka key such as:

```text
case_id
```

or:

```text
job_id
```

according to the actual ordering requirement.

Do not rely on global ordering across partitions.

# 21. Object storage

Large files should follow:

```text
Image / Video
      ↓
Object Storage
      ↓
URI
      ↓
Kafka Event
```

Kafka carries metadata and references, not large binary payloads.

The actual object-storage provider remains part of the surrounding platform
architecture.

# 22. AI Engine scaling

The desired scaling boundary is:

```text
More HTTP/API traffic
       ↓
Scale Spring Boot

More inference jobs
       ↓
Scale AI workers
```

Kafka decouples the two workloads.

For GPU inference:

```text
Kafka
  ↓
AI worker pods
  ↓
GPU nodes
```

# 23. Consumer group

AI workers should use the same consumer group when they form one logical
worker pool:

```text
agri-ai-engine
```

Kafka distributes partitions among the workers.

Scaling workers does not necessarily increase throughput if there are fewer
partitions than active consumers.

# 24. Health endpoints

The AI service exposes:

```text
/health
/ready
```

Use:

```text
liveness → /health
readiness → /ready
```

Readiness should represent whether the service is able to accept work.

A future production implementation can extend readiness to include required
Kafka/model readiness checks.

# 25. Observability

The existing project observability architecture remains:

```text
Prometheus
Promtail
Loki
OpenTelemetry
Tempo
Grafana
```

Step 20 does not replace that architecture.

Recommended Kafka/AI operational metrics include:

```text
consumer lag
messages received
messages completed
messages failed
DLQ count
processing latency
queue depth
inference latency
model load time
GPU utilization
GPU memory
```

# 26. Prometheus

The package includes a starter Prometheus configuration:

```text
deploy/monitoring/prometheus/prometheus.yml
```

It targets:

```text
/metrics
```

The existing AI engine should expose its Prometheus metrics endpoint as already
defined in the earlier architecture.

# 27. Logging

Logs should contain correlation identifiers:

```text
request_id
job_id
case_id
model_version
```

Example:

```text
request_id=REQ-001
job_id=JOB-001
model_version=3.2.0
stage=inference
```

Do not log:

```text
credentials
tokens
private URLs
sensitive farmer data
```

# 28. Distributed tracing

The complete trace should conceptually be:

```text
Spring Boot
    ↓
Kafka publish
    ↓
AI consumer
    ↓
Preprocessing
    ↓
Expert inference
    ↓
Evidence fusion
    ↓
Expert 8
    ↓
Kafka result
    ↓
Spring Boot
```

Use OpenTelemetry/Tempo from the existing observability architecture.

# 29. Production deployment separation

Keep:

```text
API/backend pods
```

separate from:

```text
AI worker pods
```

and:

```text
Kafka
```

This allows independent scaling and resource management.

# 30. Failure handling

Example:

```text
Kafka request
     ↓
AI Engine
     ↓
GPU OOM
     ↓
Classify failure
     ↓
ai.inference.failed
     ↓
Retry only if retryable
     ↓
Otherwise DLQ
```

Do not blindly retry non-retryable failures such as malformed input or
missing model artifacts.

# 31. Model deployment

Production model flow remains:

```text
Model Registry
      ↓
Approved Model
      ↓
Container / Model Storage
      ↓
AI Worker
      ↓
Inference
```

Step 20 does not train or promote models automatically.

# 32. Configuration

Kafka configuration is environment-driven:

```text
KAFKA_BOOTSTRAP_SERVERS
KAFKA_CLIENT_ID
KAFKA_CONSUMER_GROUP
KAFKA_INFERENCE_REQUEST_TOPIC
KAFKA_INFERENCE_COMPLETED_TOPIC
KAFKA_INFERENCE_FAILED_TOPIC
KAFKA_FOLLOWUP_TOPIC
KAFKA_DLQ_TOPIC
```

This allows development and production environments to use different brokers
without changing Python code.

# 33. Testing

Install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run unit tests:

```bash
pytest -q
```

Validate Kafka event serialization:

```bash
pytest tests/test_kafka_integration.py -q
```

Start local integration environment:

```bash
docker compose   -f deploy/docker/docker-compose.yml   up --build
```

# 34. Topic initialization

For a running Kafka container:

```bash
docker exec -it agri-kafka   /opt/bitnami/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092   --list
```

The Kubernetes topic-init job creates the defined topics automatically.

# 35. Deployment validation

After deployment:

```bash
kubectl get pods
kubectl get svc
kubectl get jobs
```

Then inspect:

```bash
kubectl logs deployment/ai-engine
kubectl logs job/kafka-topics-init
```

Use the appropriate namespace if the deployment is not in `default`.

# 36. End-to-end message path

```text
1. Spring Boot creates job
        ↓
2. Object stored in object storage
        ↓
3. Spring Boot publishes ai.inference.request
        ↓
4. AI worker consumes event
        ↓
5. Existing AI pipeline processes input
        ↓
6. Result is structured
        ↓
7. AI publishes ai.inference.completed
        ↓
8. Spring Boot consumes result
        ↓
9. Backend persists result
        ↓
10. React receives/display result
```

# 37. Follow-up integration

```text
Farmer / Extension
       ↓
Follow-up
       ↓
Step 19
       ↓
followup.feedback.received
       ↓
Follow-up worker
       ↓
Existing observation/evidence pipeline
       ↓
Validation
       ↓
Learning candidate
```

# 38. Data ownership

Kafka:

```text
transport
```

Object storage:

```text
large binary inputs/outputs
```

Python AI engine:

```text
AI computation
```

Spring Boot:

```text
application/business data
```

PostgreSQL:

```text
persistent business records
```

Redis:

```text
cache / transient state as defined by backend
```

This prevents duplicate ownership of data.

# 39. Production readiness checklist

Before real deployment, verify:

```text
[ ] Kafka HA topology
[ ] Persistent Kafka storage
[ ] TLS
[ ] SASL / authentication
[ ] Kafka ACLs
[ ] Secrets management
[ ] Network policies
[ ] Topic retention
[ ] Partition strategy
[ ] Replication factor
[ ] Consumer lag monitoring
[ ] DLQ monitoring
[ ] AI GPU configuration
[ ] Model artifact availability
[ ] Model version pinning
[ ] Resource limits
[ ] Autoscaling policy
[ ] Health/readiness checks
[ ] Prometheus metrics
[ ] Centralized logs
[ ] Distributed tracing
[ ] Backup/recovery
[ ] Load testing
[ ] Failure testing
```

# 40. Important production limitation

The included Docker Compose and Kubernetes Kafka configuration is a working
development/integration baseline, not a claim of production-grade Kafka HA.

Production sizing and HA must be configured according to the actual cluster,
traffic, storage, availability, security, and recovery requirements.

# 41. Final Step 20 architecture

```text
                         SPRING BOOT
                              │
                              ▼
                   ai.inference.request
                              │
                              ▼
                     ┌─────────────────┐
                     │      KAFKA      │
                     │                 │
                     │ Request         │
                     │ Completed       │
                     │ Failed          │
                     │ DLQ             │
                     │ Follow-up       │
                     └────────┬────────┘
                              │
                              ▼
                       AI ENGINE WORKERS
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
         CPU Worker                       GPU Worker
              │                               │
              └───────────────┬───────────────┘
                              ▼
                    Existing AI Pipeline
                              │
                   ┌──────────┴──────────┐
                   ▼                     ▼
               Experts 1–7          Expert 8
                   │                     │
                   └──────────┬──────────┘
                              ▼
                    Decision Outputs
                              │
                              ▼
                    ai.inference.completed
                              │
                              ▼
                         SPRING BOOT
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
             PostgreSQL     Redis        React
```

# 42. Final principle

Step 20 completes the deployment/transport boundary:

```text
Spring Boot
    ↕
  Kafka
    ↕
Python AI Engine
```

while preserving the existing internal AI architecture:

```text
Input
 ↓
Observation / Environment / Remote Sensing
 ↓
Experts 1–7
 ↓
Structured Evidence Fusion
 ↓
Expert 8
 ↓
Decision / Risk / Recommendation
 ↓
Validation
 ↓
Follow-up & Feedback
```

Kafka is the communication layer; it does not replace any of the existing
AI, validation, business, or feedback components.
