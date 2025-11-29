"""
Eporner.com downloader and search implementation.
"""

import requests
import re
import json
import subprocess
import shutil
import concurrent.futures
import time
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from bs4 import BeautifulSoup

from .base import BaseSiteDownloader, BaseSiteSearch


class EpornerDownloader(BaseSiteDownloader):
    """
    Eporner.com video downloader.
    
    Uses direct MP4 downloads with aria2c or multi-threaded Python downloader.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.eporner.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        self.session.headers.update(self.headers)
    
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
        """Download video from Eporner."""
        # Extract info and get download links
        title, links = self._extract_info(url)
        
        # Select quality
        selected_quality = self._select_quality(links, quality)
        download_url = links[selected_quality]
        
        # Resolve final URL
        final_url = self._get_final_url(download_url)
        
        # Prepare output path
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if filename:
            output_file = output_path / filename
        else:
            # Clean quality name for filename
            clean_quality = selected_quality.replace(' ', '').replace('(', '').replace(')', '')
            output_file = output_path / f"{self._sanitize_filename(title)}_{clean_quality}.mp4"
        
        # Download with aria2c or Python downloader
        self._download_manager(final_url, str(output_file), on_progress)
        
        return str(output_file)
    
    def get_info(self, url: str) -> Dict[str, Any]:
        """Extract video information."""
        title, links = self._extract_info(url)
        
        # Extract available qualities
        available_qualities = []
        for quality_str in links.keys():
            # Extract numeric quality
            match = re.search(r'(\d{3,4})p', quality_str)
            if match:
                available_qualities.append(int(match.group(1)))
        
        # Get video ID
        video_id = self._extract_video_id(url)
        
        return {
            "title": title,
            "available_qualities": sorted(available_qualities, reverse=True),
            "video_id": video_id,
            "site": "eporner"
        }
    
    def list_qualities(self, url: str) -> List[int]:
        """List available quality options."""
        info = self.get_info(url)
        return info["available_qualities"]
    
    @staticmethod
    def is_supported_url(url: str) -> bool:
        """Check if URL is from Eporner."""
        return "eporner.com" in url.lower()
    
    @staticmethod
    def get_site_name() -> str:
        """Return site identifier."""
        return "eporner"
    
    def _extract_info(self, url: str) -> tuple[str, Dict[str, str]]:
        """Extract video title and download links."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            html_content = response.text
            
            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', html_content)
            title = "eporner_video"
            if title_match:
                title = title_match.group(1).replace(" - EPORNER", "").strip()
                title = re.sub(r'[\\/*?:"<>|]', "", title)
            
            download_links = {}
            
            # Method 1: Extract from JSON-LD
            json_ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html_content, re.DOTALL)
            if json_ld_match:
                try:
                    data = json.loads(json_ld_match.group(1))
                    if 'contentUrl' in data:
                        download_links['Best (JSON)'] = data['contentUrl']
                except json.JSONDecodeError:
                    pass
            
            # Method 2: Extract dload links
            matches = re.findall(r'href="(/dload/[^"]+)"', html_content)
            
            for link in matches:
                link = link.replace("&amp;", "&")
                full_link = "https://www.eporner.com" + link
                
                # Detect quality
                quality = "Unknown"
                if "2160p" in link: quality = "2160p"
                elif "1440p" in link: quality = "1440p"
                elif "1080p" in link: quality = "1080p"
                elif "720p" in link: quality = "720p"
                elif "480p" in link: quality = "480p"
                elif "360p" in link: quality = "360p"
                elif "240p" in link: quality = "240p"
                
                # Add AV1 label if applicable
                if "av1" in link.lower():
                    quality += " (AV1)"
                
                if quality not in download_links:
                    download_links[quality] = full_link
            
            # Clean up duplicate JSON link
            if 'Best (JSON)' in download_links:
                best_url = download_links['Best (JSON)']
                is_duplicate = any(v == best_url for k, v in download_links.items() if k != 'Best (JSON)')
                
                if is_duplicate:
                    del download_links['Best (JSON)']
                else:
                    # Try to identify quality from URL
                    match_res = re.search(r'(\d{3,4})p', best_url) or re.search(r'/(\d{3,4})/', best_url)
                    if match_res:
                        res = match_res.group(1) + "p (Source)"
                        if res not in download_links:
                            download_links[res] = best_url
                            del download_links['Best (JSON)']
            
            if not download_links:
                raise ValueError("No download links found")
            
            return title, download_links
            
        except Exception as e:
            raise RuntimeError(f"Failed to extract video info: {e}")
    
    def _select_quality(self, links: Dict[str, str], quality: str) -> str:
        """Select best matching quality from available links."""
        # Sort qualities: non-AV1 first, then by resolution
        def sort_key(k):
            is_av1 = 1 if "(AV1)" in k else 0
            res = 0
            match = re.search(r'(\d+)p', k)
            if match:
                res = int(match.group(1))
            return (is_av1, -res)
        
        sorted_keys = sorted(links.keys(), key=sort_key)
        
        if quality == 'best':
            return sorted_keys[0]
        elif quality == 'worst':
            return sorted_keys[-1]
        else:
            # Try to match specific quality
            try:
                req_q = int(quality)
                for key in sorted_keys:
                    if f"{req_q}p" in key:
                        return key
                # Fallback to closest
                return sorted_keys[0]
            except ValueError:
                return sorted_keys[0]
    
    def _get_final_url(self, dload_url: str) -> str:
        """Resolve final download URL."""
        try:
            if "gvideo" in dload_url:
                return dload_url
            response = self.session.head(dload_url, allow_redirects=True)
            return response.url
        except:
            return dload_url
    
    def _download_manager(self, url: str, filename: str, on_progress: Optional[Callable] = None):
        """Download using aria2c or Python downloader."""
        if shutil.which("aria2c"):
            success = self._download_with_aria2c(url, filename)
            if success:
                return
        
        # Fallback to Python multi-threaded downloader
        self._download_python_multithreaded(url, filename, on_progress)
    
    def _download_with_aria2c(self, url: str, filename: str) -> bool:
        """Download using aria2c."""
        cmd = [
            'aria2c',
            url,
            '-o', filename,
            '-x', '16',
            '-s', '16',
            '-j', '1',
            '--user-agent', self.headers['User-Agent'],
            '--referer', self.headers['Referer'],
            '--summary-interval=0',
            '--file-allocation=none',
            '--console-log-level=warn',
            '--download-result=hide'
        ]
        
        try:
            subprocess.run(cmd, check=True)
            return True
        except:
            return False
    
    def _download_python_multithreaded(self, url: str, filename: str, on_progress: Optional[Callable], num_threads: int = 16):
        """Download using Python multi-threading."""
        try:
            head = self.session.head(url, allow_redirects=True)
            if 'content-length' not in head.headers:
                self._download_single(url, filename)
                return
            
            file_size = int(head.headers.get('content-length', 0))
        except:
            self._download_single(url, filename)
            return
        
        chunk_size = file_size // num_threads
        ranges = []
        for i in range(num_threads):
            start = i * chunk_size
            end = start + chunk_size - 1
            if i == num_threads - 1:
                end = file_size - 1
            ranges.append((start, end, i))
        
        with open(filename, 'wb') as f:
            f.truncate(file_size)
        
        completed = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {
                executor.submit(self._download_chunk, url, filename, start, end, i): i
                for start, end, i in ranges
            }
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    downloaded_bytes = future.result()
                    completed += downloaded_bytes
                    if on_progress:
                        on_progress(completed, file_size)
                except Exception:
                    pass
    
    def _download_chunk(self, url: str, filename: str, start: int, end: int, index: int) -> int:
        """Download a file chunk."""
        headers = self.session.headers.copy()
        headers['Range'] = f'bytes={start}-{end}'
        
        response = self.session.get(url, headers=headers, stream=True, timeout=20)
        response.raise_for_status()
        
        with open(filename, 'r+b') as f:
            f.seek(start)
            total_written = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    total_written += len(chunk)
        return total_written
    
    def _download_single(self, url: str, filename: str):
        """Single-threaded download fallback."""
        with self.session.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    
    def _sanitize_filename(self, title: str) -> str:
        """Clean filename for filesystem."""
        return re.sub(r'[\\/*?:"<>|]', "", title)
    
    def _extract_video_id(self, url: str) -> str:
        """Extract video ID from URL."""
        match = re.search(r'/video-([^/]+)/', url)
        if match:
            return match.group(1)
        return "unknown"


