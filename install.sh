#!/bin/bash

# PH Shorts Downloader Installation Script
# Supports Linux and macOS

set -e

echo "╔═══════════════════════════════════════════════════════╗"
echo "║          PH Shorts Downloader - Installer            ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    echo "   Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"

# Check pip
echo ""
echo "[2/4] Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed!"
    echo "   Installing pip..."
    python3 -m ensurepip --upgrade
fi
echo "✓ pip is ready"

# Install package
echo ""
echo "[3/4] Installing ph-shorts-dl..."
pip3 install --upgrade pip
pip3 install -e .

echo "✓ Installation complete!"

# Check FFmpeg (optional but recommended)
echo ""
echo "[4/4] Checking FFmpeg (optional)..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠ Warning: FFmpeg is not installed!"
    echo "   Videos will be saved as .ts files without FFmpeg."
    echo "   To install FFmpeg:"
    echo "     • Ubuntu/Debian: sudo apt install ffmpeg"
    echo "     • macOS: brew install ffmpeg"
    echo "     • Arch Linux: sudo pacman -S ffmpeg"
else
    FFMPEG_VERSION=$(ffmpeg -version | head -n1 | awk '{print $3}')
    echo "✓ FFmpeg $FFMPEG_VERSION is installed"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║              Installation Successful! 🎉              ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "Usage:"
echo "  • Interactive mode:  ph-shorts"
echo "  • With URL:          ph-shorts \"VIDEO_URL\""
echo "  • Help:              ph-shorts --help"
echo ""
