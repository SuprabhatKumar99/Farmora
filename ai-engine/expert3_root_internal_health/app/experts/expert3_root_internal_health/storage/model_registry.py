from pathlib import Path


class LocalModelRegistry:
    """Development registry for Expert 3 model artifacts."""

    def __init__(
        self,
        root="models/expert3_root_internal_health",
    ):
        self.root = Path(root)

    def resolve(self, version, filename):
        path = self.root / version / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Model artifact not found: {path}"
            )

        return path
