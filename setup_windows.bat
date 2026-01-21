@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo Bitwig Path Extractor Setup
echo ==========================================

:: Check for Python
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python not found. Please install it from python.org and add to PATH.
    pause
    exit /b 1
)

:: Handle existing venv
if exist "venv" (
    echo Cleaning old environment...
    taskkill /F /IM python.exe /T >nul 2>&1
    rmdir /s /q "venv" >nul 2>&1
    if exist "venv" (
        echo.
        echo [ERROR] Could not delete 'venv' folder.
        echo Please close VS Code, any open terminals, or the GUI and try again.
        pause
        exit /b 1
    )
)

echo Creating fresh virtual environment...
python -m venv venv
if !errorlevel! neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

echo Installing dependencies...
:: Use relative path to avoid the '!' expansion bug
.\venv\Scripts\python.exe -m pip install flet==0.25.2

if !errorlevel! neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Setup complete successfully!
echo You can now run the app using "run_gui.bat"
echo ==========================================
pause
