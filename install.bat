@echo off
REM PH Shorts Downloader Installation Script for Windows

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║          PH Shorts Downloader - Installer            ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

REM Check Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed!
    echo    Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

python --version
echo ✓ Python is ready
echo.

REM Check pip
echo [2/4] Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: pip is not installed!
    echo    Installing pip...
    python -m ensurepip --upgrade
)
echo ✓ pip is ready
echo.

REM Install package
echo [3/4] Installing ph-shorts-dl...
python -m pip install --upgrade pip
python -m pip install -e .

if errorlevel 1 (
    echo ❌ Installation failed!
    pause
    exit /b 1
)

echo ✓ Installation complete!
echo.

REM Check FFmpeg (optional)
echo [4/4] Checking FFmpeg (optional)...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠ Warning: FFmpeg is not installed!
    echo    Videos will be saved as .ts files without FFmpeg.
    echo    Download FFmpeg from: https://ffmpeg.org/download.html
) else (
    ffmpeg -version | findstr "ffmpeg version"
    echo ✓ FFmpeg is installed
)

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║              Installation Successful! 🎉              ║
echo ╚═══════════════════════════════════════════════════════╝
echo.
echo Usage:
echo   • Interactive mode:  ph-shorts
echo   • With URL:          ph-shorts "VIDEO_URL"
echo   • Help:              ph-shorts --help
echo.
pause
