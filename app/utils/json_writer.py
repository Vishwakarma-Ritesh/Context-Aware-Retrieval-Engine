"""JSON artifact writer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.utils.file_handlers import ensure_parent_directory


def write_json(path: Path, payload: dict[str, Any] | list[dict[str, Any]]) -> None:
    ensure_parent_directory(path)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
