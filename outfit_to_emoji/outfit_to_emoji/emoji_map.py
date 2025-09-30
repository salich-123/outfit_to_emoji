from __future__ import annotations

from typing import Dict, List, Tuple

from .colors import NamedColor


ITEM_TO_EMOJI: Dict[str, str] = {
    "jersey": "🎽",
    "t-shirt": "👕",
    "tee": "👕",
    "shirt": "👔",
    "suit": "🤵",
    "tie": "👔",
    "bow tie": "🤵",
    "poncho": "🧥",
    "fur coat": "🧥",
    "cardigan": "🧥",
    "coat": "🧥",
    "jacket": "🧥",
    "hoodie": "🧥",
    "jean": "👖",
    "jeans": "👖",
    "trousers": "👖",
    "pants": "👖",
    "trench coat": "🧥",
    "gown": "👗",
    "kimono": "👘",
    "miniskirt": "👗",
    "skirt": "👗",
    "dress": "👗",
    "shorts": "🩳",
    "cowboy boot": "👢",
    "boot": "👢",
    "sneaker": "👟",
    "shoe": "👟",
    "heels": "👠",
    "high heel": "👠",
    "sandal": "🩴",
    "sunglasses": "🕶️",
    "hat": "👒",
    "cap": "🧢",
    "backpack": "🎒",
    "handbag": "👜",
    "wallet": "👛",
    "bikini": "👙",
    "abaya": "🧕",
    "cloak": "🧥",
    "sweatshirt": "🧥",
    "scarf": "🧣",
    "glove": "🧤",
    "socks": "🧦",
    "umbrella": "🌂",
    "watch": "⌚",
    "necklace": "📿",
    "earring": "📿",
}


COLOR_TO_EMOJIS: Dict[str, List[str]] = {
    "black": ["🖤", "🕶️", "🦂"],
    "white": ["🤍", "🕊️", "❄️"],
    "red": ["❤️", "🍎", "🌹"],
    "orange": ["🧡", "🧡", "🍊"],
    "yellow": ["💛", "🌟", "🌼"],
    "green": ["💚", "🍀", "🌿"],
    "blue": ["💙", "🌊", "🧊"],
    "purple": ["💜", "🔮", "🍇"],
    "brown": ["🟤", "🪵", "🥨"],
    "gray": ["🩶", "🌫️", "🪨"],
    "pink": ["💗", "🌸", "🩷"],
}

def get_color_emoji(color_name: str, index: int = 0) -> str:
    options = COLOR_TO_EMOJIS.get(color_name, ["❓"])
    if not options:
        return "❓"
    return options[index % len(options)]


def normalize_item_label(label: str) -> str:
    return label.lower().replace("_", " ")


LOCATION_EMOJIS: List[str] = [
    "🏙️",  # city
    "🏖️",  # beach
    "🏔️",  # mountains
    "🛍️",  # shopping
    "🎉",  # party/event
    "🏠",  # home/indoor
]

def get_location_emoji(items: List[Tuple[str, float]], colors: List[NamedColor]) -> str:
    # Deterministic but varied choice based on simple hash of inputs
    base = len(items) * 3 + len(colors) * 5
    return LOCATION_EMOJIS[base % len(LOCATION_EMOJIS)]


def map_items_and_colors_to_emojis(
    items: List[Tuple[str, float]], colors: List[NamedColor]
) -> Tuple[str, Dict[str, List[str]]]:
    item_emojis: List[str] = []
    for label, prob in items:
        key = normalize_item_label(label)
        # find best mapping by substring match
        chosen = None
        for k, e in ITEM_TO_EMOJI.items():
            if k in key:
                chosen = e
                break
        if chosen and prob >= 0.10:  # low threshold to include more fun
            item_emojis.append(chosen)

    color_emojis: List[str] = []
    for i, c in enumerate(colors[:3]):
        color_emojis.append(get_color_emoji(c.name, i))

    # Add expressive location emoji instead of a pin
    location_emoji = get_location_emoji(items, colors)

    # Construct a fun string: items, colors, then location
    parts = item_emojis + color_emojis + [location_emoji]
    final = " ".join(parts)
    return final, {"items": item_emojis, "colors": color_emojis, "location": [location_emoji]}

def render_color_emoji_chips(colors: List[NamedColor]) -> str:
    chips: List[str] = []
    for i, c in enumerate(colors):
        emoji = get_color_emoji(c.name, i)
        chips.append(
            f"<span class='color-badge'>{emoji} <span style='text-transform:capitalize'>{c.name}</span></span>"
        )
    return "".join(chips)



