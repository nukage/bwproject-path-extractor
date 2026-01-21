# Bitwig Project Path Extractor

A simple Python utility to extract all audio sample file paths from a Bitwig Studio `.bwproject` file.

## Usage

```bash
# Basic extraction
python extract_paths.py "YourProject.bwproject"

# Extraction with file existence check
python extract_paths.py "YourProject.bwproject" --check
```

### Options
- `-o`, `--output`: Specify a custom output filename (default: `extracted_sample_paths.txt`)
- `--check`: Verify if the extracted files exist on the current system (checks absolute and relative paths).
- `--missing`: Specify a filename to save missing paths (default: `missing_sample_paths.txt`).

## How it works
The script scans the binary project file and its internal compressed members for sequences of characters that match common audio file extensions (`.wav`, `.mp3`, `.flac`, etc.) while filtering out non-path metadata. It handles both standard ASCII/UTF-8 and UTF-16LE encoding.
