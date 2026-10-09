"""Renderizado de resultados con Rich."""

from __future__ import annotations

from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


def print_banner() -> None:
    title = "[bold bright_blue]🔎 F1Detective[/bold bright_blue]\n[dim]Investigate your filesystem.[/dim]"
    console.print(Panel(title, border_style="bright_blue", padding=(1, 2)))


def print_dashboard(stats: dict) -> None:
    console.print()

    # Resumen principal en panel
    main_table = Table(show_header=False, box=box.ROUNDED, border_style="bright_blue")
    main_table.add_column("Métrica", style="bold cyan")
    main_table.add_column("Valor", style="bold white")

    duration = stats.get("duration", 0)
    largest = stats["largest_file"]
    largest_str = f"{largest['path']} ({largest['size']:,} bytes)" if largest["path"] else "N/A"

    main_table.add_row("Archivos", str(stats["total_files"]))
    main_table.add_row("Carpetas", str(stats["folder_count"]))
    main_table.add_row("Tamaño total", f"{stats['total_size']:,} bytes")
    main_table.add_row("Duración", f"{duration:.2f} s")
    main_table.add_row("Errores", str(len(stats["errors"])))
    main_table.add_row("Archivo más grande", largest_str)
    main_table.add_row("Enlaces simbólicos", str(stats["symlinks"]))

    console.print(Panel(main_table, title="[bold bright_blue]📊 RESUMEN DE INVESTIGACIÓN[/bold bright_blue]", border_style="bright_blue"))

    # Archivos más grandes
    if stats["top_10"]:
        t10 = Table(title="[bold]📁 Archivos más grandes[/bold]", box=box.ROUNDED, border_style="green")
        t10.add_column("Archivo", overflow="fold", style="cyan")
        t10.add_column("Tamaño (bytes)", justify="right", style="yellow")
        for p, s in stats["top_10"]:
            t10.add_row(str(p), f"{s:,}")
        console.print(t10)

    # Duplicados
    if stats["duplicates"]:
        dup_groups = len(stats["duplicates"])
        dup_files = sum(d["count"] for d in stats["duplicates"])
        dup_space = stats["duplicate_space"]
        dup_title = f"[bold]🔍 Duplicados detectados[/bold] — {dup_groups} grupos, {dup_files} archivos, {dup_space:,} bytes recuperables"
        dup_table = Table(title=dup_title, box=box.ROUNDED, border_style="red")
        dup_table.add_column("Grupo", style="bold")
        dup_table.add_column("Cantidad", justify="right")
        dup_table.add_column("Tamaño (bytes)", justify="right")
        dup_table.add_column("Hash (primeros 16)", style="dim")
        for idx, d in enumerate(stats["duplicates"], 1):
            files_str = "\n".join(str(p.name) for p in d["files"][:3])
            if len(d["files"]) > 3:
                files_str += f"\n... (+{len(d['files'])-3} más)"
            dup_table.add_row(
                f"Grupo {idx}",
                str(d["count"]),
                f"{d['size']:,}",
                d["hash"][:16],
            )
        console.print(dup_table)
    else:
        console.print("[green bold]✓ No se detectaron duplicados.[/green bold]")

    # Extensiones
    ext = stats["extensions"]
    if ext:
        ext_table = Table(title="[bold]📂 Resumen de extensiones[/bold]", box=box.ROUNDED, border_style="magenta")
        ext_table.add_column("Extensión", style="bold")
        ext_table.add_column("Cantidad", justify="right", style="cyan")
        for k, v in ext.most_common():
            ext_table.add_row(k or "(sin extensión)", str(v))
        console.print(ext_table)

    if stats["errors"]:
        console.print(f"[yellow bold]⚠️ Archivos inaccesibles o errores:[/yellow bold] {len(stats['errors'])}")

    # Final
    console.print()
    console.print(Panel("[bold bright_green]✓ Investigation complete[/bold bright_green]\n[dim]F1Detective V1.5 — Análisis terminado sin modificar archivos.[/dim]", border_style="bright_green"))
