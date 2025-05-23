from __future__ import annotations

import subprocess
import tempfile
import os
from pathlib import Path
from typing import Tuple
import shutil
import requests

# Optional dependency for YouTube/remote site support
try:
    import yt_dlp  # type: ignore
except ImportError:  # pragma: no cover
    yt_dlp = None

FFMPEG_BINARY = shutil.which("ffmpeg") or "ffmpeg"

def download_video(url: str, destination: Path | str | None = None) -> Path:
    """Download remote video to a temporary file.

    Parameters
    ----------
    url: str
        Publicly accessible URL to a Loom or MP4 video.
    destination: Path | str | None
        Optional path to write the file to. If omitted, a temporary file is
        created inside the system temp folder.

    Returns
    -------
    Path
        Path to the downloaded video file.
    """
    # Detect YouTube/Shorts links early
    is_youtube = "youtube.com" in url or "youtu.be" in url

    if is_youtube and yt_dlp is not None:
        # Let yt_dlp decide the filename; download into a temp dir
        tmp_dir = tempfile.mkdtemp(prefix="accent_dl_")
        ydl_opts = {
            # Always prefer a format that **contains audio**. The previous
            # setting occasionally downloaded a video-only (silent) stream
            # which broke ffmpeg later when we tried to extract audio.
            # "ba" = bestaudio; "bv*+ba" = best video merged with best audio.
            # Either of these will guarantee an audio track is present.
            "format": "bv*+ba/bestaudio/best",
            "outtmpl": os.path.join(tmp_dir, "%(id)s.%(ext)s"),
            "quiet": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_path = Path(ydl.prepare_filename(info))
        return downloaded_path

    # Fallback: simple HTTP(S) download of direct file
    if destination is None:
        suffix = Path(url).suffix or ".mp4"
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=suffix)
        os.close(tmp_fd)
        dest_path = Path(tmp_path)
    else:
        dest_path = Path(destination)

    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    with dest_path.open("wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return dest_path


def extract_audio(video_path: str | Path, audio_path: str | Path | None = None) -> Path:
    """Extract audio track from video using ffmpeg.

    The output is a 16kHz mono WAV file suitable for speech models.
    """
    video_path = Path(video_path)
    if audio_path is None:
        audio_path = video_path.with_suffix(".wav")
    audio_path = Path(audio_path)

    cmd = [
        FFMPEG_BINARY,
        "-y",  # overwrite
        "-i",
        str(video_path),
        "-ac",
        "1",  # mono
        "-ar",
        "16000",  # 16 kHz sample rate
        "-vn",  # ignore the video stream explicitly
        str(audio_path),
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            "ffmpeg failed to decode the video. If you provided a YouTube or non-MP4 URL, "
            "install 'yt-dlp' (pip install yt-dlp) or supply a direct .mp4 link.\n"
            + result.stderr
        )
    return audio_path 