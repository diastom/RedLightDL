"""
Batch Download Example - RedLight API

This example shows how to download multiple videos with progress tracking.
"""

from RedLight import VideoDownloader
from typing import List


def progress_callback(video_num: int, total_videos: int):
    """Creates a progress callback for a specific video."""
    def callback(downloaded, total):
        percent = (downloaded / total) * 100
        print(f"  Video {video_num}/{total_videos}: [{percent:.1f}%] {downloaded}/{total} segments", end="\r")
    return callback


def batch_download(urls: List[str], output_dir: str = "./batch_downloads"):
    """
    Download multiple videos in batch.
    
    Args:
        urls: List of video URLs to download
        output_dir: Directory to save videos
    """
    print(f"=== Batch Download - {len(urls)} videos ===\n")
    
    downloader = VideoDownloader(output_dir=output_dir)
    downloaded = []
    failed = []
    
    for i, url in enumerate(urls, 1):
        try:
            print(f"\n📹 Processing video {i}/{len(urls)}...")
            
            # Get info
            info = downloader.get_info(url)
            print(f"  Title: {info['title']}")
            
            # Download
            video_path = downloader.download(
                url=url,
                quality="best",
                on_progress=progress_callback(i, len(urls))
            )
            
            print(f"\n  ✅ Downloaded: {video_path}")
            downloaded.append(video_path)
            
        except Exception as e:
            print(f"\n  ❌ Failed: {str(e)}")
            failed.append(url)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"✅ Successfully downloaded: {len(downloaded)}/{len(urls)}")
    if failed:
        print(f"❌ Failed: {len(failed)}")
        print("\nFailed URLs:")
        for url in failed:
            print(f"  - {url}")


def main():
    # Example URLs (replace with actual URLs)
    video_urls = [
        "https://www.pornhub.com/view_video.php?viewkey=xxxxx1",
        "https://www.pornhub.com/view_video.php?viewkey=xxxxx2",
        "https://www.pornhub.com/view_video.php?viewkey=xxxxx3",
    ]
    
    batch_download(video_urls, output_dir="./my_collection")


if __name__ == "__main__":
    main()
