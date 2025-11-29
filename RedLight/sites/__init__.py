"""
RedLight Sites Module - Multi-site support infrastructure.

This module provides the base architecture for supporting multiple adult content sites.
"""

from .base import BaseSiteDownloader, BaseSiteSearch
from .registry import SiteRegistry

# Import site implementations
from .pornhub import PornHubDownloader, PornHubSearch
from .eporner import EpornerDownloader, EpornerSearch

# Initialize registry and register all sites
_registry = SiteRegistry()

# Register PornHub
_registry.register_site(
    name="pornhub",
    downloader_class=PornHubDownloader,
    search_class=PornHubSearch
)

# Register Eporner
_registry.register_site(
    name="eporner",
    downloader_class=EpornerDownloader,
    search_class=EpornerSearch
)

__all__ = [
    "BaseSiteDownloader",
    "BaseSiteSearch",
    "SiteRegistry",
    "PornHubDownloader",
    "PornHubSearch",
    "EpornerDownloader",
    "EpornerSearch",
]
