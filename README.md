# English Accent Analyzer

This application analyzes English accents from video content, classifying them as British, American, or Australian.

## Features
- Accepts public video URLs (YouTube, Loom, or direct MP4 links)
- Extracts audio from videos
- Analyzes the speaker's accent
- Classifies the accent as British, American, or Australian
- Provides a confidence score
- Includes a detailed explanation of accent characteristics

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- ffmpeg (required for audio processing)

### Installation

1. Clone or download this repository

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
```
venv\Scripts\activate
```
- On macOS/Linux:
```
source venv/bin/activate
```

4. Install the required packages:
```
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask server:
```
python src/main.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

3. Enter a public video URL and click "Analyze Accent"

## How It Works

1. **Audio Extraction**: The application extracts audio from the provided video URL using yt-dlp and pydub.

2. **Accent Analysis**: The application uses pattern matching to identify accent characteristics based on:
   - Vocabulary patterns (e.g., "lift" vs "elevator")
   - Grammar patterns (e.g., "have got" vs "have gotten")
   - Phonetic patterns (pronunciation differences)

3. **Classification**: Based on the analysis, the application determines the most likely accent and calculates a confidence score.

## Limitations

- The accent detection is based on pattern matching and may not be as accurate as professional linguistic analysis
- The application currently only supports English accents (British, American, Australian)
- Video URLs must be publicly accessible

## Troubleshooting

- If you encounter issues with audio extraction, ensure ffmpeg is properly installed
- For YouTube videos, ensure they are not age-restricted or private
