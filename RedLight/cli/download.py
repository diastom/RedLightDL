import sys
import shutil
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich import box
import traceback
from .ui import console, db
from ..sites import SiteRegistry
from ..api import GetVideoInfo, DownloadVideo
from ..converter import VideoConverter

def process_video_conversion(video_path, format=None, compress=None, audio_only=False, keep_ts=False, console=None):
    """
    Handle video conversion, compression, and audio extraction.
    
    Args:
        video_path: Path to the downloaded video
        format: Target format (mp4, webm, mkv)
        compress: Compression quality (0-100)
        audio_only: Extract audio as MP3
        keep_ts: Keep original file if converting
        console: Rich console for output
    
    Returns:
        Path to the final file
    """
    if not (format or compress is not None or audio_only):
        return video_path
        
    if not console:
        from .ui import console as default_console
        console = default_console

    try:
        if not VideoConverter.IsFFmpegAvailable():
            console.print("[red]❌ FFmpeg not found! Conversion features require FFmpeg.[/]")
            console.print("[yellow]Install FFmpeg to use --format, --compress, or --audio-only[/]")
            return video_path
        
        converter = VideoConverter()
        console.print(f"  [dim]Processing: {Path(video_path).name}...[/]")
        
        converted_path = converter.Convert(
            input_file=video_path,
            output_format=format if format else "mp4",
            compress_quality=compress,
            audio_only=audio_only
        )
        
        console.print(f"  [green]✓[/] Converted: {Path(converted_path).name}")
        
        # Cleanup: If user didn't explicitly ask to keep TS, delete it
        # Only delete if the new file is different from the old one
        if not keep_ts and Path(video_path) != Path(converted_path):
            try:
                Path(video_path).unlink()
            except Exception:
                pass
                
        return converted_path
        
    except Exception as e:
        console.print(f"  [red]Conversion failed: {e}[/]")
        return video_path

def download_video(url, output=None, quality='best', proxy=None, keep_ts=False, subs=False, speed_limit=None):

    """Download a video with fancy progress bars using multi-site API"""
    
    try:

        
        # Phase 1: Get video info and display
        with console.status("[bold cyan]🔍 Detecting site and fetching video information...", spinner="dots"):
            registry = SiteRegistry()
            site_name = registry.detect_site(url)
            
            if not site_name:
                raise ValueError("Unsupported URL. Please use a PornHub or Eporner link.")
            
            # Get video info
            info = GetVideoInfo(url)
        
        # Display video information
        console.print(f"[green]✓[/] Site: [bold]{site_name.title()}[/]")
        console.print(f"[green]✓[/] Video: [bold]{info['title']}[/]")
        console.print(f"[green]✓[/] Available Qualities: [bold]{', '.join([f'{q}p' for q in info['available_qualities']])}[/]")
        
        # Determine selected quality
        if quality == 'best':
            selected_q = max(info['available_qualities'])
        elif quality == 'worst':
            selected_q = min(info['available_qualities'])
        else:
            try:
                req_q = int(quality)
                # Find closest quality
                selected_q = min(info['available_qualities'], key=lambda x: abs(x - req_q))
            except:
                selected_q = max(info['available_qualities'])
        
        console.print(f"[green]✓[/] Selected Quality: [bold]{selected_q}p[/]")
        
        if proxy:
            console.print(f"[green]✓[/] Proxy: [bold]{proxy}[/]")
        
        # Phase 2: Download with progress tracking
        console.print("\n[bold cyan]📥 Downloading...[/]")
        output_dir = "./downloads"
        
        # For Eporner, disable aria2c to get progress feedback
        # We'll use the Python multi-threaded downloader
        if site_name == "eporner":
            # Temporarily disable aria2c for better progress tracking
            aria2c_path = shutil.which("aria2c")
            
            # Monkey-patch to disable aria2c
            original_which = shutil.which
            def mock_which(cmd):
                if cmd == "aria2c":
                    return None
                return original_which(cmd)
            
            shutil.which = mock_which
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(complete_style="cyan", finished_style="green"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeRemainingColumn(),
                console=console
            ) as progress:
                
                # Progress tracking
                task_id = None
                
                def on_progress(current, total):
                    nonlocal task_id
                    if task_id is None:
                        task_id = progress.add_task(
                            f"[cyan]Downloading {selected_q}p...", 
                            total=total
                        )
                    progress.update(task_id, completed=current)
                
                # Download using the multi-site API with progress callback
                result_path = DownloadVideo(
                    url=url,
                    output_dir=output_dir,
                    quality=quality,
                    filename=output,
                    keep_ts=keep_ts,
                    proxy=proxy,
                    on_progress=on_progress
                )
        finally:
            # Restore aria2c detection if we disabled it
            if site_name == "eporner":
                shutil.which = original_which
        
        # Success message
        console.print()
        success_panel = Panel(
            f"[bold green]✓ Download Successful![/]\n\n"
            f"[cyan]Site:[/] [bold white]{site_name.title()}[/]\n"
            f"[cyan]Title:[/] [bold white]{info['title']}[/]\n"
            f"[cyan]Quality:[/] [bold white]{selected_q}p[/]\n"
            f"[cyan]File:[/] [bold white]{Path(result_path).name}[/]\n"
            f"[cyan]Location:[/] [dim]{Path(result_path).absolute()}[/]",
            title="[bold green]Success[/]",
            border_style="green",
            box=box.DOUBLE
        )
        console.print(success_panel)
        
        # Save to history
        db.add_entry(url, info['title'], result_path, selected_q)
        
        return result_path
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠ Download cancelled by user[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]✗ Error:[/] {str(e)}")

        console.print(f"[dim]{traceback.format_exc()}[/]")
        sys.exit(1)
