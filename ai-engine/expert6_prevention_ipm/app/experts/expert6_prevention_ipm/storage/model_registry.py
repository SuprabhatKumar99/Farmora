from pathlib import Path


class LocalModelRegistry:
    """Development registry for Expert 6 model artifacts."""

    def __init__(self, root="models/expert6_prevention_ipm"):
        self.root = Path(root)

    def resolve(self, version, filename):
        path = self.root / version / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Model artifact not found: {path}"
            )

        return path
