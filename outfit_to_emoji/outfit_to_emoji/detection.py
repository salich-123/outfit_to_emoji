from __future__ import annotations

from typing import List, Tuple

import numpy as np
from PIL import Image

try:
    from tensorflow.keras.applications.mobilenet_v2 import (
        MobileNetV2,
        decode_predictions,
        preprocess_input,
    )
    from tensorflow.keras.preprocessing import image as keras_image
    TENSORFLOW_AVAILABLE = True
except Exception:  # pragma: no cover - optional dep guard
    TENSORFLOW_AVAILABLE = False
    MobileNetV2 = None  # type: ignore
    decode_predictions = None  # type: ignore
    preprocess_input = None  # type: ignore
    keras_image = None  # type: ignore


def load_imagenet_model():
    if not TENSORFLOW_AVAILABLE:
        raise RuntimeError(
            "TensorFlow/Keras not available. Please install tensorflow to run detection."
        )
    return MobileNetV2(weights="imagenet")


def _prepare_image(img: Image.Image) -> np.ndarray:
    img_resized = img.resize((224, 224))
    x = np.array(img_resized)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


# A small set of ImageNet synsets roughly associated with clothing/outfit cues
CLOTHING_KEYWORDS = {
    "jersey",
    "T-shirt",
    "suit",
    "tie",
    "bow_tie",
    "maillot",
    "poncho",
    "fur_coat",
    "Cardigan",
    "jean",
    "trench_coat",
    "gown",
    "kimono",
    "miniskirt",
    "cowboy_boot",
    "sandals",
    "sweatshirt",
    "sunglasses",
    "hat",
    "cap",
    "backpack",
    "handbag",
    "wallet",
    "bikini",
    "abaya",
    "cloak",
}


def _filter_clothing(preds: List[Tuple[str, str, float]], top_k: int = 5) -> List[Tuple[str, float]]:
    clothing: List[Tuple[str, float]] = []
    for (_, label, prob) in preds:
        for key in CLOTHING_KEYWORDS:
            if key.lower() in label.lower():
                clothing.append((label.replace("_", " "), float(prob)))
                break
    clothing.sort(key=lambda x: x[1], reverse=True)
    return clothing[:top_k]


def detect_clothing_items(img: Image.Image, model, top_k: int = 5) -> List[Tuple[str, float]]:
    """Return [(label, probability)] for clothing-like ImageNet classes.

    Falls back to empty list on errors.
    """
    try:
        x = _prepare_image(img)
        preds = model.predict(x)
        decoded = decode_predictions(preds, top=10)[0]
        return _filter_clothing(decoded, top_k=top_k)
    except Exception:
        return []



