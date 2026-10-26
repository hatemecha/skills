import json
from pathlib import Path


def load_settings(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_settings(path: Path, settings: dict) -> None:
    path.write_text(json.dumps(settings), encoding="utf-8")


def update_settings(path: Path, changes: dict) -> dict:
    current = load_settings(path)
    current.update(changes)
    return current
