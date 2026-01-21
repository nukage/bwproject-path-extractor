@echo off

if not exist "venv" (
    echo [INFO] Virtual environment not found. Running setup...
    call setup_windows.bat
)

if exist "venv" (
    echo [INFO] Starting Bitwig Path Extractor...
    .\venv\Scripts\python.exe gui.py
) else (
    echo [ERROR] Setup failed to create venv.
)
pause
