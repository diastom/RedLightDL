"""
Multi-Site Usage Examples - RedLight API

This example demonstrates how to use RedLight with all 4 supported sites:
- PornHub
- Eporner  
- Spankbang
- XVideos
"""

from RedLight import DownloadVideo, GetVideoInfo, SiteRegistry

# Example URLs (replace with actual URLs)
PORNHUB_URL = "https://www.pornhub.com/view_video.php?viewkey=xxxxx"
EPORNER_URL = "https://www.eporner.com/video-xxxxx/title"
SPANKBANG_URL = "https://spankbang.com/xxxxx/video/title"
XVIDEOS_URL = "https://www.xvideos.com/video.xxxxx/title"


def example_automatic_detection():
    """Example 1: Automatic Site Detection"""
    print("="*60)
    print("Example 1: Automatic Site Detection")
    print("="*60)
    
    # RedLight automatically detects which site you're downloading from
    urls = [PORNHUB_URL, EPORNER_URL, SPANKBANG_URL, XVIDEOS_URL]
    
    registry = SiteRegistry()
    
    for url in urls:
        site_name = registry.detect_site(url)
        if site_name:
            print(f"✓ Detected: {site_name} - {url[:50]}...")
        else:
            print(f"✗ Not supported: {url[:50]}...")


def example_multi_site_download():
    """Example 2: Download from Multiple Sites"""
    print("\n" + "="*60)
    print("Example 2: Multi-Site Downloads")
    print("="*60)
    
    # All use the same simple API!
    urls_to_download = [
        ("PornHub", PORNHUB_URL),
        ("Eporner", EPORNER_URL),
        ("Spankbang", SPANKBANG_URL),
        ("XVideos", XVIDEOS_URL)
    ]
    
    for site_name, url in urls_to_download:
        try:
            print(f"\n[{site_name}] Getting video info...")
            info = GetVideoInfo(url)
            
            print(f"  Title: {info['title']}")
            print(f"  Available qualities: {info['available_qualities']}")
            
            # Download
            print(f"  Downloading...")
            video_path = DownloadVideo(url, quality="best")
            
            print(f"  ✓ Downloaded: {video_path}")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")


def example_site_specific_features():
    """Example 3: Site-Specific Features"""
    print("\n" + "="*60)
    print("Example 3: Site-Specific Features")
    print("="*60)
    
    # PornHub - HLS Streaming with multiple qualities
    print("\n[PornHub] HLS Streaming")
    try:
        info = GetVideoInfo(PORNHUB_URL)
        print(f"  Qualities: {info['available_qualities']}")
        print(f"  Uses multi-threaded segment downloading")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Eporner - Ultra-fast aria2c downloads
    print("\n[Eporner] Ultra-Fast aria2c")
    try:
        print(f"  Uses aria2c for maximum download speed")
        print(f"  Direct MP4 downloads (no segments)")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Spankbang - 4K support
    print("\n[Spankbang] 4K Support")
    try:
        info = GetVideoInfo(SPANKBANG_URL)
        print(f"  Qualities: {info['available_qualities']}")
        print(f"  Supports up to 4K (2160p)!")
        print(f"  Hybrid MP4/HLS delivery")
    except Exception as e:
        print(f"  Error: {e}")
    
    # XVideos - Intelligent fallback
    print("\n[XVideos] Intelligent Fallback")
    try:
        info = GetVideoInfo(XVIDEOS_URL)
        print(f"  Qualities: {info['available_qualities']}")
        print(f"  Automatic MP4/HLS fallback")
    except Exception as e:
        print(f"  Error: {e}")


def example_mixed_batch():
    """Example 4: Mixed Site Batch Download"""
    print("\n" + "="*60)
    print("Example 4: Mixed Site Batch Download")
    print("="*60)
    
    from RedLight import BatchDownloader
    
    # Mix URLs from all sites
    urls = [
        PORNHUB_URL,
        EPORNER_URL,
        SPANKBANG_URL,
        XVIDEOS_URL
    ]
    
    # RedLight handles all sites automatically
    downloader = BatchDownloader(
        concurrent=True,
        max_workers=4,
        quality="720"
    )
    
    downloader.AddUrls(urls)
    
    print(f"Downloading {len(urls)} videos from {len(set(url.split('/')[2] for url in urls))} different sites...")
    
    try:
        results = downloader.DownloadAll()
        print(f"\n✓ Successfully downloaded {len(results)} videos")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def main():
    print("\n" + "="*60)
    print("RedLight API - Multi-Site Examples")
    print("="*60)
    print("\nSupported Sites:")
    print("  • PornHub - HLS Streaming")
    print("  • Eporner - Ultra-fast aria2c downloads")
    print("  • Spankbang - 4K support")
    print("  • XVideos - Intelligent fallback")
    print("\n" + "="*60)
    
    # Run examples
    example_automatic_detection()
    
    # Uncomment to run other examples:
    # example_multi_site_download()
    # example_site_specific_features()
    # example_mixed_batch()
    
    print("\n" + "="*60)
    print("Examples complete!")
    print("="*60)


if __name__ == "__main__":
    main()
