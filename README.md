# Universal File Comparison Tool

A small desktop app that tells you whether two files are exactly the same, for any file type. Pick
two files and it compares their sizes and SHA-256 hashes for a bit-for-bit verdict; if they differ
and they are text files, it shows a line-by-line diff of the first differences.

- Python 3.8+ with Tkinter; zero external dependencies (`hashlib`, `difflib`, `os`, `tkinter`)
- Works on any format: documents, images, audio, archives, CorelDRAW `.cdr` and more
- Reads files in 8 KB chunks, so large files don't need to fit in memory for the hash check
- Runs fully offline on Windows, macOS and Linux

## Project layout

```
universal-file-comparison-tool/
├── file_comparer.py     The whole app: Tkinter UI (FileComparerApp) + comparison logic
└── LICENSE              MIT
```

### How it works in one paragraph

`compare_files()` runs three checks in order. First it reports both file sizes. Then it computes a
SHA-256 hash of each file's full contents; identical hashes mean the files are 100% identical and it
stops there. If the hashes differ and both files share a supported text extension, it reads them as
UTF-8 and runs `difflib.unified_diff`, showing the first 15 lines of the diff output. For `.cdr`
files it explains how to compare them visually instead.

## Comparison rules

| Situation | Result |
|---|---|
| Any two files | Size of each file in bytes |
| SHA-256 hashes match | **EXACT BINARY MATCHES (100% identical)** |
| Hashes differ | **DIFFERENT at the binary level** |
| Hashes differ, both files `.txt` `.csv` `.json` `.py` `.md` `.html` or `.xml` with the same extension | Unified diff, first 15 lines |
| Hashes differ, text content still identical (e.g. line endings, encoding) | "Text content is identical despite structural differences" |
| Either file is `.cdr` | Note: rasterize to PNG (Inkscape CLI or UniConverter) and compare the images |
| Other binary formats | Hash verdict only |

## Setup

Requirements: Python 3.8 or newer with Tkinter. Tkinter ships with the python.org installers for
Windows and macOS; on Debian / Ubuntu install it with:

```bash
sudo apt install python3-tk
```

```bash
git clone https://github.com/mdimasprasetyo/universal-file-comparison-tool.git
cd universal-file-comparison-tool
```

## Usage

```bash
python file_comparer.py      # or python3 on macOS / Linux
```

1. Click **Browse...** under **File 1** and pick the first file.
2. Click **Browse...** under **File 2** and pick the second file.
3. Click **Compare Files**.
4. Read the verdict in the **Analysis Output** panel: sizes, the hash verdict, and a diff or a note
   when the files differ.

## Limitations

- The text diff only runs when both files have the same supported extension.
- Only the first 15 lines of the diff output are shown.
- Binary formats other than `.cdr` get the identical / different verdict only, with no detail.

## License

[MIT](LICENSE) © 2026 Muhammad D. Prasetyo
