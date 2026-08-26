# Backend Architecture

 **Spring Boot modular backend** with PostgreSQL as the source of truth, Redis for caching, Kafka for asynchronous event processing, and a dedicated AI Gateway/Client layer for communicating with the Python AI engine.

The key design choice: **start as a modular monolith, but structure it so individual modules can later be extracted into microservices if the project scales.**

---

## 1. Backend Technology Stack

| Layer               | Technology                         |
| ------------------- | ---------------------------------- |
| Language            | **Java 21**                        |
| Framework           | **Spring Boot 3.x**                |
| API                 | Spring Web / REST                  |
| Security            | Spring Security                    |
| Authentication      | JWT + HttpOnly Cookie              |
| Authorization       | RBAC                               |
| ORM                 | Spring Data JPA + Hibernate        |
| Database            | **PostgreSQL**                     |
| DB Migration        | Flyway                             |
| Cache               | **Redis**                          |
| Messaging           | **Apache Kafka**                   |
| Kafka Integration   | Spring Kafka                       |
| AI Communication    | WebClient / OpenFeign              |
| Real-time           | WebSocket / STOMP                  |
| Validation          | Jakarta Bean Validation            |
| Resilience          | Resilience4j                       |
| API Documentation   | OpenAPI / Swagger                  |
| Logging             | SLF4J + Logback                    |
| Metrics             | Micrometer                         |
| Distributed Tracing | OpenTelemetry                      |
| Testing             | JUnit 5 + Mockito + Testcontainers |
| Containerization    | Docker                             |
| Orchestration       | Kubernetes                         |

---

# 2. High-Level Backend Architecture

```text
                         ┌─────────────────────┐
                         │   React Frontend    │
                         └──────────┬──────────┘
                                    │
                              HTTPS / REST
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   NGINX / Ingress   │
                         └──────────┬──────────┘
                                    │
                                    ▼
              ┌─────────────────────────────────────────┐
              │             SPRING BOOT                  │
              │                                         │
              │              API LAYER                  │
              │                                         │
              │ Controllers • DTOs • Validation        │
              └───────────────────┬─────────────────────┘
                                  │
                                  ▼
              ┌─────────────────────────────────────────┐
              │          APPLICATION LAYER              │
              │                                         │
              │ Auth • Detection • Reports • Alerts   │
              │ Analytics • Users • Media • AI        │
              └───────────────────┬─────────────────────┘
                                  │
                                  ▼
              ┌─────────────────────────────────────────┐
              │             DOMAIN LAYER                │
              │                                         │
              │ Entities • Business Rules • Events     │
              └───────────────┬─────────┬───────────────┘
                              │         │
                 ┌────────────┘         └─────────────┐
                 ▼                                    ▼
        ┌─────────────────┐                  ┌────────────────┐
        │ Infrastructure  │                  │ Event System   │
        │                 │                  │                │
        │ PostgreSQL      │                  │ Kafka          │
        │ Redis           │                  │ Producers      │
        │ Object Storage  │                  │ Consumers      │
        └─────────────────┘                  └───────┬────────┘
                                                     │
                                                     ▼
                                            ┌─────────────────┐
                                            │   AI ENGINE     │
                                            │ Python/FastAPI   │
                                            │ PyTorch + YOLO   │
                                            └─────────────────┘
```

---

# 3. Backend Internal Architecture

Use a **Clean/Hexagonal-inspired architecture**.

```text
┌─────────────────────────────────────────────┐
│              Presentation Layer             │
│                                             │
│ REST Controllers                            │
│ WebSocket Controllers                        │
│ Exception Handlers                           │
│ Request/Response DTOs                        │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│             Application Layer               │
│                                             │
│ Use Cases                                   │
│ Application Services                        │
│ Transaction Management                      │
│ Event Publishing                            │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│                Domain Layer                 │
│                                             │
│ Entities                                    │
│ Value Objects                               │
│ Business Rules                              │
│ Domain Events                               │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│             Infrastructure Layer            │
│                                             │
│ JPA Repositories                            │
│ PostgreSQL                                  │
│ Redis                                       │
│ Kafka                                       │
│ AI Client                                   │
│ Object Storage                              │
└─────────────────────────────────────────────┘
```

