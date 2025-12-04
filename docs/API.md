# 📘 API Functions Reference

This document covers all high-level helper functions provided by RedLight. These functions are designed for quick and simple usage without dealing with classes directly.

## Table of Contents

- [DownloadVideo](#downloadvideo)
- [GetVideoInfo](#getvideoinfo)
- [ListAvailableQualities](#listavailablequalities)

---

## DownloadVideo

Download a video from PornHub Shorts with a single function call.

### Signature

```python
def DownloadVideo(
    url: str,
    output_dir: str = "./downloads",
    quality: str = "best",
    filename: Optional[str] = None,
    keep_ts: bool = False,
    on_progress: Optional[Callable[[int, int], None]] = None
) -> str
### Examples

#### Multi-Site Support (Automatic Detection)

```python
from RedLight import DownloadVideo

# Works with PornHub
video_path = DownloadVideo("https://www.pornhub.com/view_video.php?viewkey=xxxxx")

# Works with Eporner (ultra-fast with aria2c)
video_path = DownloadVideo("https://www.eporner.com/video-xxxxx/title")

# Works with Spankbang (supports 4K!)
video_path = DownloadVideo("https://spankbang.com/xxxxx/video/title")

# Works with XVideos
video_path = DownloadVideo("https://www.xvideos.com/video.xxxxx/title")

# RedLight automatically detects the site and uses the optimal downloader!
print(f"Video saved to: {video_path}")
```

#### Basic Download
```python
from RedLight import DownloadVideo

# Download with default settings (best quality, MP4 format)
video_path = DownloadVideo("https://www.pornhub.com/view_video.php?viewkey=xxxxx")
print(f"Video saved to: {video_path}")
```

#### Custom Quality
```python
# Download 720p quality
video_path = DownloadVideo(
    url="https://www.pornhub.com/view_video.php?viewkey=xxxxx",
    quality="720"
)
```

#### Custom Output Directory and Filename
```python
# Save to specific location with custom name
video_path = DownloadVideo(
    url="https://www.pornhub.com/view_video.php?viewkey=xxxxx",
    output_dir="./my_videos",
    filename="awesome_video.mp4"
)
```

#### Keep Original TS File
```python
# Keep the original .ts file (skip MP4 conversion)
video_path = DownloadVideo(
    url="https://www.pornhub.com/view_video.php?viewkey=xxxxx",
    keep_ts=True
)
# Result: video_path will end with .ts
```

#### Progress Tracking
```python
def progress_callback(downloaded, total):
    percent = (downloaded / total) * 100
    print(f"Progress: {percent:.1f}% ({downloaded}/{total} segments)")

video_path = DownloadVideo(
    url="https://www.pornhub.com/view_video.php?viewkey=xxxxx",
    on_progress=progress_callback
)
```

#### Error Handling
```python
try:
    video_path = DownloadVideo("https://www.pornhub.com/view_video.php?viewkey=xxxxx")
    print(f"Success: {video_path}")
except Exception as e:
    print(f"Download failed: {e}")
```

---

## GetVideoInfo

Extract video metadata without downloading the video.

### Signature

```python
def GetVideoInfo(url: str) -> Dict[str, Union[str, List[int]]]
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | `str` | Video URL |

### Returns

- **Type:** `Dict[str, Union[str, List[int]]]`
- **Description:** Dictionary containing video metadata

**Return Dictionary Structure:**
```python
{
    "title": str,                    # Video title
    "available_qualities": List[int], # Available quality heights (e.g., [720, 1080])
    "video_id": str                   # Extracted video ID
}
```

### Examples

#### Basic Usage
```python
from RedLight import GetVideoInfo

info = GetVideoInfo("https://www.pornhub.com/view_video.php?viewkey=xxxxx")

print(f"Title: {info['title']}")
print(f"Video ID: {info['video_id']}")
print(f"Available Qualities: {info['available_qualities']}")
```

#### Check Available Qualities Before Download
```python
from RedLight import GetVideoInfo, DownloadVideo

# Get info first
info = GetVideoInfo("https://www.pornhub.com/view_video.php?viewkey=xxxxx")

# Check if 1080p is available
if 1080 in info['available_qualities']:
    print("1080p available! Downloading...")
    DownloadVideo(url, quality="1080")
else:
    print("1080p not available. Available qualities:", info['available_qualities'])
    DownloadVideo(url, quality="best")
```

#### Display Video Information
```python
from RedLight import GetVideoInfo

url = "https://www.pornhub.com/view_video.php?viewkey=xxxxx"
info = GetVideoInfo(url)

print("=" * 50)
print(f"Video Title: {info['title']}")
print(f"Video ID: {info['video_id']}")
print(f"Available Qualities: {', '.join(map(str, info['available_qualities']))}p")
print("=" * 50)
```

---

## ListAvailableQualities

Get a list of all available quality options for a video.

### Signature

```python
def ListAvailableQualities(url: str) -> List[int]
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | `str` | Video URL |

### Returns

- **Type:** `List[int]`
- **Description:** List of available quality heights in descending order (e.g., `[1080, 720, 480]`)

### Examples

#### Basic Usage
```python
from RedLight import ListAvailableQualities

qualities = ListAvailableQualities("https://www.pornhub.com/view_video.php?viewkey=xxxxx")
print(f"Available qualities: {qualities}")
# Output: [1080, 720, 480]
```

#### Interactive Quality Selection
```python
from RedLight import ListAvailableQualities, DownloadVideo

url = "https://www.pornhub.com/view_video.php?viewkey=xxxxx"
qualities = ListAvailableQualities(url)

print("Available qualities:")
for i, q in enumerate(qualities, 1):
    print(f"{i}. {q}p")

choice = int(input("Select quality (number): "))
selected_quality = str(qualities[choice - 1])

DownloadVideo(url, quality=selected_quality)
```

#### Automatic Quality Selection
```python
from RedLight import ListAvailableQualities, DownloadVideo

url = "https://www.pornhub.com/view_video.php?viewkey=xxxxx"
qualities = ListAvailableQualities(url)

# Prefer 720p if available, otherwise use best
if 720 in qualities:
    quality = "720"
elif 1080 in qualities:
    quality = "1080"
else:
    quality = "best"

print(f"Downloading in {quality}p...")
DownloadVideo(url, quality=quality)
```

---

## Common Patterns

### Download Multiple Videos
```python
from RedLight import DownloadVideo

urls = [
    "https://www.pornhub.com/view_video.php?viewkey=xxxxx",
    "https://www.pornhub.com/view_video.php?viewkey=yyyyy",
    "https://www.pornhub.com/view_video.php?viewkey=zzzzz"
]

for url in urls:
    try:
        path = DownloadVideo(url)
        print(f"✓ Downloaded: {path}")
    except Exception as e:
        print(f"✗ Failed: {url} - {e}")
```

For more efficient batch downloading, see [BatchDownloader](Classes.md#batchdownloader) in the Classes documentation.

### Error Handling Best Practices
```python
from RedLight import DownloadVideo, GetVideoInfo

url = "https://www.pornhub.com/view_video.php?viewkey=xxxxx"

try:
    # Get info first to validate
    info = GetVideoInfo(url)
    print(f"Downloading: {info['title']}")
    
    # Download
    path = DownloadVideo(url, quality="720")
    print(f"Success! Saved to: {path}")
    
except ValueError as e:
    print(f"Invalid URL or video not found: {e}")
except ConnectionError as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## See Also

- [Classes Documentation](Classes.md) - For class-based API with more control
- [Examples](Examples.md) - More practical examples
- [Advanced Usage](Advanced.md) - Advanced topics and best practices
