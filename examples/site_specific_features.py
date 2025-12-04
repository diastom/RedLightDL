"""
Site-Specific Features Example - RedLight API

This example showcases the unique features of each supported site:
- PornHub: HLS streaming, playlists, advanced search
- Eporner: Ultra-fast aria2c downloads
- Spankbang: 4K support, hybrid delivery
- XVideos: Intelligent fallback, multiple qualities
"""

from RedLight import (
    PornHubDownloader,
    PornHubSearch,
    EpornerDownloader,
    EpornerSearch,
    SpankBangDownloader,
    SpankBangSearch,
    XVideosDownloader,
    XVideosSearch,
    GetVideoInfo
)


def pornhub_features():
    """Demonstrate PornHub-specific features"""
    
    print("="*60)
    print("PornHub Features")
    print("="*60)
    
    print("\n1. HLS Streaming Downloads")
    print("-"*60)
    print("  • Multi-threaded segment downloading")
    print("  • Qualities: 240p, 480p, 720p, 1080p")
    print("  • Automatic segment merging")
    searcher = PornHubSearch()
    print("  • Sort by: mostviewed, toprated, newest")
    print("  • Duration filters: short, medium, long")
    print("  • Page navigation")
    
    print("\n  Example search:")
    print("    results = searcher.search('query', sort_by='toprated', duration='medium')")
    
    print("\n3. Playlist/Channel Support")
    print("-"*60)
    print("  • Download entire channels")
    print("  • Playlist downloads")
    print("  • Customizable limits")
    
    print("\n  Example:")
    print("    playlist = PlaylistDownloader()")
    print("    urls = playlist.GetChannelVideos('username', limit=10)")


def eporner_features():
    """Demonstrate Eporner-specific features"""
    
    print("\n" + "="*60)
    print("Eporner Features")
    print("="*60)
    
    print("\n1. Ultra-Fast aria2c Downloads")
    print("-"*60)
    print("  • Direct MP4 downloads (no segments)")
    print("  • Built-in aria2c download manager")
    print("  • Maximum download speed")
    print("  • Resume support")
    
    ep = EpornerDownloader()
    url = "https://www.eporner.com/video-xxxxx/title"
    
    print("\n  How it works:")
    print("    1. Fetches direct MP4 URL")
    print("    2. Uses aria2c for parallel downloading")
    print("    3. Automatic retry on failure")
    print("    4. Much faster than sequential downloads")
    
    print("\n2. Simple Quality Selection")
    print("-"*60)
    print("  • Multiple MP4 qualities available")
    print("  • Direct file downloads")
    print("  • No conversion needed")
    
    print("\n3. Search Functionality")
    print("-"*60)
    searcher = EpornerSearch()
    print("  • Basic search support")
    print("  • Returns direct video URLs")
    
    print("\n  Example:")
    print("    results = searcher.search('query')")
    print("    for video in results:")
    print("        DownloadVideo(video['url'])  # Ultra-fast with aria2c!")


def spankbang_features():
    """Demonstrate Spankbang-specific features"""
    
    print("\n" + "="*60)
    print("Spankbang Features")
    print("="*60)
    
    print("\n1. 4K Support")
    print("-"*60)
    print("  • Qualities: 240p, 480p, 720p, 1080p, 4K (2160p)")
    print("  • Highest quality support among all sites")
    print("  • Automatic quality detection")
    
    sb = SpankBangDownloader()
    url = "https://spankbang.com/xxxxx/video/title"
    
    print("\n  Example 4K download:")
    print("    video = sb.download(url, quality='2160')  # 4K")
    print("    video = sb.download(url, quality='best')  # Auto-select highest")
    
    print("\n2. Hybrid Delivery System")
    print("-"*60)
    print("  • Intelligent format selection")
    print("  • MP4 with aria2c for fast downloads")
    print("  • HLS fallback for reliability")
    print("  • Best of both worlds")
    
    print("\n  How it works:")
    print("    1. Tries MP4 with aria2c first (faster)")
    print("    2. Falls back to HLS if needed (more reliable)")
    print("    3. Automatic format detection")
    
    print("\n3. Search Functionality")
    print("-"*60)
    searcher = SpankBangSearch()
    print("  • Basic search support")
    print("  • Returns video metadata")
    
    print("\n  Example:")
    print("    results = searcher.search('query')")


def xvideos_features():
    """Demonstrate XVideos-specific features"""
    
    print("\n" + "="*60)
    print("XVideos Features")
    print("="*60)
    
    print("\n1. Intelligent Fallback System")
    print("-"*60)
    print("  • Tries MP4 download first")
    print("  • Automatically falls back to HLS")
    print("  • Ensures download success")
    print("  • No manual intervention needed")
    
    xv = XVideosDownloader()
    url = "https://www.xvideos.com/video.xxxxx/title"
    
    print("\n  How it works:")
    print("    1. Attempts direct MP4 download")
    print("    2. If MP4 fails, tries HLS streaming")
    print("    3. Downloads whichever works")
    print("    4. User gets the video either way")
    
    print("\n2. Multiple Quality Options")
    print("-"*60)
    print("  • Qualities: 360p, 720p, 1080p")
    print("  • Good balance of quality and file size")
    print("  • Automatic quality selection")
    
    print("\n  Example:")
    print("    info = GetVideoInfo(url)")
    print("    print(info['available_qualities'])  # [360, 720, 1080]")
    print("    video = xv.download(url, quality='720')")
    
    print("\n3. Search Functionality")
    print("-"*60)
    searcher = XVideosSearch()
    print("  • Basic search support")
    print("  • Returns video information")
    
    print("\n  Example:")
    print("    results = searcher.search('query')")


def comparison_example():
    """Compare all sites side by side"""
    
    print("\n" + "="*60)
    print("Site Comparison")
    print("="*60)
    
    features = [
        ("Max Quality", "1080p", "1080p", "4K (2160p)", "1080p"),
        ("Technology", "HLS", "MP4+aria2c", "Hybrid", "MP4/HLS"),
        ("Speed", "Fast", "Ultra Fast", "Fast", "Fast"),
        ("Playlists", "Yes", "No", "No", "No"),
        ("Search", "Advanced", "Basic", "Basic", "Basic"),
        ("Fallback", "No", "No", "Yes", "Yes")
    ]
    
    print("\n                 PornHub    Eporner    Spankbang  XVideos")
    print("-"*60)
    for feature, ph, ep, sb, xv in features:
        print(f"{feature:15} {ph:11} {ep:11} {sb:11} {xv:11}")
    
    print("\nBest for:")
    print("  • PornHub: Playlists, Advanced search, Reliable streaming")
    print("  • Eporner: Maximum download speed")
    print("  • Spankbang: Highest quality (4K)")
    print("  • XVideos: Reliability with automatic fallback")


def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║      RedLight DL - Site-Specific Features Showcase         ║
╚════════════════════════════════════════════════════════════╝

This example showcases unique features of each site.
All examples are informational - no downloads will be performed.
""")
    
    # Show features of each site
    pornhub_features()
    eporner_features()
    spankbang_features()
    xvideos_features()
    
    # Comparison
    comparison_example()
    
    print("\n" + "="*60)
    print("✓ Feature showcase complete!")
    print("="*60)
    print("\nTo use these features:")
    print("  • Import the site-specific classes")
    print("  • Use GetVideoInfo() to check available options")
    print("  • Download with DownloadVideo() - it auto-detects the site!")


if __name__ == "__main__":
    main()
