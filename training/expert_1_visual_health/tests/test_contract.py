from pathlib import Path

def test_canonical_structure():
    root = Path(__file__).resolve().parents[2]
    for name in [f"{i:02d}_" for i in range(1,12)]:
        assert any(p.name.startswith(name) for p in root.iterdir())