class EpornerSearch(BaseSiteSearch):
    """
    Eporner.com search implementation using web scraping.
    """
    
    def __init__(self):
        self.base_url = "https://www.eporner.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
    
    def search(
        self,
        query: str,
        page: int = 1,
        sort_by: str = "relevance",
        duration: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search Eporner for videos."""
        try:
            # Build search URL
            search_url = f"{self.base_url}/search/{query}/"
            
            # Add page parameter
            if page > 1:
                search_url += f"{page}/"
            
            # Add sort parameter
            params = {}
            if sort_by == "views":
                params['order'] = 'top-weekly'
            elif sort_by == "rating":
                params['order'] = 'top-rated'
            elif sort_by == "date":
                params['order'] = 'latest-updates'
            
            # Fetch search results
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse results
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Find video containers (adjust selectors based on actual HTML structure)
            video_items = soup.find_all('div', class_='mb')
            
            for item in video_items[:50]:  # Limit to 50 results
                try:
                    # Extract video link
                    link_elem = item.find('a', href=True)
                    if not link_elem:
                        continue
                    
                    video_url = link_elem['href']
                    if not video_url.startswith('http'):
                        video_url = self.base_url + video_url
                    
                    # Extract title
                    title_elem = link_elem.get('title') or link_elem.text.strip()
                    
                    # Extract thumbnail
                    img_elem = item.find('img')
                    thumbnail = img_elem.get('src', '') if img_elem else ''
                    
                    # Extract duration
                    duration_elem = item.find('div', class_='mbtim')
                    duration_str = duration_elem.text.strip() if duration_elem else ''
                    
                    # Extract views (if available)
                    views_elem = item.find('div', class_='mbvie')
                    views_str = views_elem.text.strip() if views_elem else ''
                    
                    results.append({
                        "title": title_elem if isinstance(title_elem, str) else title_elem,
                        "url": video_url,
                        "duration": duration_str,
                        "views": views_str,
                        "thumbnail": thumbnail,
                        "site": "eporner"
                    })
                except Exception:
                    continue
            
            return results
            
        except Exception as e:
            return []
    
    @staticmethod
    def get_site_name() -> str:
        """Return site identifier."""
        return "eporner"
    
    def get_search_filters(self) -> Dict[str, List[str]]:
        """Get available search filters."""
        return {
            "sort_by": ["relevance", "views", "rating", "date"],
            "duration": []  # Eporner doesn't have duration filters in basic search
        }
