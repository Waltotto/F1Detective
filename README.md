# F1Detective

F1Detective is a small, clean, and secure CLI tool that investigates your filesystem. It analyzes a folder, counts files and directories, calculates total size, finds the largest files, summarizes extensions, detects duplicates using SHA-256, and presents everything in an attractive terminal dashboard — without modifying or deleting any file.

## What problem it solves

When you need a quick, safe overview of a folder — how big it is, what's taking space, whether there are duplicates — most tools either lack visual clarity or risk touching your data. F1Detective provides a professional, readable report with zero side effects.

## Main features

- Recursive folder analysis
- File and folder counts
- Total size calculation
- Largest files table (top 10)
- Extension frequency summary
- Duplicate detection (size filter + SHA-256 hash)
- Symlink detection and safe skipping
- Graceful error handling for inaccessible or missing files
- Beautiful terminal output using Rich
- No modifications to any analyzed file

## Installation

```bash
pip install -e .
```

This creates the `f1detective` entry point.

## Usage

```bash
f1detective <folder>
```

Example:

```bash
f1detective .
```

Or as a module:

```bash
python -m f1detective .
```

## Example output (summary)

```
╔══════════════════════════════════════╗
║  🔎 F1Detective                          ║
║  Investigate your filesystem.            ║
╚══════════════════════════════════════╝
```

- Total files
- Total folders
- Total size
- Duration
- Largest file
- Duplicate groups (count + recoverable space)
- Extension summary
- Final status: `✓ Investigation complete`

## Tests

```bash
python -m pytest
```

## Security

F1Detective is read-only. It never deletes, moves, renames, or modifies any file. It handles missing files and permission errors gracefully without stopping the analysis.

## Project structure

```
f1detective/
├── f1detective/     # source package
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── scanner.py
│   ├── formatters.py
│   └── utils.py
├── tests/
│   └── test_scanner.py
├── pyproject.toml
├── .gitignore
└── README.md
```

## Roadmap (future, not implemented)

- JSON/CSV export
- Filter by extension or date
- Pattern exclusions (e.g., `.git/`, `node_modules`)
- Progress bar customization

## License

MIT