This prevents your controllers from becoming overloaded with business logic.

---

# 4. Recommended Project Structure

```text
backend/
│
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/sih/project/
│   │   │
│   │   │       ├── BackendApplication.java
│   │   │       │
│   │   │       ├── config/
│   │   │       │   ├── SecurityConfig.java
│   │   │       │   ├── KafkaConfig.java
│   │   │       │   ├── RedisConfig.java
│   │   │       │   ├── WebSocketConfig.java
│   │   │       │   ├── OpenApiConfig.java
│   │   │       │   └── CorsConfig.java
│   │   │       │
│   │   │       ├── auth/
│   │   │       ├── user/
│   │   │       ├── detection/
│   │   │       ├── media/
│   │   │       ├── ai/
│   │   │       ├── report/
│   │   │       ├── alert/
│   │   │       ├── analytics/
│   │   │       ├── notification/
│   │   │       ├── camera/
│   │   │       └── audit/
│   │   │
│   │   └── resources/
│   │       ├── application.yml
│   │       ├── application-dev.yml
│   │       ├── application-prod.yml
│   │       │
│   │       └── db/
│   │           └── migration/
│   │               ├── V1__init.sql
│   │               ├── V2__users.sql
│   │               ├── V3__detections.sql
│   │               └── ...
│   │
│   └── test/
│
├── Dockerfile
├── pom.xml
└── README.md
```

---

# 5. Feature Module Architecture

Each major feature should follow the same structure.

Example:

```text
detection/
│
├── controller/
│   └── DetectionController.java
│
├── service/
│   └── DetectionService.java
│
├── repository/
│   └── DetectionRepository.java
│
├── entity/
│   └── Detection.java
│
├── dto/
│   ├── DetectionRequest.java
│   └── DetectionResponse.java
│
├── mapper/
│   └── DetectionMapper.java
│
├── event/
│   ├── DetectionCreatedEvent.java
│   └── DetectionEventPublisher.java
│
├── exception/
│   └── DetectionNotFoundException.java
│
└── validator/
    └── DetectionValidator.java
```

This pattern should be reused for:

```text
auth/
user/
media/
detection/
ai/
report/
alert/
analytics/
camera/
notification/
audit/
```

---

# 6. Core Backend Modules

## Authentication

Responsible for:

* Login
* Logout
* Token/session management
* Password management
* Authentication
* Role verification

```text
auth/
├── controller/
├── service/
├── security/
├── repository/
├── entity/
└── dto/
```

---

## User Management

Responsible for:

* User profiles
* Roles
* Permissions
* User activation/deactivation
* User administration

Example roles:

```text
ADMIN
OPERATOR
ANALYST
VIEWER
```

---

## Media Management

Responsible for:

* Image uploads
* Video uploads
* File metadata
* Storage references
* Upload status
* Processing status

Important:

```text
Spring Boot
     │
     ├── metadata → PostgreSQL
     │
     └── actual file → Object Storage
```

Don't store large media files directly in PostgreSQL.

---

# 7. Detection Module

This is the core business module.

```text
Detection
│
├── Create detection job
├── Submit AI inference
├── Track processing status
├── Store AI results
├── Query detection history
├── Filter detections
├── Detection statistics
└── Detection details
```

Example lifecycle:

```text
UPLOADED
    │
    ▼
QUEUED
    │
    ▼
PROCESSING
    │
    ├─────────────┐
    ▼             ▼
COMPLETED       FAILED
```

---

# 8. AI Gateway Architecture

The backend should **not contain the YOLO/PyTorch implementation**.

Instead:

