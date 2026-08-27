from pathlib import Path

class LocalModelRegistry:
    def __init__(self, root="models/expert1_visual_health"):
        self.root = Path(root)

    def resolve(self, version, filename):
        path = self.root / version / filename
        if not path.exists():
            raise FileNotFoundError(f"Model artifact not found: {path}")
        return path
