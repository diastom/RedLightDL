# Release Notes - PH Shorts Downloader

## Version 1.0.6 (2025-11-28)

### 🎉 Major New Features

#### Programmable API Support
PHShorts can now be used as a Python library! Build custom scripts, bots, and automation tools.

**New Modules:**
- `api.py` - High-level helper functions (PascalCase naming)
- `async_downloader.py` - Async support for bots

**Available Functions:**
```python
from PHShorts import (
    DownloadVideo,           # Simple one-liner downloads
    GetVideoInfo,            # Get metadata without downloading
    ListAvailableQualities,  # List available quality options
    VideoDownloader,         # Main downloader class
    AsyncVideoDownloader     # Async version for bots
)
```

**Use Cases:**
- Build Telegram/Discord bots
- Create batch download scripts
- Integrate into existing applications
- Progress tracking and custom workflows

### 📚 Documentation & Examples

- Added comprehensive API usage section in README
- Created 4 working example files:
  - `examples/basic_usage.py` - Simple download example
  - `examples/progress_tracking.py` - Progress bar implementation
  - `examples/telegram_bot.py` - Telegram bot integration
  - `examples/batch_download.py` - Batch downloads with error handling

### 🔄 Changes
- Updated `__init__.py` to export new API functions
- Version bumped to 1.0.6 throughout project
- **Naming Convention**: Functions use PascalCase (e.g., `DownloadVideo`)
- CLI functionality remains unchanged (full backward compatibility)

### 🐛 Bug Fixes
- None in this release (new features only)

---

## Version 1.0.5 (Previous)

See previous release notes for older versions.
