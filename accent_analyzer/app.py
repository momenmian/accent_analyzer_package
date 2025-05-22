# This is the main application file.
# It orchestrates video downloading, audio extraction, and accent detection.
# Now includes a Flask web UI.

import os
import shutil
from flask import Flask, render_template, request
from accent_analyzer.video_processor import download_video, extract_audio
from accent_analyzer.accent_detector import detect_accent

app = Flask(__name__)

TEMP_VIDEO_DIR = "temp_videos"
TEMP_AUDIO_DIR = "temp_audio"

# The core analysis logic remains largely the same.
# It's designed to return results, which is suitable for Flask.
def analyze_video_accent(video_url: str) -> dict | None:
    """
    Analyzes the accent from a video URL by downloading the video,
    extracting its audio, and then running accent detection.

    Args:
        video_url: The URL of the video to analyze.

    Returns:
        A dictionary with accent detection results if successful, None otherwise.
    """
    # Ensure temporary directories are unique per request or managed carefully
    # For simplicity in this example, using fixed names and ensuring they are created.
    # In a concurrent environment, unique temp dirs per request would be better.
    current_temp_video_dir = os.path.join(os.getcwd(), TEMP_VIDEO_DIR)
    current_temp_audio_dir = os.path.join(os.getcwd(), TEMP_AUDIO_DIR)

    os.makedirs(current_temp_video_dir, exist_ok=True)
    os.makedirs(current_temp_audio_dir, exist_ok=True)

    downloaded_video_path = None
    # extracted_audio_path = None # This variable is defined but not used outside its immediate scope.
    detection_results = None

    try:
        print(f"Starting analysis for video URL: {video_url}")

        # Step 1: Download Video
        print(f"Downloading video to {current_temp_video_dir}...")
        downloaded_video_path = download_video(video_url, current_temp_video_dir, filename="input_video")
        if not downloaded_video_path:
            print("Error: Video download failed.")
            # Ensure cleanup happens even if only download fails
            raise ValueError("Video download failed") 
        print(f"Video downloaded successfully: {downloaded_video_path}")

        # Step 2: Extract Audio
        print(f"Extracting audio to {current_temp_audio_dir}...")
        extracted_audio_path = extract_audio(downloaded_video_path, current_temp_audio_dir, audio_filename="input_audio")
        if not extracted_audio_path:
            print("Error: Audio extraction failed.")
            raise ValueError("Audio extraction failed")
        print(f"Audio extracted successfully: {extracted_audio_path}")

        # Step 3: Detect Accent
        print("Detecting accent...")
        detection_results = detect_accent(extracted_audio_path)
        if not detection_results:
            print("Error: Accent detection failed or returned no results.")
            raise ValueError("Accent detection returned no results")
        
        # Console logging of results (can be kept for backend logging)
        print("\n--- Backend Accent Detection Results ---")
        if isinstance(detection_results, dict):
            print(f"  Dominant Accent: {detection_results.get('dominant_accent', 'N/A')}")
            # ... (other print statements can be kept or removed as desired)
        print("--- End of Backend Results ---")
        
        return detection_results

    except Exception as e:
        # Log the exception for backend debugging
        print(f"An error occurred in the analysis pipeline: {e}")
        # The error_message for the template will be set in the route
        return None # Indicate failure to the calling Flask route
    finally:
        print("\nCleaning up temporary files...")
        if os.path.exists(current_temp_video_dir):
            try:
                shutil.rmtree(current_temp_video_dir)
                print(f"Successfully removed {current_temp_video_dir}")
            except Exception as e:
                print(f"Error removing {current_temp_video_dir}: {e}")
        
        if os.path.exists(current_temp_audio_dir):
            try:
                shutil.rmtree(current_temp_audio_dir)
                print(f"Successfully removed {current_temp_audio_dir}")
            except Exception as e:
                print(f"Error removing {current_temp_audio_dir}: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    error_message = None
    if request.method == 'POST':
        video_url = request.form.get('video_url')
        if not video_url:
            error_message = "Video URL is required."
        else:
            try:
                results = analyze_video_accent(video_url)
                if results is None:
                    # analyze_video_accent now returns None on any internal error,
                    # and prints specifics to console.
                    error_message = "Analysis failed. Check server logs for details. The video might be inaccessible, too long, or in an unsupported format."
            except Exception as e:
                # This catches errors if analyze_video_accent itself raises an unhandled one
                # or if there's an issue before/after calling it.
                print(f"Error in Flask route during analysis: {e}")
                error_message = f"An unexpected error occurred: {str(e)}"
                
    return render_template('index.html', results=results, error_message=error_message)

if __name__ == "__main__":
    print("Starting Flask development server...")
    # The host='0.0.0.0' makes it accessible from outside the container/VM if needed
    # The port can be changed if 5000 is in use
    app.run(host='0.0.0.0', port=5000, debug=True)
