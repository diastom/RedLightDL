"""
RedLight API - Simple helper functions for quick usage.

This module provides high-level functions for downloading videos
and extracting metadata without dealing with classes directly.
Supports multiple adult content sites with automatic detection.
"""

from pathlib import Path
from typing import Optional, Callable, Dict, List, Union
from .downloader import CustomHLSDownloader
from .sites import SiteRegistry


def DownloadVideo(
    url: str,
    output_dir: str = "./downloads",
    quality: str = "best",
    filename: Optional[str] = None,
    keep_ts: bool = False,
    proxy: Optional[str] = None,
    on_progress: Optional[Callable[[int, int], None]] = None
) -> str:
    """
    Download a video from any supported site (auto-detected).
    
    Args:
        url: Video URL from any supported site
        output_dir: Directory to save the video (default: "./downloads")
        quality: Video quality - "best", "worst", or specific height like "720"
        filename: Custom filename (optional, auto-detected from video title if not provided)
        keep_ts: If True, keep original file (for HLS: .ts, for MP4: original format)
        proxy: HTTP/HTTPS proxy (optional)
        on_progress: Callback function (downloaded, total) for progress tracking
    
    Returns:
        Path to the downloaded video file
        
    Raises:
        ValueError: If URL is from an unsupported site
        
    Example:
        >>> from RedLight import DownloadVideo
        >>> # Works with PornHub
        >>> video_path = DownloadVideo("https://pornhub.com/...")
        >>> # Also works with Eporner
        >>> video_path = DownloadVideo("https://eporner.com/...")
    """
    # Get appropriate downloader for the URL
    registry = SiteRegistry()
    downloader = registry.get_downloader_for_url(url)
    
    if not downloader:
        raise ValueError(f"Unsupported URL. Supported sites: {', '.join([s['name'] for s in registry.get_all_sites()])}")
    
    # Download using site-specific downloader
    return downloader.download(
        url=url,
        quality=quality,
        output_dir=output_dir,
        filename=filename,
        keep_original=keep_ts,
        proxy=proxy,
        on_progress=on_progress
    )


def GetVideoInfo(url: str) -> Dict[str, Union[str, List[int]]]:
    """
    Get video metadata without downloading (supports all sites).
    
    Args:
        url: Video URL from any supported site
    
    Returns:
        Dictionary containing:
            - title: Video title
            - available_qualities: List of available quality heights
            - video_id: Extracted video ID
            - site: Site name (e.g., "pornhub", "eporner")
            
    Raises:
        ValueError: If URL is from an unsupported site
            
    Example:
        >>> from RedLight import GetVideoInfo
        >>> info = GetVideoInfo("https://pornhub.com/...")
        >>> print(f"Title: {info['title']}")
        >>> print(f"Site: {info['site']}")
    """
    registry = SiteRegistry()
    downloader = registry.get_downloader_for_url(url)
    
    if not downloader:
        raise ValueError(f"Unsupported URL. Supported sites: {', '.join([s['name'] for s in registry.get_all_sites()])}")
    
    return downloader.get_info(url)


def ListAvailableQualities(url: str) -> List[int]:
    """
    List all available quality options for a video (supports all sites).
    
    Args:
        url: Video URL from any supported site
    
    Returns:
        List of available quality heights (e.g., [1080, 720, 480])
        
    Example:
        >>> from RedLight import ListAvailableQualities
        >>> qualities = ListAvailableQualities("https://eporner.com/...")
        >>> print(f"Available: {qualities}")
    """
    info = GetVideoInfo(url)
    return info["available_qualities"]


class VideoDownloader:
    """
    Main class for programmatic video downloads with full control.
    
    This class provides a clean API for developers who want more control
    over the download process, including progress tracking and quality selection.
    
    Example:
        >>> from RedLight import VideoDownloader
        >>> 
        >>> def progress(downloaded, total):
        ...     percent = (downloaded / total) * 100
        ...     print(f"Progress: {percent:.1f}%")
        >>> 
        >>> downloader = VideoDownloader(output_dir="./videos")
        >>> video_path = downloader.download(
        ...     url="https://pornhub.com/...",
        ...     quality="720",
        ...     on_progress=progress
        ... )
    """
    
    def __init__(
        self,
        output_dir: str = "./downloads",
        proxy: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize VideoDownloader.
        
        Args:
            output_dir: Default directory for downloads
            proxy: HTTP/HTTPS proxy (e.g., "http://127.0.0.1:8080")
            headers: Custom HTTP headers
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.proxy = proxy
        self.headers = headers
    
    def download(
        self,
        url: str,
        quality: str = "best",
        filename: Optional[str] = None,
        keep_ts: bool = False,
        on_progress: Optional[Callable[[int, int], None]] = None
    ) -> str:
        """Download a video."""
        return DownloadVideo(
            url=url,
            output_dir=str(self.output_dir),
            quality=quality,
            filename=filename,
            keep_ts=keep_ts,
            on_progress=on_progress
        )
    
    def get_info(self, url: str) -> Dict[str, Union[str, List[int]]]:
        """Get video information without downloading."""
        return GetVideoInfo(url)
    
    def list_qualities(self, url: str) -> List[int]:
        """List available quality options."""
        return ListAvailableQualities(url)
