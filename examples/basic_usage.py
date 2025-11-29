"""
Basic Usage Example - RedLight API

This example demonstrates the simplest way to download videos
using the RedLight API.
"""

from RedLight import DownloadVideo, GetVideoInfo

# Example PornHub Shorts URL (replace with actual URL)
VIDEO_URL = "https://www.pornhub.com/view_video.php?viewkey=your_video_key_here"


def main():
    print("=== RedLight API - Basic Usage ===\n")
    
    # 1. Get video information first
    print("📋 Fetching video information...")
    info = GetVideoInfo(VIDEO_URL)
    
    print(f"Title: {info['title']}")
    print(f"Video ID: {info['video_id']}")
    print(f"Available Qualities: {info['available_qualities']}")
    print()
    
    # 2. Download the video
    print("⬇️ Downloading video...")
    video_path = DownloadVideo(
        url=VIDEO_URL,
        output_dir="./my_videos",
        quality="best"  # or "720", "1080", etc.
    )
    
    print(f"✅ Downloaded successfully!")
    print(f"📁 Saved to: {video_path}")


if __name__ == "__main__":
    main()
