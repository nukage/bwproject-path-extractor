# Bitwig Project Path Extractor

A simple Python utility to extract all audio sample file paths from a Bitwig Studio `.bwproject` file.

## Usage

```bash
python extract_paths.py "YourProject.bwproject"
```

### Options
- `-o`, `--output`: Specify a custom output filename (default: `extracted_paths.txt`)

## How it works
The script scans the binary project file and its internal compressed members for sequences of characters that match common audio file extensions (`.wav`, `.mp3`, `.flac`, etc.) while filtering out non-path metadata. It handles both standard ASCII/UTF-8 and UTF-16LE encoding.
