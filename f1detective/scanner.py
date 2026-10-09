"""Lógica de escaneo y análisis de archivos."""

from __future__ import annotations

import collections
from pathlib import Path

from collections.abc import Callable
from .utils import safe_sha256


def scan_directory(root: Path, on_file: "Callable[[], None] | None" = None) -> dict:
    """Recorre la carpeta y devuelve estadísticas y duplicados."""
    stats = {
        "total_files": 0,
        "total_size": 0,
        "folder_count": 1 if root.is_dir() else 0,
        "largest_file": {"path": None, "size": 0},
        "extensions": collections.Counter(),
        "top_10": [],
        "duplicates": [],
        "duplicate_space": 0,
        "errors": [],
        "symlinks": 0,
    }

    file_sizes: dict[int, list[Path]] = collections.defaultdict(list)

    try:
        for item in root.rglob("*"):
            try:
                if item.is_symlink():
                    stats["symlinks"] += 1
                    continue
                if item.is_dir():
                    stats["folder_count"] += 1
                    continue
                if not item.is_file():
                    continue
                stats["total_files"] += 1
                if on_file is not None:
                    on_file()
                size = item.stat().st_size
                stats["total_size"] += size
                stats["extensions"][item.suffix.lower()] += 1
                if size > stats["largest_file"]["size"]:
                    stats["largest_file"] = {"path": item, "size": size}
                file_sizes[size].append(item)
            except (OSError, PermissionError) as exc:
                stats["errors"].append(str(item))
    except Exception as exc:
        stats["errors"].append(str(exc))

    # Top 10 mayores
    all_files = []
    for size, paths in file_sizes.items():
        for p in paths:
            all_files.append((p, size))
    stats["top_10"] = sorted(all_files, key=lambda x: x[1], reverse=True)[:10]

    # Duplicados
    for size, paths in file_sizes.items():
        if len(paths) < 2:
            continue
        hashes: dict[str, list[Path]] = collections.defaultdict(list)
        for p in paths:
            h = safe_sha256(p)
            if h is not None:
                hashes[h].append(p)
        for h, group in hashes.items():
            if len(group) > 1:
                stats["duplicates"].append({
                    "hash": h,
                    "size": size,
                    "count": len(group),
                    "files": group,
                })
                stats["duplicate_space"] += size * (len(group) - 1)

    return stats
