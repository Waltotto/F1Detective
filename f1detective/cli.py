"""Punto de entrada CLI."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from .scanner import scan_directory
from .formatters import print_banner, print_dashboard

console = Console()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="f1detective",
        description="Analiza una carpeta y genera un informe.",
    )
    parser.add_argument("path", type=str, help="Ruta de la carpeta a analizar")
    args = parser.parse_args(argv)

    root = Path(args.path)
    if not root.exists():
        console.print("[red bold]❌ La ruta no existe:[/red bold] {}".format(root))
        return 1
    if not root.is_dir():
        console.print("[red bold]❌ No es una carpeta:[/red bold] {}".format(root))
        return 1

    print_banner()
    console.print()
    console.print("[bold bright_blue]🎯 Carpeta investigada:[/bold bright_blue] {}".format(root.resolve()))
    console.print("[dim]Iniciando escaneo recursivo...[/dim]")

    start = time.perf_counter()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Investigando archivos...", total=None)
        stats = scan_directory(root, on_file=lambda: progress.advance(task, 1))
        progress.update(task, description="[green]Investigación completa[/green]", completed=stats["total_files"])

    duration = time.perf_counter() - start
    stats["duration"] = duration
    print_dashboard(stats)
    return 0
