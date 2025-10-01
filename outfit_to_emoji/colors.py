from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


@dataclass
class NamedColor:
    name: str
    rgb: Tuple[int, int, int]

    @property
    def hex(self) -> str:
        r, g, b = self.rgb
        return f"#{r:02x}{g:02x}{b:02x}"


BASIC_COLOR_NAMES = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (220, 20, 60),
    "orange": (255, 140, 0),
    "yellow": (255, 215, 0),
    "green": (34, 139, 34),
    "blue": (30, 144, 255),
    "purple": (138, 43, 226),
    "brown": (139, 69, 19),
    "gray": (128, 128, 128),
    "pink": (255, 105, 180),
}


def _closest_color_name(rgb: Tuple[int, int, int]) -> str:
    arr = np.array(rgb)
    min_dist = float("inf")
    best = "unknown"
    for name, ref in BASIC_COLOR_NAMES.items():
        dist = np.linalg.norm(arr - np.array(ref))
        if dist < min_dist:
            min_dist = dist
            best = name
    return best


def extract_dominant_colors(img: Image.Image, num_colors: int = 4) -> List[NamedColor]:
    small = img.convert("RGB").resize((128, 128))
    data = np.array(small).reshape(-1, 3)

    n_clusters = max(1, min(num_colors, len(np.unique(data, axis=0))))
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    labels = kmeans.fit_predict(data)
    centers = kmeans.cluster_centers_.astype(int)

    # Order by cluster size descending
    counts = np.bincount(labels)
    order = np.argsort(counts)[::-1]
    ordered_centers = centers[order]

    results: List[NamedColor] = []
    for c in ordered_centers[:num_colors]:
        rgb = (int(c[0]), int(c[1]), int(c[2]))
        results.append(NamedColor(name=_closest_color_name(rgb), rgb=rgb))
    return results


def render_color_badges(colors: List[NamedColor]) -> str:
    badges = []
    for c in colors:
        badges.append(
            f"<span style='display:inline-flex;align-items:center;gap:8px;margin:4px 10px 4px 0;padding:6px 10px;border-radius:10px;border:1px solid #e5e7eb;background:rgba(255,255,255,0.9)'>"
            f"<span style='display:inline-block;width:18px;height:18px;background:{c.hex};border:1px solid #d1d5db; clip-path: polygon(25% 6.7%, 75% 6.7%, 100% 50%, 75% 93.3%, 25% 93.3%, 0% 50%);'></span>"
            f"<span style='font-size:0.95rem;text-transform:capitalize'>{c.name}</span>"
            f"</span>"
        )
    return "".join(badges)