```text
Spring Boot
     │
     ▼
AI Gateway
     │
     ├── HTTP Client
     ├── Request validation
     ├── Timeout
     ├── Retry
     ├── Circuit breaker
     └── Result mapping
     │
     ▼
Python AI Engine
```

For example:

```text
ai/
├── client/
│   ├── AiEngineClient.java
│   └── AiEngineClientImpl.java
│
├── dto/
│   ├── AiInferenceRequest.java
│   └── AiInferenceResponse.java
│
├── service/
│   └── AiService.java
│
└── config/
    └── AiEngineProperties.java
```

---

# 9. Kafka Architecture

Kafka acts as the **event backbone**.

```text
                 SPRING BOOT
                      │
           ┌──────────┴──────────┐
           │                     │
        Producer              Consumer
           │                     │
           ▼                     │
      ┌─────────┐                │
      │  KAFKA  │────────────────┘
      └────┬────┘
           │
     ┌─────┼──────────────────────┐
     │     │                      │
     ▼     ▼                      ▼
    AI   Alert                Notification
 Worker  Worker                  Worker
```

Recommended topics:

```text
media.uploaded
media.processing
ai.inference.request
ai.inference.completed
ai.inference.failed

detection.created
detection.completed

report.generate
report.generated

alert.created
notification.send

audit.event
```

---

# 10. Asynchronous AI Processing

For a large video:

```text
POST /api/v1/detections
             │
             ▼
       DetectionService
             │
       Create Job
             │
             ▼
         PostgreSQL
             │
             ▼
          Kafka
             │
             │ ai.inference.request
             ▼
        Python AI Engine
             │
             ▼
       YOLO / PyTorch
             │
             ▼
          Kafka
             │
             │ ai.inference.completed
             ▼
        Spring Consumer
             │
       ┌─────┴─────┐
       ▼           ▼
 PostgreSQL       Redis
       │
       ▼
 WebSocket Event
       │
       ▼
 React Dashboard
```

The user therefore doesn't have to keep an HTTP request open while a large video is processed.

---

# 11. PostgreSQL Architecture

PostgreSQL should contain authoritative business data.

Recommended logical tables:

```text
users
roles
permissions
user_roles

media
media_metadata

detections
detection_objects
detection_results

ai_models
ai_model_versions

cameras
camera_events

alerts
notifications

reports
report_items

processing_jobs

audit_logs
```

Relationship:

```text
USER
 │
 ├───────────────┐
 ▼               ▼
MEDIA           REPORT
 │
 ▼
PROCESSING JOB
 │
 ▼
DETECTION
 │
 ▼
DETECTION OBJECT
 │
 ├── class
 ├── confidence
 ├── bounding box
 └── metadata
```

---

# 12. Database Layer

Use:

```text
Spring Data JPA
       │
       ▼
Hibernate
       │
       ▼
HikariCP
       │
       ▼
PostgreSQL
```

Use **Flyway** for schema versioning:

```text
V1__initial_schema.sql
V2__create_users.sql
V3__create_media.sql
V4__create_detections.sql
V5__create_alerts.sql
```

Never manually modify production database schemas.

---

# 13. Redis Architecture

Redis should be used for data that needs fast access and doesn't need to be the permanent source of truth.

```text
Redis
│
├── Dashboard cache
├── Detection status
├── Session-related data
├── Rate limiting
├── Temporary processing state
├── Distributed locks
└── Frequently accessed configuration
```

Example:

```text
GET /api/v1/dashboard
          │
          ▼
        Redis
       /     \
    HIT       MISS
     │          │
     ▼          ▼
  Response   PostgreSQL
                │
                ▼
              Redis
                │
                ▼
             Response
```

---

# 14. WebSocket Architecture

WebSockets are useful for real-time UI updates.

```text
Kafka Event
     │
     ▼
Spring Kafka Consumer
     │
     ▼
Application Service
     │
     ▼
WebSocket Publisher
     │
     ▼
React Frontend
```

Use it for:

