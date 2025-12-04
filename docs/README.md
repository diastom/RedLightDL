# 📚 RedLight API Documentation

Welcome to the complete API documentation for RedLight! This documentation will help you integrate RedLight into your Python projects.

## 📖 Documentation Structure

### Quick Start
- **[Quick Start Guide](QuickStart.md)** - Get started in 5 minutes
- **[Installation](QuickStart.md#installation)** - Installing RedLight

### Multi-Site Support
- **[Multi-Site Guide](MultiSite.md)** 🌐 **NEW!** - Complete guide for all 4 supported sites
  - PornHub, Eporner, Spankbang, XVideos
  - Simple and advanced examples
  - Multi-site search and batch downloads
  - Site comparison and best practices

### API Reference
- **[API Functions](API.md)** - High-level helper functions (`DownloadVideo`, `GetVideoInfo`, etc.)
- **[Classes](Classes.md)** - Detailed class documentation
  - `VideoDownloader`
  - `BatchDownloader`
  - `PlaylistDownloader`
  - `VideoConverter`
  - `MetadataEditor`
  - `PornHubSearch`, `MultiSiteSearch`
  - `AsyncVideoDownloader`
  - Site-specific classes

### Guides & Examples
- **[Examples](Examples.md)** - Practical code examples for common use cases
- **[Advanced Usage](Advanced.md)** - Advanced topics and best practices

## 🚀 Quick Example

```python
from RedLight import DownloadVideo

# Simple one-liner
video_path = DownloadVideo("https://www.pornhub.com/view_video.php?viewkey=xxxxx")
print(f"Downloaded: {video_path}")
```

## 📋 Table of Contents

1. [Quick Start Guide](QuickStart.md)
2. [Multi-Site Guide](MultiSite.md) 🌐
3. [API Functions Reference](API.md)
4. [Classes Documentation](Classes.md)
5. [Code Examples](Examples.md)
6. [Advanced Usage](Advanced.md)

## 🆘 Getting Help

- **GitHub Issues:** [Report bugs or request features](https://github.com/diastom/RedLightDL/issues)
- **Examples:** Check the [examples/](../examples/) directory for working code

## 🔗 External Links

- [GitHub Repository](https://github.com/diastom/RedLightDL)
- [PyPI Package](https://pypi.org/project/ph-shorts/)
- [Changelog](../CHANGELOG.md)
