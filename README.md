# Bitwig Project Path Extractor

A utility to extract and audit audio sample file paths from Bitwig Studio `.bwproject` files.

## Features

- **GUI Interface**: Modern, easy-to-use desktop application.
- **File Picker**: Use the file picker to select your `.bwproject` file to start auditing.
- **Existence Check**: Scans your disk to verify if samples are actually where the project thinks they are.
- **Search & Filter**: Quickly find specific samples or filter by status (Found/Missing).
- **Multiple Exports**:
  - Direct UI view with status icons.
  - Plain Text (`.txt`) list of all paths.
  - Styled HTML Report for easy sharing and documentation.
- **Cross-Platform**: Supports Windows, macOS, and Linux.

## Installation & Usage

### Windows
1. Double-click `setup_windows.bat` (only needed for first-time setup).
2. Run `run_gui.bat` to launch the application.

### macOS / Linux
1. Run `sh setup_mac.sh` in your terminal.
2. Run `sh run_gui.sh` to launch the application.

## Command Line Usage (Optional)
If you prefer the command line, you can still use the core script directly:
```bash
python extract_paths.py "path/to/your/project.bwproject"
```

## Requirements
- Python 3.8 or higher.
- Dependencies are automatically handled by the setup scripts.
