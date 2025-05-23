from __future__ import annotations

from typing import Tuple, List

import torch
import torchaudio
from speechbrain.pretrained.interfaces import foreign_class

MODEL_SOURCE = "Jzuluaga/accent-id-commonaccent_xlsr-en-english"


class AccentClassifier:
    """Wraps a SpeechBrain accent classification model."""

    def __init__(self, device: str | None = None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.classifier = foreign_class(
            source=MODEL_SOURCE,
            pymodule_file="custom_interface.py",
            classname="CustomEncoderWav2vec2Classifier",
            run_opts={"device": device},
        )

    def classify(self, wav_path: str) -> Tuple[str, float, List[Tuple[str, float]]]:
        """Classify an audio file.

        Returns
        -------
        Tuple containing:
        1. predicted accent label
        2. confidence score (probability)
        3. list of (label, probability) for top 5 accents
        """
        out_prob, score, index, text_lab = self.classifier.classify_file(wav_path)
        # out_prob is tensor of probabilities shape (n_classes,)
        probs = out_prob.squeeze().tolist()
        label_probs = list(zip(self.classifier.hparams.label_encoder.decode_ndim(range(len(probs))), probs))
        label_probs.sort(key=lambda x: x[1], reverse=True)
        top5 = label_probs[:5]
        return text_lab, float(score), top5 