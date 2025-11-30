"""
Video Converter Module - Convert and compress videos.

This module provides format conversion and compression capabilities
using FFmpeg.
"""

from typing import Optional
from pathlib import Path
import subprocess
import shutil


class VideoConverter:
    """
    Convert video formats and compress videos using FFmpeg.
    
    Supports conversion to multiple formats (mp4, webm, mkv) and
    compression with quality control. Can also extract audio-only (mp3).
    
    Example:
        >>> from RedLight import VideoConverter
        >>> 
        >>> converter = VideoConverter()
        >>> webm_file = converter.Convert("video.mp4", output_format="webm")
        >>> compressed = converter.Convert("video.mp4", compress_quality=70)
    """
    
    def __init__(self):
        """Initialize VideoConverter and check for FFmpeg."""
        self.ffmpeg_available = shutil.which("ffmpeg") is not None
        
        if not self.ffmpeg_available:
            raise RuntimeError(
                "FFmpeg is not installed or not in PATH. "
                "Please install FFmpeg to use video conversion features."
            )
    
    def Convert(
        self,
        input_file: str,
        output_format: str = "mp4",
        compress_quality: Optional[int] = None,
        audio_only: bool = False,
        output_file: Optional[str] = None
    ) -> str:
        """Convert video format or compress video."""
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Handle audio extraction
        if audio_only:
            output_format = "mp3"
        
        # Generate output filename
        if output_file:
            output_path = Path(output_file)
        else:
            output_path = input_path.with_suffix(f".{output_format}")
            
            # Avoid overwriting - add suffix if exists
            counter = 1
            while output_path.exists():
                output_path = input_path.with_stem(
                    f"{input_path.stem}_converted_{counter}"
                ).with_suffix(f".{output_format}")
                counter += 1
        
        # Build FFmpeg command
        cmd = ["ffmpeg", "-i", str(input_path)]
        
        if audio_only:
            # Extract audio only
            cmd.extend(["-vn", "-acodec", "libmp3lame", "-q:a", "2"])
        else:
            # Video conversion
            if output_format == "webm":
                cmd.extend(["-c:v", "libvpx-vp9", "-c:a", "libopus"])
            elif output_format == "mkv":
                cmd.extend(["-c:v", "libx264", "-c:a", "aac"])
            else:  # mp4
                cmd.extend(["-c:v", "libx264", "-c:a", "aac"])
            
            # Apply compression if specified
            if compress_quality is not None:
                # CRF: 0 (lossless) to 51 (worst quality)
                # Convert 0-100 scale to CRF scale (inverted)
                crf = int(51 - (compress_quality / 100 * 51))
                cmd.extend(["-crf", str(crf)])
        
        cmd.extend(["-y", str(output_path)])  # -y to overwrite
        
        # Execute FFmpeg
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return str(output_path)
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"FFmpeg conversion failed: {e.stderr}"
            )
    
    def Compress(
        self,
        input_file: str,
        quality: int = 70,
        output_file: Optional[str] = None
    ) -> str:
        """Compress video file."""
        return self.Convert(
            input_file=input_file,
            compress_quality=quality,
            output_file=output_file
        )
    
    def ExtractAudio(
        self,
        input_file: str,
        output_file: Optional[str] = None
    ) -> str:
        """Extract audio from video as MP3."""
        return self.Convert(
            input_file=input_file,
            audio_only=True,
            output_file=output_file
        )
    
    @staticmethod
    def IsFFmpegAvailable() -> bool:
        """Check if FFmpeg is available."""
        return shutil.which("ffmpeg") is not None

    def ConvertTsToMp4(self, input_file: Path, keep_ts: bool = False) -> str:
        """
        Convert .ts file to .mp4 with fallback logic.
        
        Args:
            input_file: Path to input .ts file
            keep_ts: If True, returns original file path without conversion
            
        Returns:
            Path to output file (either .mp4 or original .ts)
        """
        input_path = Path(input_file)
        
        if keep_ts:
            return str(input_path)

        if not self.ffmpeg_available:
            print("⚠ FFmpeg not found. Keeping .ts file.")
            return str(input_path)

        # Validate input file exists and has content
        if not input_path.exists() or input_path.stat().st_size == 0:
            print(f"⚠ Input file is empty or missing. Cannot convert.")
            return str(input_path)

        output_path = input_path.with_suffix('.mp4')
        
        try:
            # Try direct copy first (fastest)
            cmd = [
                'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
                '-i', str(input_path), 
                '-c', 'copy',
                str(output_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # Check if output file was created and has reasonable size
            if output_path.exists() and output_path.stat().st_size > 0:
                if input_path.exists():
                    input_path.unlink()
                return str(output_path)
            else:
                raise subprocess.CalledProcessError(1, cmd)
                
        except subprocess.CalledProcessError:
            # Try re-encoding as fallback (slower but more compatible)
            try:
                print("⚠ Direct copy failed, trying re-encode...")
                cmd = [
                    'ffmpeg', '-y', '-hide_banner', '-loglevel', 'warning',
                    '-err_detect', 'ignore_err',
                    '-i', str(input_path),
                    '-c:v', 'libx264', '-preset', 'ultrafast',
                    '-c:a', 'aac', '-b:a', '128k',
                    '-movflags', '+faststart',
                    str(output_path)
                ]
                result = subprocess.run(cmd, check=False, capture_output=True, text=True)
                
                if output_path.exists() and output_path.stat().st_size > 0:
                    if input_path.exists():
                        input_path.unlink()
                    return str(output_path)
                else:
                    if result.stderr:
                        print(f"⚠ FFmpeg error: {result.stderr[:200]}")
            except Exception as ex:
                print(f"⚠ Re-encode exception: {ex}")
            
            print(f"⚠ Failed to convert to MP4. Keeping .ts file.")
            return str(input_path)
