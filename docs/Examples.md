# 💡 Code Examples

Practical, real-world examples for using RedLight in your projects.

## Table of Contents

- [Multi-Site Downloads](#multi-site-downloads)
- [Basic Downloads](#basic-downloads)
- [Batch Processing](#batch-processing)
- [Channel Management](#channel-management)
- [Search and Filter](#search-and-filter)
- [Format Conversion](#format-conversion)
- [Automation Scripts](#automation-scripts)
- [Bot Integration](#bot-integration)
- [Error Handling](#error-handling)

---

## Multi-Site Downloads

RedLight supports 4 major adult content sites: **PornHub**, **Eporner**, **Spankbang**, and **XVideos**.

### Automatic Site Detection

RedLight automatically detects which site you're downloading from:

```python
from RedLight import DownloadVideo

# All use the same simple API!
DownloadVideo("https://www.pornhub.com/view_video.php?viewkey=xxxxx")
DownloadVideo("https://www.eporner.com/video-xxxxx/title")
DownloadVideo("https://spankbang.com/xxxxx/video/title")
DownloadVideo("https://www.xvideos.com/video.xxxxx/title")

# RedLight uses the optimal downloader for each site
```

### Site-Specific Examples

#### PornHub - HLS Streaming

```python
from RedLight import DownloadVideo, GetVideoInfo

# Get video info
url = "https://www.pornhub.com/view_video.php?viewkey=xxxxx"
info = GetVideoInfo(url)

print(f"Title: {info['title']}")
print(f"Qualities: {info['available_qualities']}")  # [240, 480, 720, 1080]

# Download in 1080p
video_path = DownloadVideo(url, quality="1080")
print(f"Downloaded: {video_path}")
```

#### Eporner - Ultra-Fast with aria2c

```python
from RedLight import DownloadVideo

# Eporner uses aria2c for lightning-fast downloads
url = "https://www.eporner.com/video-xxxxx/title"

# Automatically uses aria2c download manager
video_path = DownloadVideo(url)

print(f"Downloaded at maximum speed: {video_path}")
```

#### Spankbang - 4K Support

```python
from RedLight import DownloadVideo, GetVideoInfo

url = "https://spankbang.com/xxxxx/video/title"

# Check if 4K is available
info = GetVideoInfo(url)
print(f"Available qualities: {info['available_qualities']}")

# Download best quality (may be 4K!)
video_path = DownloadVideo(url, quality="best")
print(f"Downloaded: {video_path}")
```

#### XVideos - Intelligent Fallback

```python
from RedLight import DownloadVideo

url = "https://www.xvideos.com/video.xxxxx/title"

# XVideos downloader automatically handles MP4/HLS fallback
video_path = DownloadVideo(url, quality="720")

print(f"Downloaded: {video_path}")
```

### Mixed Site Batch Download

Download from multiple sites in one batch:

```python
from RedLight import BatchDownloader

# Mix URLs from all supported sites
urls = [
    "https://www.pornhub.com/view_video.php?viewkey=xxxxx",
    "https://www.eporner.com/video-xxxxx/title",
    "https://spankbang.com/xxxxx/video/title",
    "https://www.xvideos.com/video.xxxxx/title",
    "https://www.pornhub.com/view_video.php?viewkey=yyyyy",
    "https://www.eporner.com/video-yyyyy/another-title"
]

# RedLight handles all sites automatically
downloader = BatchDownloader(
    concurrent=True,
    max_workers=4,
    quality="720"
)

downloader.AddUrls(urls)
results = downloader.DownloadAll()

print(f"✓ Downloaded {len(results)} videos from multiple sites")
```

### Multi-Site Search

#### Search All Sites Simultaneously

```python
from RedLight import MultiSiteSearch, DownloadVideo

# Search across all 4 sites at once
searcher = MultiSiteSearch()
results = searcher.search_all("your search term")

print(f"Found {len(results)} videos total")

# Group by site
by_site = {}
for video in results:
    site = video['site']
    if site not in by_site:
        by_site[site] = []
    by_site[site].append(video)

# Display results per site
for site, videos in by_site.items():
    print(f"\n{site}: {len(videos)} results")
    for v in videos[:3]:  # Top 3 from each site
        print(f"  - {v['title']}")

# Download top result from each site
for site, videos in by_site.items():
    if videos:
        print(f"\nDownloading from {site}: {videos[0]['title']}")
        DownloadVideo(videos[0]['url'])
```

#### Site-Specific Search

```python
from RedLight import (
    PornHubSearch,
    EpornerSearch,
    SpankBangSearch,
    XVideosSearch
)

query = "search term"

# Search each site separately with site-specific options
ph_search = PornHubSearch()
ph_results = ph_search.search(query, sort_by="toprated", duration="medium")

ep_search = EpornerSearch()
ep_results = ep_search.search(query)

sb_search = SpankBangSearch()
sb_results = sb_search.search(query)

xv_search = XVideosSearch()
xv_results = xv_search.search(query)

print(f"Results:")
print(f"  PornHub: {len(ph_results)}")
print(f"  Eporner: {len(ep_results)}")
print(f"  Spankbang: {len(sb_results)}")
print(f"  XVideos: {len(xv_results)}")
```

### Organized Multi-Site Downloads

Download and organize videos by site:

```python
from RedLight import SiteRegistry, DownloadVideo
from pathlib import Path

def download_and_organize(urls):
    """Download videos and organize by site"""
    
    registry = SiteRegistry()
    results = {"success": {}, "failed": []}
    
    for url in urls:
        # Detect site
        site_name = registry.detect_site(url)
        
        if not site_name:
            results["failed"].append((url, "Unsupported site"))
            continue
        
        # Create site-specific directory
        output_dir = f"./downloads/{site_name}"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            # Download to site folder
            video_path = DownloadVideo(url, output_dir=output_dir)
            
            if site_name not in results["success"]:
                results["success"][site_name] = []
            results["success"][site_name].append(video_path)
            
            print(f"✓ [{site_name}] {Path(video_path).name}")
            
        except Exception as e:
            results["failed"].append((url, str(e)))
            print(f"✗ [{site_name}] Error: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    for site, videos in results["success"].items():
        print(f"{site}: {len(videos)} videos")
    print(f"Failed: {len(results['failed'])}")
    
    return results

# Usage
urls = [
    "https://www.pornhub.com/view_video.php?viewkey=xxxxx",
    "https://www.eporner.com/video-xxxxx/title",
    "https://spankbang.com/xxxxx/video/title",
    "https://www.xvideos.com/video.xxxxx/title"
]

results = download_and_organize(urls)

# Files are organized:
# ./downloads/pornhub/video1.mp4
# ./downloads/eporner/video2.mp4
# ./downloads/spankbang/video3.mp4
# ./downloads/xvideos/video4.mp4
```

### Site-Specific Downloaders (Advanced)

For fine-grained control, use site-specific classes:

```python
from RedLight import (
    PornHubDownloader,
    EpornerDownloader,
    SpankBangDownloader,
    XVideosDownloader
)

# PornHub downloader with custom settings
ph = PornHubDownloader(
    output_dir="./pornhub_videos",
    proxy="http://proxy.example.com:8080"
)
ph_video = ph.download(
    url="https://www.pornhub.com/view_video.php?viewkey=xxxxx",
    quality="1080"
)

# Eporner downloader (ultra-fast with aria2c)
ep = EpornerDownloader(output_dir="./eporner_videos")
ep_video = ep.download(
    url="https://www.eporner.com/video-xxxxx/title"
)

# Spankbang downloader (4K support)
sb = SpankBangDownloader(output_dir="./spankbang_videos")
sb_video = sb.download(
    url="https://spankbang.com/xxxxx/video/title",
    quality="2160"  # 4K
)

# XVideos downloader (intelligent fallback)
xv = XVideosDownloader(output_dir="./xvideos_videos")
xv_video = xv.download(
    url="https://www.xvideos.com/video.xxxxx/title",
    quality="720"
)

print("All sites downloaded with custom configurations!")
```

---

## Basic Downloads

### Simple Download

```python
from RedLight import DownloadVideo

url = "https://www.pornhub.com/view_video.php?viewkey=xxxxx"
video_path = DownloadVideo(url)

print(f"Downloaded: {video_path}")
```

### Download with Custom Settings

```python
from RedLight import DownloadVideo

video_path = DownloadVideo(
    url="https://www.pornhub.com/view_video.php?viewkey=xxxxx",
    output_dir="./videos",
    quality="1080",
    filename="awesome_video.mp4"
)
```

### Progress Bar with Rich

```python
from RedLight import VideoDownloader
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

downloader = VideoDownloader()

with Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TimeRemainingColumn(),
) as progress:
    
    task_id = None
    
    def on_progress(downloaded, total):
        nonlocal task_id
        if task_id is None:
            task_id = progress.add_task("Downloading...", total=total)
        progress.update(task_id, completed=downloaded)
    
    video_path = downloader.download(
        url="https://www.pornhub.com/view_video.php?viewkey=xxxxx",
        on_progress=on_progress
    )

print(f"Downloaded: {video_path}")
```

---

## Batch Processing

### Simple Batch Download

```python
from RedLight import BatchDownloader

urls = [
    "https://www.pornhub.com/view_video.php?viewkey=xxxxx",
    "https://www.pornhub.com/view_video.php?viewkey=yyyyy",
    "https://www.pornhub.com/view_video.php?viewkey=zzzzz"
]

downloader = BatchDownloader(
    concurrent=True,
    max_workers=3,
    quality="720"
)

downloader.AddUrls(urls)
results = downloader.DownloadAll()

print(f"Successfully downloaded {len(results)} videos")
```

### Batch Download with Progress and Error Handling

```python
from RedLight import BatchDownloader
from pathlib import Path

urls = [...]  # Your URLs

downloader = BatchDownloader(concurrent=True, max_workers=3)
downloader.AddUrls(urls)

successful = []
failed = []

def on_complete(url, path):
    successful.append(path)
    print(f"✓ {Path(path).name}")

def on_error(url, error):
    failed.append((url, str(error)))
    print(f"✗ {url[:50]}... - {error}")

results = downloader.DownloadAll(
    on_complete=on_complete,
    on_error=on_error
)

print(f"\nResults:")
print(f"  Successful: {len(successful)}")
print(f"  Failed: {len(failed)}")

if failed:
    print("\nFailed URLs:")
    for url, error in failed:
        print(f"  - {url}")
        print(f"    Error: {error}")
```

### Download URLs from a Text File

```python
from RedLight import BatchDownloader
from pathlib import Path

# Read URLs from file
urls_file = Path("urls.txt")
urls = [line.strip() for line in urls_file.read_text().splitlines() if line.strip()]

print(f"Found {len(urls)} URLs")

# Download
downloader = BatchDownloader(concurrent=True, max_workers=5)
downloader.AddUrls(urls)

results = downloader.DownloadAll()
print(f"Downloaded {len(results)}/{len(urls)} videos")
```

---

## Channel Management

### Download Latest Videos from Channel

```python
from RedLight import PlaylistDownloader, BatchDownloader

# Get latest 10 videos from channel
playlist = PlaylistDownloader()
urls = playlist.GetChannelVideos("pornhub_user", limit=10)

if not urls:
    print("No videos found or channel doesn't exist")
    exit()

print(f"Found {len(urls)} videos")

# Download them
downloader = BatchDownloader(concurrent=True, max_workers=3)
downloader.AddUrls(urls)

results = downloader.DownloadAll()
print(f"Downloaded {len(results)} videos")
```

### Download and Convert Channel Videos

```python
from RedLight import PlaylistDownloader, BatchDownloader, VideoConverter
from pathlib import Path

# Get videos
playlist = PlaylistDownloader()
urls = playlist.GetChannelVideos("channel_name", limit=5)

# Download (keep .ts for conversion)
downloader = BatchDownloader(concurrent=True, keep_ts=True)
downloader.AddUrls(urls)

video_paths = []

def on_complete(url, path):
    video_paths.append(path)
    print(f"Downloaded: {Path(path).name}")

downloader.DownloadAll(on_complete=on_complete)

# Convert to WebM and compress
converter = VideoConverter()

for video_path in video_paths:
    print(f"Converting: {Path(video_path).name}")
    
    webm_path = converter.Convert(
       input_file=video_path,
        output_format="webm",
        compress_quality=80
    )
    
    print(f"Converted: {Path(webm_path).name}")
    
    # Delete original .ts file
    Path(video_path).unlink()
```

---

## Search and Filter

### Search and Download Top Results

```python
from RedLight import PornHubSearch, DownloadVideo

# Search for videos
searcher = PornHubSearch()
results = searcher.search(
    query="query",
    sort_by="toprated",
    duration="medium"
)

print(f"Found {len(results)} videos")

# Download top 5
for i, video in enumerate(results[:5], 1):
    print(f"\n[{i}/5] {video['title']}")
    print(f"  Duration: {video['duration']}")
    print(f"  Views: {video['views']}")
    
    try:
        path = DownloadVideo(video['url'], quality="720")
        print(f"  ✓ Downloaded: {path}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
```

### Interactive Search and Download

```python
from RedLight import PornHubSearch, DownloadVideo

searcher = PornHubSearch()

while True:
    query = input("\nEnter search query (or 'quit'): ")
    if query.lower() == 'quit':
        break
    
    results = searcher.search(query, sort_by="mostviewed")
    
    if not results:
        print("No results found")
        continue
    
    print("\nResults:")
    for i, video in enumerate(results[:10], 1):
        print(f"{i}. {video['title']} ({video['duration']})")
    
    choice = input("\nEnter number to download (or 'skip'): ")
    
    if choice.isdigit() and 1 <= int(choice) <= len(results):
        video = results[int(choice) - 1]
        print(f"\nDownloading: {video['title']}")
        
        try:
            path = DownloadVideo(video['url'])
            print(f"✓ Saved to: {path}")
        except Exception as e:
            print(f"✗ Error: {e}")
```

---

## Format Conversion

### Download and Convert to MP3

```python
from RedLight import DownloadVideo, VideoConverter

# Download video
print("Downloading...")
video_path = DownloadVideo(url, keep_ts=True)

# Extract audio
print("Extracting audio...")
converter = VideoConverter()
audio_path = converter.Convert(
    input_file=video_path,
    audio_only=True
)

print(f"Audio saved: {audio_path}")

# Delete video file
from pathlib import Path
Path(video_path).unlink()
```

### Batch Convert Videos

```python
from RedLight import VideoConverter
from pathlib import Path

converter = VideoConverter()

# Get all MP4 files in directory
video_dir = Path("./downloads")
mp4_files = list(video_dir.glob("*.mp4"))

print(f"Found {len(mp4_files)} MP4 files")

# Convert all to WebM with compression
for video_file in mp4_files:
    print(f"Converting: {video_file.name}")
    
    webm_path = converter.Convert(
        input_file=str(video_file),
        output_format="webm",
        compress_quality=75
    )
    
    print(f"  ✓ {Path(webm_path).name}")
```

### Smart Compression

```python
from RedLight import VideoConverter
from pathlib import Path

def compress_if_large(video_path, max_size_mb=100):
    """Compress video if larger than max_size_mb"""
    
    file_size = Path(video_path).stat().st_size / (1024 * 1024)  # MB
    
    if file_size > max_size_mb:
        print(f"File size: {file_size:.1f}MB (compressing...)")
        
        converter = VideoConverter()
        compressed = converter.Compress(
            input_file=video_path,
            quality=70
        )
        
        new_size = Path(compressed).stat().st_size / (1024 * 1024)
        saved = file_size - new_size
        
        print(f"Compressed: {new_size:.1f}MB (saved {saved:.1f}MB)")
        return compressed
    else:
        print(f"File size: {file_size:.1f}MB (no compression needed)")
        return video_path

# Usage
from RedLight import DownloadVideo

video_path = DownloadVideo(url)
final_path = compress_if_large(video_path, max_size_mb=50)
```

---

## Automation Scripts

### Daily Channel Scraper

```python
import schedule
import time
from RedLight import PlaylistDownloader, BatchDownloader
from datetime import datetime

def download_daily():
    """Download latest videos from channel daily"""
    
    print(f"\n[{datetime.now()}] Starting daily download...")
    
    # Get latest 5 videos
    playlist = PlaylistDownloader()
    urls = playlist.GetChannelVideos("channel_name", limit=5)
    
    if not urls:
        print("No new videos found")
        return
    
    print(f"Found {len(urls)} videos")
    
    # Download
    downloader = BatchDownloader(
        output_dir=f"./downloads/{datetime.now().strftime('%Y-%m-%d')}",
        concurrent=True
    )
    downloader.AddUrls(urls)
    
    results = downloader.DownloadAll()
    print(f"Downloaded {len(results)} videos")

# Schedule daily at 2 AM
schedule.every().day.at("02:00").do(download_daily)

print("Daily scraper started. Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Bulk Channel Downloader

```python
from RedLight import PlaylistDownloader, BatchDownloader

channels = [
    "channel1",
    "channel2",
    "channel3"
]

playlist = PlaylistDownloader()
all_urls = []

# Collect URLs from all channels
for channel in channels:
    print(f"Scanning: {channel}")
    urls = playlist.GetChannelVideos(channel, limit=10)
    all_urls.extend(urls)
    print(f"  Found: {len(urls)} videos")

print(f"\nTotal videos: {len(all_urls)}")

# Download all
downloader = BatchDownloader(concurrent=True, max_workers=5)
downloader.AddUrls(all_urls)

results = downloader.DownloadAll()
print(f"\nDownloaded {len(results)}/{len(all_urls)} videos")
```

---

## Bot Integration

### Telegram Bot Example

```python
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from RedLight import AsyncVideoDownloader

async def download_video(update: Update, context):
    """Handle /download command"""
    
    url = context.args[0] if context.args else None
    
    if not url:
        await update.message.reply_text("Usage: /download <URL>")
        return
    
    await update.message.reply_text("Downloading video...")
    
    try:
        async with AsyncVideoDownloader() as downloader:
            # Get info
            info = await downloader.get_info(url)
            await update.message.reply_text(f"Title: {info['title']}")
            
            # Download
            video_path = await downloader.download(url, quality="720")
            
            # Send video
            with open(video_path, 'rb') as video:
                await update.message.reply_video(video)
            
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Create bot
app = Application.builder().token("YOUR_BOT_TOKEN").build()

# Add handlers
app.add_handler(CommandHandler("download", download_video))

# Start bot
app.run_polling()
```

### Discord Bot Example

```python
import discord
from discord.ext import commands
from RedLight import AsyncVideoDownloader
import asyncio

bot = commands.Bot(command_prefix='!')

@bot.command()
async def download(ctx, url: str):
    """Download PornHub video"""
    
    await ctx.send("Downloading...")
    
    try:
        async with AsyncVideoDownloader() as downloader:
            # Get info
            info = await downloader.get_info(url)
            await ctx.send(f"**Title:** {info['title']}")
            
            # Download
            video_path = await downloader.download(url)
            
            # Send file
            if os.path.getsize(video_path) < 8 * 1024 * 1024:  # 8MB limit
                await ctx.send(file=discord.File(video_path))
            else:
                await ctx.send("Video too large to send on Discord")
                
    except Exception as e:
        await ctx.send(f"Error: {e}")

bot.run("YOUR_BOT_TOKEN")
```

---

## Error Handling

### Robust Download with Retry

```python
from RedLight import DownloadVideo
import time

def download_with_retry(url, max_retries=3):
    """Download with automatic retry on failure"""
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}")
            video_path = DownloadVideo(url)
            print(f"Success: {video_path}")
            return video_path
            
        except ConnectionError as e:
            print(f"Network error: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print("Max retries reached")
                raise
                
        except ValueError as e:
            print(f"Invalid URL: {e}")
            raise  # Don't retry on invalid URL
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

# Usage
url = "https://www.pornhub.com/view_video.php?viewkey=xxxxx"
video_path = download_with_retry(url)
```

### Batch Download with Detailed Logging

```python
from RedLight import BatchDownloader
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename=f'download_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

urls = [...]  # Your URLs

downloader = BatchDownloader(concurrent=True)
downloader.AddUrls(urls)

def on_complete(url, path):
    logging.info(f"SUCCESS: {url} -> {path}")

def on_error(url, error):
    logging.error(f"FAILED: {url} - {error}")

results = downloader.DownloadAll(
    on_complete=on_complete,
    on_error=on_error
)

logging.info(f"Batch complete: {len(results)}/{len(urls)} successful")
```

---

## See Also

- [Quick Start](QuickStart.md) - Get started quickly
- [API Reference](API.md) - API function documentation
- [Classes](Classes.md) - Class documentation
- [Advanced Usage](Advanced.md) - Advanced topics