* Detection completion
* AI processing progress
* Alerts
* Notifications
* Camera status
* Job status

---

# 15. REST API Structure

Use versioned APIs:

```text
/api/v1/
```

Recommended endpoints:

```text
/api/v1/auth
/api/v1/users
/api/v1/media
/api/v1/detections
/api/v1/ai
/api/v1/reports
/api/v1/alerts
/api/v1/analytics
/api/v1/cameras
/api/v1/notifications
```

Example:

```text
POST   /api/v1/auth/login

GET    /api/v1/detections
POST   /api/v1/detections
GET    /api/v1/detections/{id}

POST   /api/v1/media/upload

GET    /api/v1/reports
POST   /api/v1/reports

GET    /api/v1/alerts
PATCH  /api/v1/alerts/{id}/status

GET    /api/v1/analytics/overview
```

---

# 16. API Request Flow

```text
React
 │
 ▼
POST /api/v1/detections
 │
 ▼
Controller
 │
 ▼
DTO Validation
 │
 ▼
Authentication
 │
 ▼
Authorization
 │
 ▼
DetectionService
 │
 ├── PostgreSQL
 │
 ├── Redis
 │
 └── Kafka
       │
       ▼
    AI Engine
```

Controllers should remain thin:

```text
Controller
    ↓
Service
    ↓
Repository / Event / External Client
```

Avoid putting business logic inside controllers.

---

# 17. Security Architecture

```text
                       REQUEST
                          │
                          ▼
                   Spring Security
                          │
              ┌───────────┴───────────┐
              │                       │
        Authentication          Authorization
              │                       │
           JWT/Cookie             RBAC
              │                       │
              └───────────┬───────────┘
                          ▼
                    Controller
                          │
                          ▼
                     Service
```

### Security layers

```text
HTTPS
  ↓
CORS
  ↓
Authentication
  ↓
Authorization
  ↓
Input Validation
  ↓
Business Rules
  ↓
Audit Logging
```

Never expose:

```text
PostgreSQL
Redis
Kafka
AI Engine
```

directly to the public internet.

---

# 18. RBAC Architecture

```text
User
 │
 ▼
Role
 │
 ├── ADMIN
 │     ├── Users
 │     ├── System
 │     └── Reports
 │
 ├── OPERATOR
 │     ├── Detection
 │     ├── Cameras
 │     └── Alerts
 │
 ├── ANALYST
 │     ├── Analytics
 │     └── Reports
 │
 └── VIEWER
       ├── Dashboard
       └── Read-only Detection
```

Spring Security should enforce these permissions server-side.

---

# 19. Resilience Architecture

Communication with the AI engine and other external systems should use:

**Resilience4j**

```text
Spring Boot
     │
     ▼
AI Gateway
     │
     ├── Timeout
     ├── Retry
     ├── Circuit Breaker
     ├── Bulkhead
     └── Fallback
     │
     ▼
AI Engine
```

Example:

```text
AI Engine unavailable
        │
        ▼
Circuit Breaker
        │
        ▼
Don't repeatedly call AI
        │
        ▼
Job → FAILED / RETRY_PENDING
        │
        ▼
Alert / UI status
```

This prevents an AI-engine failure from taking down the entire backend.

---

# 20. Observability

The backend should expose metrics through **Micrometer**.

```text
Spring Boot
     │
     ├── Metrics ────────► Prometheus
     │
     ├── Logs ───────────► Promtail → Loki
     │
     └── Traces ─────────► OpenTelemetry → Tempo
                                      │
                                      ▼
                                   Grafana
```

Monitor:

```text
HTTP request latency
HTTP error rate
JVM memory
JVM CPU
Database connections
Kafka consumer lag
Kafka producer errors
Redis latency
AI request latency
AI failure rate
Active jobs
Detection processing time
```

---

# 21. Distributed Tracing

Every important request should have:

```text
traceId
requestId
jobId
userId
```

Example:

