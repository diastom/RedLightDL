"""
Base classes for site downloaders and search implementations.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Callable, Any


class BaseSiteDownloader(ABC):
    """
    Abstract base class for site-specific video downloaders.
    
    All site downloaders must inherit from this class and implement
    the required methods.
    """
    
    @abstractmethod
    def download(
        self,
        url: str,
        quality: str = "best",
        output_dir: str = "./downloads",
        filename: Optional[str] = None,
        keep_original: bool = False,
        proxy: Optional[str] = None,
        on_progress: Optional[Callable[[int, int], None]] = None
    ) -> str:
        """
        Download a video from the site.
        
        Args:
            url: Video URL
            quality: Quality preference ("best", "worst", or specific like "1080")
            output_dir: Directory to save the video
            filename: Custom filename (optional)
            keep_original: Keep original file format
            proxy: HTTP/HTTPS proxy
            on_progress: Progress callback(completed, total)
        
        Returns:
            Path to downloaded video file
        """
        pass
    
    @abstractmethod
    def get_info(self, url: str) -> Dict[str, Any]:
        """
        Extract video information without downloading.
        
        Args:
            url: Video URL
        
        Returns:
            Dictionary containing:
                - title: Video title
                - available_qualities: List of available quality heights
                - video_id: Video identifier
                - duration: Video duration (optional)
                - thumbnail: Thumbnail URL (optional)
                - site: Site name
        """
        pass
    
    @abstractmethod
    def list_qualities(self, url: str) -> List[int]:
        """
        List available quality options for a video.
        
        Args:
            url: Video URL
        
        Returns:
            List of available quality heights (e.g., [1080, 720, 480])
        """
        pass
    
    @staticmethod
    @abstractmethod
    def is_supported_url(url: str) -> bool:
        """
        Check if this downloader supports the given URL.
        
        Args:
            url: URL to check
        
        Returns:
            True if URL is supported, False otherwise
        """
        pass
    
    @staticmethod
    @abstractmethod
    def get_site_name() -> str:
        """
        Get the site identifier name.
        
        Returns:
            Site name (e.g., "pornhub", "eporner")
        """
        pass


class BaseSiteSearch(ABC):
    """
    Abstract base class for site-specific search implementations.
    
    All search implementations must inherit from this class.
    """
    
    @abstractmethod
    def search(
        self,
        query: str,
        page: int = 1,
        sort_by: str = "relevance",
        duration: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search for videos on the site.
        
        Args:
            query: Search query string
            page: Page number
            sort_by: Sort order (site-specific options)
            duration: Duration filter (site-specific options)
            **kwargs: Additional site-specific filters
        
        Returns:
            List of video dictionaries containing:
                - title: Video title
                - url: Video URL
                - duration: Video duration string
                - views: View count (optional)
                - rating: Rating (optional)
                - thumbnail: Thumbnail URL (optional)
                - site: Site name
        """
        pass
    
    @staticmethod
    @abstractmethod
    def get_site_name() -> str:
        """
        Get the site identifier name.
        
        Returns:
            Site name (e.g., "pornhub", "eporner")
        """
        pass
    
    @abstractmethod
    def get_search_filters(self) -> Dict[str, List[str]]:
        """
        Get available search filters for this site.
        
        Returns:
            Dictionary of filter categories and their options, e.g.:
            {
                "sort_by": ["relevance", "views", "rating", "date"],
                "duration": ["short", "medium", "long"]
            }
        """
        pass
