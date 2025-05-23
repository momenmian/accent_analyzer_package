# Accent Analysis Tool

Accent Analyzer is an AI-powered tool designed to evaluate English language accents from video content. It assists in the hiring process by providing objective accent analysis. It can process public video URLs (Loom, YouTube, direct MP4) to analyze the speaker's English accent.

## Features

-   Accepts public video URLs (Loom, YouTube, direct .mp4 files).
-   Extracts audio from video.
-   Classifies English accents (e.g., American, British, Australian, Canadian).
-   Provides a confidence score for the classification.
-   Offers a basic analysis summary (top 5 accent candidates).
-   Simple CLI and Streamlit web UI.

## Setup and Installation

Follow these steps to set up and run the Accent Analysis Tool:

**1. Prerequisites:**

*   **Python 3.8+:** Ensure you have Python 3.8 or a newer version installed. You can download it from [python.org](https://www.python.org/).
*   **FFmpeg:** This is a system dependency required for audio extraction.
    *   **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt update && sudo apt install ffmpeg
        ```
    *   **macOS (using Homebrew):**
        ```bash
        brew install ffmpeg
        ```
    *   **Windows:** Download the FFmpeg binaries from [ffmpeg.org](https://ffmpeg.org/download.html). Add the `bin` directory (containing `ffmpeg.exe`) to your system's PATH environment variable.

**2. Clone the Repository:**

```bash
git clone https://github.com/momenmian/accent_analyzer_tool.git
cd accent_analysis_tool 
```

**3. Create a Virtual Environment (Recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**4. Install Dependencies:**

The project uses `yt-dlp` to download videos from sites like YouTube and Loom. Other dependencies are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

**5. Run the Application:**

You can use either the Streamlit web interface or the command-line script.

*   **Streamlit Web UI:**
    ```bash
    streamlit run streamlit_app.py
    ```
    Then open your web browser to the URL provided by Streamlit (usually `http://localhost:8501`).

*   **Command-Line Interface (CLI):**
    ```bash
    python main.py "<video_url>"
    ```
    Replace `<video_url>` with the public URL of the video you want to analyze. For example:
    ```bash
    python main.py "https://www.youtube.com/watch?v=your_video_id"
    python main.py "https://www.loom.com/share/your_video_id"
    ```

## Usage Notes

*   The first time you run the analysis, the accent classification model will be downloaded. This might take a few minutes depending on your internet connection. Subsequent runs will be faster as the model will be cached.
*   Ensure that the video URLs you provide are publicly accessible.

## Project Structure

*   `main.py`: CLI application entry point.
*   `streamlit_app.py`: Streamlit web UI application.
*   `accent_model.py`: Handles accent classification using a pre-trained model.
*   `audio_utils.py`: Utilities for downloading videos and extracting audio.
*   `requirements.txt`: Python package dependencies.
*   `PRD.md`: Project Requirements Document.