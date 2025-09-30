import io
from typing import List, Tuple

import streamlit as st
from PIL import Image

from outfit_to_emoji.detection import detect_clothing_items, load_imagenet_model
from outfit_to_emoji.colors import extract_dominant_colors, render_color_badges
from outfit_to_emoji.emoji_map import map_items_and_colors_to_emojis, render_color_emoji_chips


st.set_page_config(
    page_title="Outfit → Emoji Converter",
    page_icon="🧿",
    layout="centered",
)

# Add custom CSS (simplified, no big gradient boxes; square color badges)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .main { font-family: 'Inter', sans-serif; }
    .stApp { background: #0f172a; }
    .main-container { padding: 12px 0; }
    .title-container { text-align:center; margin-bottom: 12px; }
    .result-card { background: transparent; padding: 0; margin: 10px 0; }
    .emoji-display { font-size: 2.2rem; text-align:center; padding: 8px; color: #e2e8f0; }
    .spinner-container { display:flex; justify-content:center; padding: 8px; }
    .loading-spinner { width: 28px; height: 28px; border: 3px solid rgba(255,255,255,0.15); border-top: 3px solid #22d3ee; border-radius: 50%; animation: spin 1s linear infinite; }
    @keyframes spin { 0% { transform: rotate(0deg);} 100% { transform: rotate(360deg);} }
    /* squared color badges (overrides) */
    .color-badge { display:inline-flex; align-items:center; gap:8px; margin:4px 10px 4px 0; padding:6px 10px; border-radius:8px; border:1px solid #1f2937; background:#0b1220; color:#cbd5e1; }
    /* copy area */
    .copy-wrap { display:flex; gap:8px; align-items:center; background:#0b1220; padding:12px; border-radius:10px; border:1px solid #1f2937; }
    .copy-input { flex:1; padding:10px; font-size:16px; background:#0b1220; color:#e2e8f0; border:1px solid #1f2937; border-radius:8px; }
    .copy-button { background:#22d3ee; color:#0b1220; border:none; border-radius:8px; padding:10px 14px; cursor:pointer; font-weight:600; }
    .copy-button:hover { filter: brightness(1.1); }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def get_model():
    return load_imagenet_model()


def read_image_from_bytes(uploaded_bytes: bytes) -> Image.Image:
    return Image.open(io.BytesIO(uploaded_bytes)).convert("RGB")


def main():
    # Main container (clean)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Animated title
    st.markdown('<div class="title-container">', unsafe_allow_html=True)
    st.title("🎭 Outfit → Emoji Converter")
    st.markdown("### ✨ Upload or capture your outfit photo; we'll turn it into emojis ✨")
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("🔍 How it works", expanded=False):
        st.markdown(
            "- We use a pre-trained CNN (MobileNetV2) to detect clothing-related cues.\n"
            "- We extract dominant colors from the image.\n"
            "- We map items and colors into a fun emoji string.")

    # Image input options with animations
    st.subheader("📸 Choose Your Input Method")
    
    input_method = st.radio(
        "How would you like to provide your outfit photo?",
        ["📁 Upload from computer", "📷 Take a photo with camera"],
        horizontal=True
    )
    
    image: Image.Image | None = None
    
    if input_method == "📁 Upload from computer":
        uploaded_file = st.file_uploader(
            "📁 Upload a photo of your outfit", 
            type=["jpg", "jpeg", "png"],
            help="Choose a clear photo of your outfit"
        )
        if uploaded_file is not None:
            image = read_image_from_bytes(uploaded_file.read())
    
    else:  # Camera option
        st.info("📷 Click below to open your camera and take a snapshot")
        camera_img = st.camera_input(
            "📷 Take a snapshot of your outfit",
            help="Position yourself in the camera view and click 'Take a snapshot' when ready"
        )
        if camera_img is not None:
            image = read_image_from_bytes(camera_img.getvalue())

    if image is None:
        st.info("👆 Please upload a photo or take a snapshot to get started!")
        return

    # Photo display (clean)
    st.subheader("📸 Your Photo")
    st.image(image, caption="Input outfit photo", use_column_width=True)

    # Animated loading spinner
    st.markdown("""
    <div class="spinner-container"><div class="loading-spinner"></div></div>
    <div style="text-align:center; color:#cbd5e1;">Analyzing your outfit…</div>
    """, unsafe_allow_html=True)

    with st.spinner(""):
        model = get_model()
        detected_items: List[Tuple[str, float]] = detect_clothing_items(image, model=model, top_k=5)
        dominant = extract_dominant_colors(image, num_colors=4)

    item_labels = [f"{label} ({prob:.0%})" for label, prob in detected_items]

    # Results (clean)
    st.subheader("👕 Detected Items")
    if item_labels:
        st.write(", ".join(item_labels))
    else:
        st.write("No strong clothing cues detected; we'll still try colors! 🎨")

    st.subheader("🎨 Dominant Colors")
    # Show color emojis (not shapes)
    st.markdown(render_color_emoji_chips(dominant), unsafe_allow_html=True)

    emoji_str, emoji_parts = map_items_and_colors_to_emojis(detected_items, dominant)
    
    # Emoji display with float + pulsing location
    st.subheader("😊 Your Emoji Fit")
    location_html = ""
    if emoji_parts.get("location"):
        loc = emoji_parts["location"][0]
        location_html = f"<span style='display:inline-block; animation: pulseGlow 1.6s ease-in-out infinite;'>{loc}</span>"
    st.markdown(
        f"""
        <div class='emoji-display' style="animation: floatY 2s ease-in-out infinite;">
            {" ".join(emoji_parts.get('items', []))} {" ".join(emoji_parts.get('colors', []))} {location_html}
        </div>
        <style>
        @keyframes floatY {{ 0%{{transform: translateY(0);}} 50%{{transform: translateY(-4px);}} 100%{{transform: translateY(0);}} }}
        @keyframes pulseGlow {{ 0%{{filter:brightness(1);}} 50%{{filter:brightness(1.4);}} 100%{{filter:brightness(1);}} }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Enhanced copy-to-clipboard with animation
    st.components.v1.html(
        f"""
        <div class='copy-wrap'>
          <input id='emojiOutput' class='copy-input' value="{emoji_str}" readonly />
          <button class='copy-button' onclick="navigator.clipboard.writeText(document.getElementById('emojiOutput').value); this.innerHTML='✅ Copied!'; setTimeout(() => this.innerHTML='📋 Copy', 1600)">📋 Copy</button>
        </div>
        """,
        height=70,
    )

    with st.expander("🔧 Debug details", expanded=False):
        st.json(
            {
                "items": [{"label": l, "prob": float(p)} for l, p in detected_items],
                "colors": [
                    {"name": c.name, "rgb": c.rgb, "hex": c.hex}
                    for c in dominant
                ],
                "emoji_parts": emoji_parts,
            }
        )
    st.caption("✨ Thanks for using Outfit → Emoji Converter! Share your emoji fit! ✨")
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()



