# Accent Analyzer Tool

* Accept a public video URL (e.g. Loom, direct MP4).
* Extract the audio track.
* Classify the speaker's **English accent** (American, British, Australian, Canadian … and others) using a pre-trained model.
* Return a confidence score and a short explanation (top-5 candidates).
* Provide a simple CLI interface.

## 1 Quick start

```bash
# 1. (Recommended) create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. install Python dependencies
pip install -r requirements.txt

# 3. install system tools
#    – ffmpeg (required for audio extraction)
#    – yt-dlp (required for YouTube / TikTok / Shorts URLs)
# macOS (Homebrew):
brew install ffmpeg yt-dlp
# Ubuntu / Debian:
sudo apt install ffmpeg
pip install -U yt-dlp               # or `sudo snap install yt-dlp`

# 4. run either the CLI or the Web UI

# CLI (single command)
python main.py "https://example.com/my_video.mp4"

# Streamlit Web UI (nice front-end)
streamlit run streamlit_app.py       # then open the URL shown in the terminal
```

Example CLI output:

```text
Downloading video…
Extracting audio…
Loading accent classifier (this may take a minute on first run)…
Classifying accent…

=== Accent Analysis Result ===
Predicted accent: us
Confidence: 82.34%
Top candidates:
  us           82.34%
  canada       10.51%
  england       3.19%
  scotland      1.21%
  australia     0.74%
Done.
```

## 2 Project structure

```
main.py               # CLI entry-point
streamlit_app.py      # Web UI (Streamlit)
audio_utils.py        # download + ffmpeg / yt-dlp helpers
accent_model.py       # wraps the SpeechBrain model
PRD.md                # functional requirements
README.md             # this file
requirements.txt      # Python dependencies
.gitignore
└── (generated at runtime)
    ├── audio_cache/            # cached audio snippets
    └── wav2vec2_checkpoints/   # downloaded SpeechBrain checkpoints
```

## 3 Technical notes

* Accent classification uses the open-source **SpeechBrain** model
  `Jzuluaga/accent-id-commonaccent_xlsr-en-english` – 16 English accents.
* Audio is converted to **16 kHz mono WAV** with ffmpeg (`audio_utils.extract_audio`).
* For YouTube/TikTok/Shorts links the downloader uses **yt-dlp** with the format
  string `bv*+ba/bestaudio/best` to avoid silent video-only streams.
* The first run downloads the speech model (~400 MB) so inference can take ~1 min.

## 4 Supported video sources

| Source type | How to use |
|-------------|------------|
| **Direct .mp4 URL** | Pass the URL directly to the CLI / Web UI – handled by simple HTTP download. |
| **Loom – raw asset** (`https://cdn.loom.com/.../raw/<id>.mp4`) | Works exactly like any other MP4 link – just paste it. |
| **Loom – share page** (`https://www.loom.com/share/<id>`) | Use `yt-dlp` to retrieve the underlying MP4:<br>`yt-dlp -o temp.mp4 <share-url>` then `python main.py temp.mp4`. You can also extend `audio_utils.download_video()` to call `yt-dlp` for Loom as we already do for YouTube. |
| **YouTube / TikTok / Shorts** | With `yt-dlp` installed you can pass the public video URL directly; the helper downloads and merges the best video+audio track automatically. |