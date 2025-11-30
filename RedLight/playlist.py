"""
Playlist/Channel Downloader Module

This module provides functionality to scrape and download videos from
PornHub channels, users, and playlists.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import re
from urllib.parse import urljoin

class PlaylistDownloader:
    """
    Download videos from a channel, user profile, or playlist.
    
    Example:
        >>> downloader = PlaylistDownloader()
        >>> videos = downloader.GetChannelVideos("pornhub_user", limit=10)
        >>> print(f"Found {len(videos)} videos")
    """
    
    def __init__(self):
        self.base_url = "https://www.pornhub.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        })
    
    def GetChannelVideos(self, target: str, limit: int = 10) -> List[str]:
        """Get video URLs from a channel or user."""
        if "eporner.com" in target:
            return self._get_eporner_videos(target, limit)
        return self._get_pornhub_videos(target, limit)

    def _get_eporner_videos(self, target: str, limit: int) -> List[str]:
        """Scrape videos from an Eporner channel."""
        videos = []
        page = 1
        
        # Ensure URL is correct
        if not target.startswith("http"):
            # Assume it's a channel name if not a URL
            target = f"https://www.eporner.com/channel/{target}/"
            
        print(f"Scanning Eporner: {target}")
        
        while len(videos) < limit:
            try:
                # Eporner pagination: /channel/name/2/
                if page > 1:
                    if target.endswith('/'):
                        page_url = f"{target}{page}/"
                    else:
                        page_url = f"{target}/{page}/"
                else:
                    page_url = target
                    
                response = self.session.get(page_url, timeout=10)
                if response.status_code == 404:
                    break
                
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                found_on_page = 0
                
                # Find video containers
                for item in soup.find_all('div', class_='mb'):
                    link = item.find('a', href=True)
                    if link:
                        href = link['href']
                        if '/video-' in href or '/video/' in href:
                            full_url = urljoin("https://www.eporner.com", href)
                            if full_url not in videos:
                                videos.append(full_url)
                                found_on_page += 1
                                if len(videos) >= limit:
                                    break
                
                if found_on_page == 0:
                    break
                    
                page += 1
                
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                break
                
        return videos[:limit]

    def _get_pornhub_videos(self, target: str, limit: int = 10) -> List[str]:
        """Get video URLs from a channel or user."""
        # Determine URL
        if target.startswith("http"):
            url = target
            if "/videos" not in url and "pornhub.com" in url:
                url = f"{url.rstrip('/')}/videos"
        else:
            # Try user first, then channel
            # Note: This is a simplification. Ideally we'd check if it exists.
            # Defaulting to users/USERNAME/videos
            url = f"{self.base_url}/users/{target}/videos"
            
        print(f"Scanning: {url}")
        
        videos = []
        page = 1
        
        while len(videos) < limit:
            try:
                page_url = f"{url}?page={page}"
                response = self.session.get(page_url, timeout=10)
                
                if response.status_code == 404:
                    # If user not found, try channel format
                    if page == 1 and "/users/" in url:
                        url = url.replace("/users/", "/channels/")
                        print(f"User not found, trying channel: {url}")
                        continue
                    break
                
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find video links
                # Common selectors for PH video lists
                found_on_page = 0
                
                # Selector 1: Standard video blocks
                for link in soup.select('ul.videos.row-5-thumbs li.pcVideoListItem a'):
                    href = link.get('href')
                    if href and 'view_video.php' in href:
                        full_url = urljoin(self.base_url, href)
                        if full_url not in videos:
                            videos.append(full_url)
                            found_on_page += 1
                            if len(videos) >= limit:
                                break
                
                # Selector 2: Channel video blocks (sometimes different)
                if found_on_page == 0:
                    for link in soup.select('div.videoBox a'):
                        href = link.get('href')
                        if href and 'view_video.php' in href:
                            full_url = urljoin(self.base_url, href)
                            if full_url not in videos:
                                videos.append(full_url)
                                found_on_page += 1
                                if len(videos) >= limit:
                                    break
                
                if found_on_page == 0:
                    break
                    
                page += 1
                
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                break
                
        return videos[:limit]
