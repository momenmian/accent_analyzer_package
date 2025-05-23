#!/usr/bin/env python
from __future__ import annotations

import argparse
import tempfile
from pathlib import Path
import sys

try:
    # When executed as package: python -m accent_analyzer.main
    from .audio_utils import download_video, extract_audio
    from .accent_model import AccentClassifier
except ImportError:  # executed as a standalone script
    from audio_utils import download_video, extract_audio  # type: ignore
    from accent_model import AccentClassifier  # type: ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze English accent from a video URL.")
    parser.add_argument("url", help="Public URL to a Loom or MP4 video")
    parser.add_argument(
        "--keep-files",
        action="store_true",
        help="Do not delete intermediate downloaded/extracted files (for debugging)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("Downloading video...")
    video_path = download_video(args.url)

    print("Extracting audio...")
    audio_path = extract_audio(video_path)

    print("Loading accent classifier (this may take a minute on first run)...")
    classifier = AccentClassifier()

    print("Classifying accent...")
    label, score, top5 = classifier.classify(str(audio_path))

    print("\n=== Accent Analysis Result ===")
    print(f"Predicted accent: {label}")
    print(f"Confidence: {score:.2%}")
    print("Top candidates:")
    for l, p in top5:
        print(f"  {l:<12} {p:.2%}")

    if not args.keep_files:
        try:
            Path(video_path).unlink(missing_ok=True)
            Path(audio_path).unlink(missing_ok=True)
        except Exception as e:
            print(f"Warning: could not clean up temp files: {e}", file=sys.stderr)

    print("Done.")


if __name__ == "__main__":
    main() 