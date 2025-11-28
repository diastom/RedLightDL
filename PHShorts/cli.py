"""
CLI interface for PH Shorts Downloader using Rich and Click
"""

import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box
from rich.text import Text

from .downloader import CustomHLSDownloader

console = Console()

BANNER = """
[bold cyan]╔═══════════════════════════════════════════════════════╗[/]
[bold cyan]║[/]  [bold magenta]██████╗ ██╗  ██╗    ███████╗██╗  ██╗ ██████╗ ██████╗ ████████╗███████╗[/]  [bold cyan]║[/]
[bold cyan]║[/]  [bold magenta]██╔══██╗██║  ██║    ██╔════╝██║  ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝[/]  [bold cyan]║[/]
[bold cyan]║[/]  [bold magenta]██████╔╝███████║    ███████╗███████║██║   ██║██████╔╝   ██║   ███████╗[/]  [bold cyan]║[/]
[bold cyan]║[/]  [bold magenta]██╔═══╝ ██╔══██║    ╚════██║██╔══██║██║   ██║██╔══██╗   ██║   ╚════██║[/]  [bold cyan]║[/]
[bold cyan]║[/]  [bold magenta]██║     ██║  ██║    ███████║██║  ██║╚██████╔╝██║  ██║   ██║   ███████║[/]  [bold cyan]║[/]
[bold cyan]║[/]  [bold magenta]╚═╝     ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝[/]  [bold cyan]║[/]
[bold cyan]╚═══════════════════════════════════════════════════════╝[/]
            [bold yellow]Download PornHub Shorts with Style![/]
    [dim]version 1.0.0 • Simple & Light[/]
"""


def show_banner():
    """Display the awesome banner"""
    console.print(BANNER)


def interactive_mode():
    """Interactive mode with beautiful prompts"""
    show_banner()
    
    # Get URL
    url = Prompt.ask("\n[bold green]🔗 Enter Video URL[/]")
    
    # Quality Selection
    console.print("\n[bold yellow]📺 Select Quality:[/]")
    quality_table = Table(show_header=False, box=box.SIMPLE)
    quality_table.add_column("Option", style="cyan", width=12)
    quality_table.add_column("Description", style="white")
    
    quality_table.add_row("1", "🏆 Best Available (Recommended)")
    quality_table.add_row("2", "📺 1080p")
    quality_table.add_row("3", "📱 720p")
    quality_table.add_row("4", "💾 480p")
    quality_table.add_row("5", "📉 Lowest Available (Data Saver)")
    
    console.print(quality_table)
    
    q_choice = Prompt.ask("   Your choice", choices=["1", "2", "3", "4", "5"], default="1")
    quality_map = {'1': 'best', '2': '1080', '3': '720', '4': '480', '5': 'worst'}
    quality = quality_map[q_choice]
    
    # Proxy
    proxy = None
    if Confirm.ask("\n[bold yellow]🌐 Use Proxy?[/]", default=False):
        proxy = Prompt.ask("   [cyan]Enter Proxy URL (e.g., http://127.0.0.1:2080)[/]")
        if not proxy.startswith("http"):
            proxy = f"http://{proxy}"
    
    # Start download
    download_video(url, quality=quality, proxy=proxy)