```text
Frontend
   │
   │ traceId = ABC123
   ▼
Spring Boot
   │
   ├────────► PostgreSQL
   │
   ├────────► Redis
   │
   └────────► Kafka
                  │
                  ▼
              AI Engine
                  │
                  ▼
               PyTorch
```

In Grafana Tempo, you should be able to follow the entire request.

---

# 22. Error Handling

Centralize errors:

```text
controller/
     │
     ▼
GlobalExceptionHandler
     │
     ▼
Standard API Response
```

Example response:

```json
{
  "success": false,
  "error": {
    "code": "DETECTION_NOT_FOUND",
    "message": "Detection was not found",
    "timestamp": "2026-08-26T10:30:00Z",
    "requestId": "req-123"
  }
}
```

Use consistent error codes such as:

```text
AUTH_INVALID
AUTH_FORBIDDEN

USER_NOT_FOUND
MEDIA_NOT_FOUND

DETECTION_NOT_FOUND
DETECTION_PROCESSING_FAILED

AI_ENGINE_UNAVAILABLE
AI_INFERENCE_FAILED

REPORT_GENERATION_FAILED
```

---

# 23. Transaction Management

For operations involving PostgreSQL:

```text
@Service
@Transactional
```

Example:

```text
Create Detection
      │
      ├── Save detection
      ├── Save processing job
      └── Create event
```

For database + Kafka consistency, use an **outbox pattern** for critical events.

```text
                 Transaction
                      │
             ┌────────┴─────────┐
             ▼                  ▼
        PostgreSQL          Outbox Table
             │                  │
             └────────┬─────────┘
                      ▼
                Kafka Publisher
                      │
                      ▼
                    Kafka
```

This prevents the situation where PostgreSQL succeeds but Kafka publishing fails.

---

# 24. Background Workers

Not every task should run inside an HTTP request.

Create asynchronous workers for:

```text
AI inference
Video processing
Report generation
Notifications
Analytics aggregation
Cleanup
Audit processing
```

Architecture:

```text
Kafka
 │
 ├── AI Worker
 ├── Report Worker
 ├── Notification Worker
 └── Analytics Worker
```

Initially, these can be Spring Boot consumers inside the same application.

Later:

```text
Spring Boot
     │
     ├── API Service
     ├── AI Worker
     ├── Report Worker
     └── Notification Worker
```

can become separate Kubernetes deployments.

---

# 25. Backend Kubernetes Architecture

```text
                       Kubernetes
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
     Backend Pods       AI Worker Pods    Worker Pods
          │                 │                 │
          │                 │                 │
          └────────────┬────┴─────────────────┘
                       │
          ┌────────────┼─────────────┐
          ▼            ▼             ▼
     PostgreSQL      Redis          Kafka
          │
          ▼
     Persistent Volume
```

Backend should use:

```text
Deployment
Service
ConfigMap
Secret
HorizontalPodAutoscaler
PodDisruptionBudget
NetworkPolicy
Ingress
```

---

# 26. Scaling Architecture

Spring Boot API:

```text
                Load Balancer
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Backend    Backend    Backend
        Pod 1      Pod 2      Pod 3
          │          │          │
          └──────────┼──────────┘
                     ▼
              PostgreSQL
                     │
                   Redis
```

The backend should remain **stateless** wherever possible.

This allows Kubernetes to horizontally scale it.

---

# 27. AI Scaling

AI workloads are different from normal API workloads.

```text
Kafka
 │
 ▼
AI Inference Queue
 │
 ├────► AI Pod 1 ──► GPU
 │
 ├────► AI Pod 2 ──► GPU
 │
 └────► AI Pod 3 ──► GPU
```

You can independently scale AI workers according to queue length/GPU utilization without scaling the REST API.

---

# 28. Backend Deployment Architecture

