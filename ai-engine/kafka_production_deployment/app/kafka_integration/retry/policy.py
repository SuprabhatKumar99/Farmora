class RetryPolicy:
    """Deterministic retry decision.

    Retryability is supplied by the failure classification; this component
    does not guess whether an agricultural/AI failure is safe to retry.
    """

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def should_retry(self, retryable: bool, attempt: int) -> bool:
        return retryable and attempt < self.max_retries
