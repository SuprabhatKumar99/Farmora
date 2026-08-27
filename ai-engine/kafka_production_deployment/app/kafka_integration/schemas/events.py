from pydantic import BaseModel, Field


class InferenceRequestEvent(BaseModel):
    request_id: str
    job_id: str
    case_id: str | None = None
    input_type: str
    input_uri: str
    model_version: str = "production"
    metadata: dict = Field(default_factory=dict)


class InferenceCompletedEvent(BaseModel):
    request_id: str
    job_id: str
    case_id: str | None = None
    status: str
    result: dict
    model_version: str
    processing_time_ms: float | None = None


class InferenceFailedEvent(BaseModel):
    request_id: str
    job_id: str
    case_id: str | None = None
    status: str = "FAILED"
    error_code: str
    error_message: str
    model_version: str = "unknown"
    retryable: bool = False
