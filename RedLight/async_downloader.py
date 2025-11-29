"""
RedLight Async API - Asynchronous video downloader for bot integration.

This module provides async/await support for integrating RedLight
into async applications like Telegram bots, Discord bots, etc.
"""

import asyncio
from pathlib import Path
from typing import Optional, Callable, Dict, List, Union
from concurrent.futures import ThreadPoolExecutor
from .downloader import CustomHLSDownloader


class AsyncVideoDownloader:
    """
    Asynchronous video downloader for integration with async frameworks.
    
    Perfect for Telegram bots, Discord bots, and other async applications.
    All blocking I/O operations are run in a thread pool executor.
    
    Example (Telegram Bot):
        >>> from RedLight import AsyncVideoDownloader
        >>> 
        >>> async def download_for_user(url: str):
        ...     async with AsyncVideoDownloader() as downloader:
        ...         info = await downloader.get_info(url)
        ...         print(f"Downloading: {info['title']}")
        ...         
        ...         video_path = await downloader.download(url)
        ...         return video_path
    """
    
    def __init__(
        self,
        output_dir: str = "./downloads",
        proxy: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        max_workers: int = 2
    ):
        """
        Initialize AsyncVideoDownloader.
        
        Args:
            output_dir: Directory for downloads
            proxy: HTTP/HTTPS proxy
            headers: Custom HTTP headers
            max_workers: Maximum number of concurrent downloads
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.proxy = proxy
        self.headers = headers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def __aenter__(self):
        """Context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup executor."""
        self.executor.shutdown(wait=True)
    
    async def download(
        self,
        url: str,
        quality: str = "best",
        filename: Optional[str] = None,
        on_progress: Optional[Callable[[int, int], None]] = None
    ) -> str:
        """
        Download a video asynchronously.
        
        Args:
            url: Video URL
            quality: "best", "worst", or specific height
            filename: Custom filename (optional)
            on_progress: Progress callback function
        
        Returns:
            Path to downloaded video
            
        Example:
            >>> async def download_video(url):
            ...     downloader = AsyncVideoDownloader()
            ...     path = await downloader.download(url)
            ...     return path
        """
        loop = asyncio.get_event_loop()
        
        # Run blocking download in thread pool
        result = await loop.run_in_executor(
            self.executor,
            self._sync_download,
            url,
            quality,
            filename,
            on_progress
        )
        
        return result
    
    def _sync_download(
        self,
        url: str,
        quality: str,
        filename: Optional[str],
        on_progress: Optional[Callable]
    ) -> str:
        """Internal sync download function."""
        output_file = None
        if filename:
            output_file = self.output_dir / filename
        
        downloader = CustomHLSDownloader(
            output_name=str(output_file) if output_file else None,
            progress_callback=on_progress,
            proxy=self.proxy,
            headers=self.headers
        )
        
        streams = downloader.extract_video_info(url)
        
        if not output_file and downloader.output_name:
            final_output = self.output_dir / downloader.output_name.name
            downloader.output_name = final_output
        
        # Select stream
        if isinstance(streams, dict):
            quality_keys = sorted([k for k in streams.keys() if isinstance(k, int)], reverse=True)
            if quality_keys:
                m3u8_url = streams[quality_keys[0]]
            else:
                m3u8_url = list(streams.values())[0]
        else:
            m3u8_url = streams
        
        result_path = downloader.download_stream(m3u8_url, preferred_quality=quality)
        return result_path
    
    async def get_info(self, url: str) -> Dict[str, Union[str, List[int]]]:
        """
        Get video information asynchronously.
        
        Args:
            url: Video URL
        
        Returns:
            Dictionary with video metadata
            
        Example:
            >>> async def get_video_title(url):
            ...     downloader = AsyncVideoDownloader()
            ...     info = await downloader.get_info(url)
            ...     return info['title']
        """
        loop = asyncio.get_event_loop()
        
        result = await loop.run_in_executor(
            self.executor,
            self._sync_get_info,
            url
        )
        
        return result
    
    def _sync_get_info(self, url: str) -> Dict:
        """Internal sync info extraction."""
        downloader = CustomHLSDownloader(
            proxy=self.proxy,
            headers=self.headers
        )
        
        streams = downloader.extract_video_info(url)
        video_id = downloader.extract_video_id(url)
        title = downloader.output_name.stem if downloader.output_name else "Unknown"
        
        available_qualities = []
        if isinstance(streams, dict):
            available_qualities = sorted([k for k in streams.keys() if isinstance(k, int)], reverse=True)
        
        return {
            "title": title,
            "available_qualities": available_qualities,
            "video_id": video_id
        }
    
    async def list_qualities(self, url: str) -> List[int]:
        """
        List available qualities asynchronously.
        
        Args:
            url: Video URL
        
        Returns:
            List of quality heights
        """
        info = await self.get_info(url)
        return info["available_qualities"]
    
    def shutdown(self):
        """Manually shutdown the executor."""
        self.executor.shutdown(wait=True)