```text
                         INTERNET
                            │
                            ▼
                     NGINX Ingress
                            │
                            ▼
                  ┌───────────────────┐
                  │ Spring Boot API   │
                  │   Kubernetes      │
                  └─────────┬─────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
      PostgreSQL          Redis             Kafka
          │                                   │
          │                                   │
          │                         ┌─────────┴─────────┐
          │                         ▼                   ▼
          │                    AI Workers          Other Workers
          │                         │
          │                         ▼
          │                    Python AI
          │                         │
          │                         ▼
          │                    PyTorch/YOLO
          │
          └─────────────────────────────────────┐
                                                │
                                                ▼
                                          Object Storage
```

---

# 29. Backend CI/CD

```text
Developer
   │
   ▼
Git Push
   │
   ▼
GitHub Actions
   │
   ├── Compile
   ├── Unit Tests
   ├── Integration Tests
   ├── Testcontainers
   ├── Static Analysis
   ├── Dependency Scan
   ├── Docker Build
   └── Trivy Scan
           │
           ▼
    Container Registry
           │
           ▼
      Kubernetes
           │
       ┌───┴────┐
       ▼        ▼
    Staging  Production
```

---

# 30. Complete Backend Architecture

```text
┌────────────────────────────────────────────────────────────────────┐
│                           CLIENT                                   │
│                     React + TypeScript                             │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                          HTTPS / WS
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                         K8S INGRESS                                │
│                    NGINX + TLS + Routing                           │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                         SPRING BOOT                                │
│                                                                    │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │                    PRESENTATION LAYER                          │ │
│ │ Controllers • DTOs • Validation • Exception Handler           │ │
│ └────────────────────────────┬───────────────────────────────────┘ │
│                              ▼                                     │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │                    APPLICATION LAYER                           │ │
│ │ Auth • Detection • Media • Reports • Alerts • Analytics       │ │
│ │ Users • Cameras • Notifications • AI Gateway                  │ │
│ └────────────────────────────┬───────────────────────────────────┘ │
│                              ▼                                     │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │                       DOMAIN LAYER                              │ │
│ │ Entities • Business Rules • Domain Events                     │ │
│ └────────────────────────────┬───────────────────────────────────┘ │
│                              ▼                                     │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │                  INFRASTRUCTURE LAYER                          │ │
│ │ JPA • Redis • Kafka • AI Client • Object Storage              │ │
│ └──────────────┬───────────────┬───────────────┬─────────────────┘ │
└────────────────┼───────────────┼───────────────┼───────────────────┘
                 │               │               │
                 ▼               ▼               ▼
          ┌────────────┐   ┌───────────┐   ┌─────────────┐
          │ PostgreSQL │   │   Redis   │   │    Kafka    │
          │            │   │           │   │             │
          │ Source of  │   │ Cache &   │   │ Event Bus   │
          │ Truth      │   │ Fast Data │   │             │
          └────────────┘   └───────────┘   └──────┬──────┘
                                                  │
                                  ┌───────────────┼───────────────┐
                                  │               │               │
                                  ▼               ▼               ▼
                             AI Worker       Report Worker   Notification
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   AI ENGINE      │
                         │ FastAPI          │
                         │ PyTorch          │
                         │ YOLO             │
                         │ OpenCV           │
                         └──────────────────┘


┌────────────────────────────────────────────────────────────────────┐
│                       OBSERVABILITY                                │
│                                                                    │
│ Prometheus ──► Metrics                                             │
│ Promtail ────► Loki ──► Logs                                      │
│ OpenTelemetry ──► Tempo ──► Traces                                │
│                         │                                          │
│                         ▼                                          │
│                       Grafana                                     │
└────────────────────────────────────────────────────────────────────┘
```

## Recommended backend principle

The clean dependency direction should be:

**Controller → Service/Use Case → Domain → Repository/Infrastructure**

while infrastructure dependencies such as **PostgreSQL, Redis, Kafka, Object Storage, and the AI Engine remain behind clearly defined interfaces**.

That gives you a backend that is **secure, asynchronous, observable, horizontally scalable, and ready to evolve from a prototype into a production system**.
