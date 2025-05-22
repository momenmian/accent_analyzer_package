import os
import tempfile
from pydub import AudioSegment

class AudioExtractor:
    """
    Class to extract audio from video URLs
    """
    def __init__(self, temp_dir=None):
        """
        Initialize the audio extractor
        
        Args:
            temp_dir (str, optional): Directory to store temporary files. Defaults to None.
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Set ffmpeg path for pydub
        AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"
        AudioSegment.ffmpeg = "/opt/homebrew/bin/ffmpeg"
        AudioSegment.ffprobe = "/opt/homebrew/bin/ffprobe"
    
    def extract_from_url(self, url):
        """
        Extract audio from a video URL
        
        Args:
            url (str): URL of the video
            
        Returns:
            str: Path to the extracted audio file
        """
        # Check if URL is direct media file
        if url.endswith(('.mp4', '.mov', '.avi', '.webm')):
            return self._download_direct_media(url)
        
        # Otherwise use yt-dlp for extraction
        return self._extract_with_ytdlp(url)
    
    def _download_direct_media(self, url):
        """
        Download direct media file and extract audio
        
        Args:
            url (str): URL of the media file
            
        Returns:
            str: Path to the extracted audio file
        """
        import requests
        from pydub import AudioSegment
        
        temp_video_path = os.path.join(self.temp_dir, "temp_video.mp4")
        temp_audio_path = os.path.join(self.temp_dir, "temp_audio.mp3")
        
        # Download the video file
        response = requests.get(url, stream=True)
        with open(temp_video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        
        # Extract audio using pydub
        video = AudioSegment.from_file(temp_video_path)
        video.export(temp_audio_path, format="mp3")
        
        # Clean up video file
        os.remove(temp_video_path)
        
        return temp_audio_path
    
    def _extract_with_ytdlp(self, url):
        """
        Extract audio using yt-dlp
        
        Args:
            url (str): URL of the video
            
        Returns:
            str: Path to the extracted audio file
        """
        import yt_dlp
        from pydub import AudioSegment
        
        temp_audio_path = os.path.join(self.temp_dir, "temp_audio.mp3")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.temp_dir, 'temp_audio'),
            'ffmpeg_location': '/opt/homebrew/bin/',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # yt-dlp adds extension automatically, so we need to check if the file exists
        if os.path.exists(temp_audio_path):
            return temp_audio_path
        else:
            # Try with the extension that yt-dlp might have added
            for ext in ['.mp3', '.m4a', '.webm']:
                potential_path = os.path.join(self.temp_dir, f"temp_audio{ext}")
                if os.path.exists(potential_path):
                    # Convert to mp3 if not already
                    if ext != '.mp3':
                        audio = AudioSegment.from_file(potential_path)
                        audio.export(temp_audio_path, format="mp3")
                        os.remove(potential_path)
                        return temp_audio_path
                    return potential_path
            
            raise Exception("Failed to extract audio from URL")
