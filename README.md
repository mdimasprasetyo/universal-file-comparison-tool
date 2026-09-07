# Universal File Comparison Tool

A fast, zero-dependency Python GUI application built with Tkinter for universal file comparison. Uses SHA-256 cryptographic hashing to reliably verify bit-for-bit file integrity across any format (.cdr, images, docs, audio) and includes text-level diffing.

## Features

- **File picker UI** — browse and select any two files to compare
- **Size check** — reports the size of each file in bytes
- **SHA-256 hash comparison** — detects exact binary matches, regardless of file type
- **Text diff** — for `.txt`, `.csv`, `.json`, `.py`, `.md`, `.html`, and `.xml` files (when both files share the same extension), shows a unified line-by-line diff of the first differences
- **`.cdr` file note** — since CorelDRAW files are binary vector archives that can't be diffed as text, the tool suggests rasterizing them to PNG (e.g. via Inkscape CLI or UniConverter) to compare visual output instead

## Requirements

- Python 3.8+
- Tkinter (included with most standard Python installations; on Linux you may need to install it separately, e.g. `sudo apt install python3-tk`)

No external dependencies — the app only uses Python's standard library (`hashlib`, `os`, `tkinter`, `difflib`).

## Usage

```bash
python file_comparer.py
```

1. Click **Browse...** under **File 1** and select the first file.
2. Click **Browse...** under **File 2** and select the second file.
3. Click **Compare Files**.
4. Read the results in the **Analysis Output** panel:
   - File sizes for both files
   - Whether the files are exact binary matches (via SHA-256 hash)
   - If different, a line-by-line diff (for supported text file types) or a note on how to compare `.cdr` files

## How it works

1. **Size check** — compares file sizes for a quick sanity check.
2. **Hash check** — computes a SHA-256 hash of each file's full contents. Matching hashes mean the files are 100% identical at the binary level.
3. **Text diff (if applicable)** — if the hashes differ and both files share a supported text extension, the tool reads them as UTF-8 text and runs Python's `difflib.unified_diff` to show the first 15 lines of differences.

## Limitations

- Text diff only runs when both files share the same, supported extension.
- Non-text binary formats (other than `.cdr`, which gets a specific note) will only get the hash-based identical/different verdict — no detailed diff.
- Large text files are only diffed for their first 15 differing lines in the output.

## License

Feel free to use, modify, and distribute this project as you see fit. Consider adding a license file (e.g. MIT) if you plan to open source it.
