## Outfit → Emoji Converter

Turn outfit photos into a fun emoji string. Upload a photo or use your webcam. The app detects clothing-related cues with MobileNetV2 (ImageNet) and extracts dominant colors, then maps them into emojis.

### Features
- Upload or webcam capture
- Clothing cue detection via MobileNetV2
- Dominant color extraction (KMeans)
- Emoji mapping for items and colors
- Copy result to clipboard

### Installation
1. Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```
2. Install dependencies
```bash
pip install -r requirements.txt
```

### Run
```bash
streamlit run app.py
```

Open the local URL in your browser. Upload a photo or use your webcam, then copy the emoji fit.

### Notes
- First run will download MobileNetV2 weights (Internet required).
- If TensorFlow install is heavy for your environment, you can switch to a different Keras-compatible lightweight model by editing `outfit_to_emoji/detection.py`.

### Project Structure
```
app.py
outfit_to_emoji/
  __init__.py
  detection.py
  colors.py
  emoji_map.py
requirements.txt
README.md
```




