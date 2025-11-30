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
        """Download a video from the site."""
        pass
    
    @abstractmethod
    def get_info(self, url: str) -> Dict[str, Any]:
        """Extract video information without downloading."""
        pass
    
    @abstractmethod
    def list_qualities(self, url: str) -> List[int]:
        """List available quality options for a video."""
        pass
    
    @staticmethod
    @abstractmethod
    def is_supported_url(url: str) -> bool:
        """Check if this downloader supports the given URL."""
        pass
    
    @staticmethod
    @abstractmethod
    def get_site_name() -> str:
        """Get the site identifier name."""
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
        """Search for videos on the site."""
        pass
    
    @staticmethod
    @abstractmethod
    def get_site_name() -> str:
        """Get the site identifier name."""
        pass
    
    @abstractmethod
    def get_search_filters(self) -> Dict[str, List[str]]:
        """Get available search filters for this site."""
        pass
