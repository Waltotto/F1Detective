"""Utilidades seguras para F1Detective."""

from __future__ import annotations

import hashlib
from pathlib import Path


def safe_sha256(path: Path) -> str | None:
    """Calcula SHA-256 de un archivo de forma segura."""
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return None