def download_video(url, output=None, quality='best', proxy=None, keep_ts=False):
    """Download a video with fancy progress bars"""
    
    headers = {'Origin': 'https://www.pornhub.com'}
    
    try:
        # Phase 1: Extracting video info
        with console.status("[bold cyan]🔍 Fetching video information...", spinner="dots"):
            downloader = CustomHLSDownloader(
                output_name=output,
                headers=headers,
                keep_ts=keep_ts,
                proxy=proxy
            )
            m3u8_url = downloader.extract_video_info(url)
        
        console.print(f"[green]✓[/] Video: [bold]{downloader.output_name.stem}[/]")
        if proxy:
            console.print(f"[green]✓[/] Proxy: [bold]{proxy}[/]")
        
        # Phase 2: Analyzing playlist
        with console.status("[bold cyan]📊 Analyzing stream quality...", spinner="dots"):
            response = downloader.session.get(m3u8_url, timeout=10)
            response.raise_for_status()
            playlist_content = response.text
            
            # Check for multiple qualities
            if "#EXT-X-STREAM-INF" in playlist_content:
                qualities = downloader._get_qualities(playlist_content, m3u8_url)
                if qualities:
                    sorted_keys = sorted([k for k in qualities.keys() if isinstance(k, int)], reverse=True)
                    
                    if quality == 'best':
                        selected_res = sorted_keys[0] if sorted_keys else list(qualities.keys())[0]
                    elif quality == 'worst':
                        selected_res = sorted_keys[-1] if sorted_keys else list(qualities.keys())[-1]
                    else:
                        try:
                            req_q = int(quality)
                            if req_q in qualities:
                                selected_res = req_q
                            elif sorted_keys:
                                selected_res = min(sorted_keys, key=lambda x:abs(x-req_q))
                            else:
                                selected_res = list(qualities.keys())[0]
                        except ValueError:
                            selected_res = sorted_keys[0] if sorted_keys else list(qualities.keys())[0]
                    
                    console.print(f"[green]✓[/] Quality: [bold]{selected_res}p[/]")
                    
                    # Fetch final playlist
                    selected_url = qualities[selected_res]
                    response = downloader.session.get(selected_url)
                    response.raise_for_status()
                    playlist_content = response.text
                    m3u8_url = selected_url
            
            # Parse segments
            segments = downloader._parse_media_playlist(playlist_content, m3u8_url)
            total_segments = len(segments)
            console.print(f"[green]✓[/] Segments: [bold]{total_segments}[/]")
        
        # Phase 3: Download with progress
        console.print("\n[bold cyan]📥 Downloading...[/]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(complete_style="cyan", finished_style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task("[cyan]Downloading segments...", total=total_segments)
            
            def progress_callback(completed, total):
                progress.update(task, completed=completed)
            
            # Update downloader with callback
            downloader.progress_callback = progress_callback
            
            # Start download
            from pathlib import Path
            import shutil
            import concurrent.futures
            
            temp_dir = Path("temp_segments")
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            temp_dir.mkdir(exist_ok=True)
            
            downloaded_files = []
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                future_to_segment = {
                    executor.submit(downloader._download_segment, seg_url, idx, temp_dir): idx 
                    for idx, seg_url in enumerate(segments)
                }
                
                completed = 0
                for future in concurrent.futures.as_completed(future_to_segment):
                    idx = future_to_segment[future]
                    try:
                        file_path = future.result()
                        downloaded_files.append((idx, file_path))
                        completed += 1
                        progress_callback(completed, total_segments)
                    except Exception as e:
                        pass
            
            # Merge segments
            progress.update(task, description="[yellow]Merging segments...")
            downloaded_files.sort(key=lambda x: x[0])
            
            with open(downloader.output_name, 'wb') as outfile:
                for _, segment_file in downloaded_files:
                    with open(segment_file, 'rb') as infile:
                        outfile.write(infile.read())
            
            shutil.rmtree(temp_dir)
            
            # Convert to MP4
            progress.update(task, description="[yellow]Converting to MP4...")
            final_file = downloader.convert_to_mp4()
            progress.update(task, completed=total_segments, description="[green]✓ Complete!")
        
        # Success message
        console.print()
        success_panel = Panel(
            f"[bold green]✓ Download Successful![/]\n\n"
            f"[cyan]File:[/] [bold white]{final_file}[/]\n"
            f"[cyan]Location:[/] [dim]{Path(final_file).absolute()}[/]",
            title="[bold green]Success[/]",
            border_style="green",
            box=box.DOUBLE
        )
        console.print(success_panel)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠ Download cancelled by user[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]✗ Error:[/] {str(e)}")
        sys.exit(1)


@click.command()
@click.argument('url', required=False)
@click.option('-o', '--output', help='Custom output filename', default=None)
@click.option('-q', '--quality', default='best', help='Quality (best, worst, 1080, 720, 480)')
@click.option('-p', '--proxy', help='HTTP/HTTPS Proxy URL', default=None)
@click.option('--keep-ts', is_flag=True, help='Keep the original .ts file')
def main(url, output, quality, proxy, keep_ts):
    """
    PH Shorts Downloader - Download PornHub Shorts videos with style!
    
    Examples:
    
        # Interactive mode
        ph-shorts
        
        # Download with URL
        ph-shorts "https://www.pornhub.com/view_video.php?viewkey=..."
        
        # Specify quality and output
        ph-shorts "URL" -q 720 -o my_video.mp4
        
        # Use proxy
        ph-shorts "URL" -p http://127.0.0.1:1080
    """
    
    if not url:
        # Interactive mode
        interactive_mode()
    else:
        # CLI mode
        show_banner()
        download_video(url, output=output, quality=quality, proxy=proxy, keep_ts=keep_ts)


if __name__ == '__main__':
    main()
