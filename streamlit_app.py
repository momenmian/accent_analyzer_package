from __future__ import annotations

import sys
import types

# ---------------------------------------------------------------------------
# WORKAROUND: Stub-out torch.classes so Streamlit's file-watcher does not crash
# ---------------------------------------------------------------------------
# Streamlit's LocalSourcesWatcher iterates over sys.modules, and for each module
# it tries to access ``module.__path__._path`` (PEP-420 namespace packages).
# ``torch.classes`` is *not* a real module and lacks these attributes, causing
# RuntimeErrors like:
#   RuntimeError: Tried to instantiate class '__path__._path', but it does not exist!
# We pre-register a dummy module under 'torch.classes' that *does* expose the
# expected attributes so the watcher can inspect it safely.
if "torch.classes" not in sys.modules or not isinstance(sys.modules["torch.classes"], types.ModuleType):
    stub_mod = types.ModuleType("torch.classes")
    stub_mod.__path__ = types.SimpleNamespace(_path=[])  # minimal namespace-pkg API
    sys.modules["torch.classes"] = stub_mod

# ---------------------------------------------------------------------------

import streamlit as st
from pathlib import Path

try:
    # When executed as module (python -m accent_analyzer.streamlit_app)
    from .audio_utils import download_video, extract_audio  # type: ignore
    from .accent_model import AccentClassifier  # type: ignore
except ImportError:
    try:
        # Fallback: executed as a script from inside the package directory
        from audio_utils import download_video, extract_audio  # type: ignore
        from accent_model import AccentClassifier  # type: ignore
    except ImportError:
        # Last resort: absolute import when working directory is project root
        from audio_utils import download_video, extract_audio  # type: ignore
        from accent_model import AccentClassifier  # type: ignore

try:
    # Modern Streamlit
    from streamlit.runtime.caching import cache_resource as _cache_res  # type: ignore
except (ImportError, ModuleNotFoundError):
    # Legacy fallback
    _cache_res = None

if hasattr(st, "cache_resource"):
    def _cache(func):  # type: ignore
        return st.cache_resource(show_spinner=False)(func)
else:
    def _cache(func):  # type: ignore
        if hasattr(st, "experimental_singleton"):
            return st.experimental_singleton(func)
        return func  # no-op fallback


@_cache
def get_classifier():
    """Load and cache the accent classifier model."""
    return AccentClassifier()


def main() -> None:
    st.set_page_config(page_title="Accent Analyzer", page_icon="🔊")
    st.title("🔍 English Accent Analyzer")
    st.markdown(
        """
        Paste the public URL to a **Loom** recording, direct **.mp4** file, or **YouTube** video.
        The app will download the video, extract the audio track, and predict the speaker's English accent.
        """
    )

    url = st.text_input("Video URL", placeholder="https://...")

    analyze_btn = st.button("Analyze", type="primary", disabled=not url.strip())

    if analyze_btn:
        if not url.strip():
            st.error("Please enter a valid URL.")
            st.stop()

        # 1. Download video
        try:
            with st.spinner("Downloading video..."):
                video_path = download_video(url.strip())
        except Exception as e:
            st.error(f"Failed to download video: {e}")
            st.stop()

        # 2. Extract audio
        try:
            with st.spinner("Extracting audio track..."):
                audio_path = extract_audio(video_path)
        except Exception as e:
            st.error(f"Failed to extract audio: {e}")
            cleanup_files(video_path)
            st.stop()

        # 3. Classify accent
        classifier = get_classifier()
        try:
            with st.spinner("Classifying accent (this can take ~1 min on first run)..."):
                label, score, top5 = classifier.classify(str(audio_path))
        except Exception as e:
            st.error(f"Failed to classify accent: {e}")
            cleanup_files(video_path, audio_path)
            st.stop()

        # Display result
        st.success("Analysis complete!")
        st.subheader("Predicted Accent")
        st.write(f"**{label}** – {score:.2%} confidence")

        st.subheader("Top 5 accents")
        for acc, prob in top5:
            st.write(f"{acc}: {prob:.2%}")

        # 4. Cleanup temporary files
        cleanup_files(video_path, audio_path)



def cleanup_files(*paths: Path | str | None) -> None:
    """Silently remove temporary files created during processing."""
    for p in paths:
        if p is None:
            continue
        try:
            Path(p).unlink(missing_ok=True)
        except Exception:
            # Just warn in the app sidebar; do not crash the UI.
            print(f"[WARN] Could not delete temp file: {p}", file=sys.stderr)


# ---- Workaround for Streamlit + PyTorch compatibility ----------------------
# (duplicate workaround removed)
# ---- End workaround --------------------------------------------------------


if __name__ == "__main__":
    main() 