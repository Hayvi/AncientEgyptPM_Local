#!/usr/bin/env python3
"""
Extract individual sprites from sprite sheets
"""
from PIL import Image
import os

ASSETS_DIR = "assets"
OUTPUT_DIR = "sprites"

# Sprite definitions from HAR analysis
# Format: (sprite_name, source_png, x, y, width, height)
SPRITES = [
    # Background - efca029b5ef41654da3e3a712c28e506.png contains s_bg
    ("bg", "efca029b5ef41654da3e3a712c28e506.png", 0, 0, 1777, 999),
    
    # Columns - 835313e3eadfa7b4187f44724febc8c2.png contains s_column
    ("column", "835313e3eadfa7b4187f44724febc8c2.png", 1093, 157, 234, 888),
    
    # Reels frame - a3eb2babeac67a04cb04c41f4ab1dae2.png contains s_reels_frame_normal
    ("reels_frame", "a3eb2babeac67a04cb04c41f4ab1dae2.png", 0, 2, 1509, 823),
    
    # Title - 2f7fc52209ccd5b4d821281ff6932a12.png contains s_title
    ("title", "2f7fc52209ccd5b4d821281ff6932a12.png", 0, 0, 924, 109),
    
    # Main symbol (Cleopatra/Pharaoh) - 23bfabb9d5ef72343b051b518fe1a995.png
    ("symbol01", "23bfabb9d5ef72343b051b518fe1a995.png", 0, 1572, 434, 435),
    
    # Card symbols - 20d7ad009ff2a804684180e437657b33.png
    ("symbol_Q", "20d7ad009ff2a804684180e437657b33.png", 0, 539, 298, 290),  # symbol03
    ("symbol_J", "20d7ad009ff2a804684180e437657b33.png", 0, 298, 274, 239),  # symbol04
    ("symbol_10", "20d7ad009ff2a804684180e437657b33.png", 615, 612, 183, 217),  # symbol05
    ("symbol_9", "20d7ad009ff2a804684180e437657b33.png", 583, 215, 233, 163),  # symbol06
    ("symbol_K", "20d7ad009ff2a804684180e437657b33.png", 158, 2, 153, 141),  # symbol07
    ("symbol_A", "20d7ad009ff2a804684180e437657b33.png", 653, 61, 165, 152),  # symbol08
    
    # Scarab/Book symbols - try different textures
    ("symbol02_scarab", "d382e624bd6f17e43b3be7022061a3ca.png", 0, 0, 300, 300),
    ("symbol_ankh", "82e05b072d00acf4bb721c2c3773a815.png", 0, 0, 300, 300),
    
    # Fire frames - cdc881ba8688bc94fa31907e495e5db8.png or 1adb931445255fa459f1947dbd64864d.png
    ("fire_00", "cdc881ba8688bc94fa31907e495e5db8.png", 464, 2, 462, 456),
    ("fire_01", "cdc881ba8688bc94fa31907e495e5db8.png", 0, 460, 462, 456),
    ("fire_02", "cdc881ba8688bc94fa31907e495e5db8.png", 928, 2, 462, 456),
]

def extract_sprites():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for sprite_name, source_file, x, y, w, h in SPRITES:
        source_path = os.path.join(ASSETS_DIR, source_file)
        if not os.path.exists(source_path):
            print(f"Source not found: {source_file}")
            continue
        
        try:
            img = Image.open(source_path)
            # Crop the sprite
            sprite = img.crop((x, y, x + w, y + h))
            output_path = os.path.join(OUTPUT_DIR, f"{sprite_name}.png")
            sprite.save(output_path)
            print(f"Extracted: {sprite_name} ({w}x{h})")
        except Exception as e:
            print(f"Error extracting {sprite_name}: {e}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    extract_sprites()
