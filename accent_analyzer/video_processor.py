# This file will contain functions for video processing,
# such as downloading videos from YouTube and extracting audio.
import yt_dlp
import os
import ffmpeg

def download_video(url: str, output_path: str, filename: str = "downloaded_video") -> str | None:
    """
    Downloads a video from the given URL using yt-dlp.

    Args:
        url: The URL of the video to download.
        output_path: The directory to save the video to.
        filename: The desired filename (without extension) for the video.

    Returns:
        The full path to the downloaded video file if successful, None otherwise.
    """
    os.makedirs(output_path, exist_ok=True)
    # Construct the output template for yt-dlp. This will be the full path without the extension.
    # yt-dlp will add the correct extension based on the format.
    output_template = os.path.join(output_path, filename)
    
    # The desired full path for the mp4 file we expect after download.
    expected_mp4_path = output_template + ".mp4"

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_template, # yt-dlp adds .ext; so, just pass the path without it
        'quiet': True,
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Check if the expected mp4 file was created
        if os.path.exists(expected_mp4_path):
            return expected_mp4_path
        else:
            # yt-dlp might save with a different extension if mp4 merging fails or isn't optimal.
            # It could also be that 'outtmpl' with an explicit extension was needed,
            # but typical usage is to let yt-dlp determine it.
            # We'll try to find a file with the given filename and common video extensions.
            possible_extensions = ['.mp4', '.mkv', '.webm', '.flv', '.avi']
            for ext in possible_extensions:
                potential_path = output_template + ext
                if os.path.exists(potential_path):
                    return potential_path # Return the path of the first found video file
            print(f"Downloaded video file not found at expected path: {expected_mp4_path} or with other common extensions.")
            return None 
            
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading video with yt-dlp: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during video download: {e}")
        return None

def extract_audio(video_file_path: str, output_audio_path: str, audio_filename: str = "extracted_audio") -> str | None:
    """
    Extracts audio from a video file and saves it as a WAV file.

    Args:
        video_file_path: The path to the input video file.
        output_audio_path: The directory to save the extracted audio file.
        audio_filename: The desired filename (without extension) for the audio file.

    Returns:
        The full path to the extracted WAV audio file if successful, None otherwise.
    """
    os.makedirs(output_audio_path, exist_ok=True)
    full_audio_filename = f"{audio_filename}.wav"
    full_output_path = os.path.join(output_audio_path, full_audio_filename)

    if not os.path.exists(video_file_path):
        print(f"Error: Video file not found at {video_file_path}")
        return None

    try:
        (
            ffmpeg
            .input(video_file_path)
            .output(full_output_path, acodec='pcm_s16le', ar='16000', ac=1) # Standard WAV format options
            .overwrite_output() # Overwrite if exists
            .run(capture_stdout=True, capture_stderr=True, quiet=True)
        )
        if os.path.exists(full_output_path):
            return full_output_path
        else:
            print(f"Error: Output audio file not found at {full_output_path} after ffmpeg processing.")
            return None
    except ffmpeg.Error as e:
        print(f"Error extracting audio with ffmpeg: {e.stderr.decode('utf8') if e.stderr else str(e)}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during audio extraction: {e}")
        return None
