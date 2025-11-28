"""
Progress Tracking Example - PHShorts API

This example shows how to track download progress with callbacks.
"""

from PHShorts import VideoDownloader


def progress_callback(downloaded_segments, total_segments):
    """
    Callback function that gets called after each segment is downloaded.
    
    Args:
        downloaded_segments: Number of segments downloaded so far
        total_segments: Total number of segments to download
    """
    percent = (downloaded_segments / total_segments) * 100
    bar_length = 40
    filled = int(bar_length * downloaded_segments / total_segments)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    print(f"\r[{bar}] {percent:.1f}% ({downloaded_segments}/{total_segments} segments)", end="", flush=True)


def main():
    print("=== PHShorts API - Progress Tracking ===\n")
    
    VIDEO_URL = "https://www.pornhub.com/view_video.php?viewkey=your_video_key_here"
    
    # Create downloader with custom output directory
    downloader = VideoDownloader(output_dir="./downloads")
    
    # Get video info
    print("📋 Getting video information...")
    info = downloader.get_info(VIDEO_URL)
    print(f"Title: {info['title']}")
    print(f"Qualities: {info['available_qualities']}\n")
    
    # Download with progress tracking
    print("⬇️ Downloading with progress tracking:\n")
    video_path = downloader.download(
        url=VIDEO_URL,
        quality="best",
        on_progress=progress_callback
    )
    
    print(f"\n\n✅ Download complete!")
    print(f"📁 Saved to: {video_path}")


if __name__ == "__main__":
    main()
