#!/usr/bin/env python3
"""
Extract slot symbols from the texture sheets we have.
The idle symbols aren't in the HAR, but we have animation frames.
We'll use the first win frame as the symbol image.
"""
from PIL import Image
import os

ASSETS_DIR = "/home/supa/test22/AncientEgyptPM_Local/rebuild/assets"
SPRITES_DIR = "/home/supa/test22/AncientEgyptPM_Local/rebuild/sprites"

# Symbol mappings from HAR analysis
# Format: (output_name, texture_file, x, y, width, height)
SYMBOLS = [
    # Symbol 01 - Cleopatra/Pharaoh (from d382e624bd6f17e43b3be7022061a3ca.png)
    # s_symbol01_win_02 is a good frame: x=436, y=0, w=346, h=295
    ("symbol01.png", "d382e624bd6f17e43b3be7022061a3ca.png", 436, 0, 346, 295),
    
    # Symbol 02 - Anubis (from 82e05b072d00acf4bb721c2c3773a815.png)
    # s_symbol02_win_02: x=425, y=0, w=340, h=?
    ("symbol02_anubis.png", "82e05b072d00acf4bb721c2c3773a815.png", 425, 0, 340, 300),
    
    # Symbol 03-11 are card symbols from 20d7ad009ff2a804684180e437657b33.png
    # But those are treasure chests! Let me check other textures...
    
    # Let's try efca029b5ef41654da3e3a712c28e506.png for more symbols
    # And a3eb2babeac67a04cb04c41f4ab1dae2.png
]

# Card symbols from 20d7ad009ff2a804684180e437657b33.png (these are treasure chests, not what we want)
# We need to find the actual card symbols (A, K, Q, J, 10, 9) in gold

# Let me check what's in each texture by extracting sample regions
TEXTURE_SAMPLES = [
    # Try different regions from each texture to find the card symbols
    ("sample_efca_1.png", "efca029b5ef41654da3e3a712c28e506.png", 0, 0, 400, 400),
    ("sample_efca_2.png", "efca029b5ef41654da3e3a712c28e506.png", 400, 0, 400, 400),
    ("sample_efca_3.png", "efca029b5ef41654da3e3a712c28e506.png", 800, 0, 400, 400),
    ("sample_a3eb_1.png", "a3eb2babeac67a04cb04c41f4ab1dae2.png", 0, 0, 400, 400),
    ("sample_a3eb_2.png", "a3eb2babeac67a04cb04c41f4ab1dae2.png", 400, 0, 400, 400),
    ("sample_b243_1.png", "b24365832962afc4c99ac17a0fff1db6.png", 0, 0, 400, 400),
    ("sample_bfd9_1.png", "bfd97fe4b826f8f46b85743fa3d3687b.png", 0, 0, 400, 400),
]

def extract_sprite(texture_file, x, y, w, h, output_name):
    """Extract a sprite from a texture"""
    texture_path = os.path.join(ASSETS_DIR, texture_file)
    if not os.path.exists(texture_path):
        print(f"  ✗ Texture not found: {texture_file}")
        return False
    
    try:
        img = Image.open(texture_path)
        # Ensure we don't go out of bounds
        x2 = min(x + w, img.width)
        y2 = min(y + h, img.height)
        sprite = img.crop((x, y, x2, y2))
        
        output_path = os.path.join(SPRITES_DIR, output_name)
        sprite.save(output_path)
        print(f"  ✓ {output_name} ({sprite.width}x{sprite.height})")
        return True
    except Exception as e:
        print(f"  ✗ {output_name}: {e}")
        return False

def main():
    print("=== Extracting Slot Symbols ===\n")
    
    print("Main symbols:")
    for name, tex, x, y, w, h in SYMBOLS:
        extract_sprite(tex, x, y, w, h, name)
    
    print("\nTexture samples (to find card symbols):")
    for name, tex, x, y, w, h in TEXTURE_SAMPLES:
        extract_sprite(tex, x, y, w, h, name)
    
    print("\n✓ Done! Check the samples to find the card symbols.")

if __name__ == "__main__":
    main()
