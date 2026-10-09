"""Pruebas básicas para scanner."""

import tempfile
from pathlib import Path
from f1detective.scanner import scan_directory


def test_scan_empty():
    with tempfile.TemporaryDirectory() as tmp:
        result = scan_directory(Path(tmp))
        assert result["total_files"] == 0
