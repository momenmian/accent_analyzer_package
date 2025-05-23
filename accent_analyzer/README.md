# Video Accent Analyzer

## Overview

This tool analyzes a public video URL (e.g., Loom, MP4 link) to extract audio, and then (currently using a mock service) attempts to detect the speaker's English accent. It provides a classification (e.g., British, American, Australian) and a confidence score.

This project was developed as a solution to a coding challenge.

## Features

- Accepts public video URLs.
- Downloads the video.
- Extracts audio from the video (saves as WAV).
- Analyzes speaker's accent (currently uses a **mock detection service**).
- Outputs classification, confidence score, and a summary.
- Simple web UI for interaction.

## Core Technologies Used

- Python 3
- Flask (for the web UI)
- yt-dlp (for video downloading)
- FFmpeg (via ffmpeg-python, for audio extraction)
- Requests (for potential API communication)

## Prerequisites

- Python 3.7+
- Pip (Python package installer)
- **FFmpeg**: This is a critical system dependency and must be installed and available in your system's PATH.
    - On Debian/Ubuntu: `sudo apt update && sudo apt install ffmpeg`
    - On macOS (using Homebrew): `brew install ffmpeg`
    - On Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Setup and Installation

1.  **Clone the repository (or download the source code):**
    ```bash
    # git clone <repository_url> # If it were in a repo
    # cd accent_analyzer_project 
    ```
    (For now, assume the user has the `accent_analyzer` folder)

2.  **Navigate to the project directory:**
    ```bash
    cd accent_analyzer 
    ```

3.  **Create a Python virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Ensure FFmpeg is installed and accessible.**
2.  **Run the Flask development server:**
    ```bash
    python app.py
    ```
3.  Open your web browser and go to: `http://127.0.0.1:5000/` (or `http://0.0.0.0:5000/` as configured).

You should see a page where you can input a video URL to start the analysis.

## Accent Detection Mock

The current version uses a **mock accent detection service** located in `accent_detector.py`. This means it returns pre-defined results and does not perform actual accent analysis.

To implement real accent detection, you would need to:
1.  Choose a suitable accent detection API or pre-trained model.
2.  Update the `detect_accent` function in `accent_analyzer/accent_detector.py` to call this API/model with the extracted audio.
3.  Parse the API/model's response into the expected dictionary format.
4.  Potentially manage API keys or model file downloads.

Examples of services to investigate:
- Google Cloud Speech-to-Text (check for accent metadata or regional language codes like `en-US`, `en-GB`).
- AWS Transcribe.
- Azure Speech Services.
- Specialized third-party voice analytic APIs.

## Project Structure

accent_analyzer/
├── app.py                # Main Flask application and orchestration logic
├── video_processor.py    # Video downloading and audio extraction
├── accent_detector.py    # Accent detection (currently mock)
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # HTML template for the UI
├── static/
│   └── style.css         # CSS for the UI
└── README.md             # This file
