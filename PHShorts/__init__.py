"""
PH Shorts Downloader - Download Shorts from PornHub with ease!

A lightweight and powerful alternative to yt-dlp for PornHub Shorts.
Now with programmable API support for building custom scripts and bots!
"""

# Core downloader class (for advanced usage)
from .downloader import CustomHLSDownloader

# High-level API (recommended for most users)
from .api import VideoDownloader, DownloadVideo, GetVideoInfo, ListAvailableQualities

# Async API (for bots and async applications)
from .async_downloader import AsyncVideoDownloader

__version__ = "1.0.6"
__author__ = "PH Shorts DL Team"
__description__ = "Download PornHub Shorts videos with a beautiful CLI interface"

__all__ = [
    # Main API
    "VideoDownloader",
    "DownloadVideo",
    "GetVideoInfo",
    "ListAvailableQualities",
    # Async API
    "AsyncVideoDownloader",
    # Advanced
    "CustomHLSDownloader",
]

