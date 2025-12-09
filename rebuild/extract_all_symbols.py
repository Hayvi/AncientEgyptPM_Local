#!/usr/bin/env python3
"""
Extract ALL slot symbols from the texture sheets.
Coordinates from HAR file analysis.
"""
from PIL import Image
import os

ASSETS_DIR = "/home/supa/test22/AncientEgyptPM_Local/rebuild/assets"
SPRITES_DIR = "/home/supa/test22/AncientEgyptPM_Local/rebuild/sprites"

# All symbol definitions from HAR analysis
# Format: (output_name, texture_file, x, y, width, height)
SYMBOLS = [
    # Symbol 01 - Cleopatra/Pharaoh (Wild)
    # From d382e624bd6f17e43b3be7022061a3ca.png - s_symbol01_win_02
    ("symbol01.png", "d382e624bd6f17e43b3be7022061a3ca.png", 436, 0, 346, 295),
    
    # Symbol 02 - Anubis (high value)
    # From 82e05b072d00acf4bb721c2c3773a815.png - s_symbol02_win_02
    ("symbol02_anubis.png", "82e05b072d00acf4bb721c2c3773a815.png", 425, 0, 340, 300),
    
    # Card symbols from 20d7ad009ff2a804684180e437657b33.png
    # These are the gold card symbols (A, K, Q, J, 10, 9)
    
    # Symbol 03 - A (Ace) - s_symbol03_win_00: x=1680, y=770, w=273, h=264
    ("symbol_A.png", "20d7ad009ff2a804684180e437657b33.png", 1680, 770, 273, 264),
    
    # Symbol 04 - K (King) - s_symbol04_win_00: x=1290, y=946, w=276, h=241
    ("symbol_K.png", "20d7ad009ff2a804684180e437657b33.png", 1290, 946, 276, 241),
    
    # Symbol 05 - Q (Queen) - s_symbol05_win_00: x=690, y=290, w=194, h=229
    ("symbol_Q.png", "20d7ad009ff2a804684180e437657b33.png", 690, 290, 194, 229),
    
    # Symbol 06 - J (Jack) - s_symbol06_win_00: x=734, y=849, w=237, h=172
    ("symbol_J.png", "20d7ad009ff2a804684180e437657b33.png", 734, 849, 237, 172),
    
    # Symbol 07 - 10 - s_symbol07_win_00: x=526, y=672, w=171, h=159
    ("symbol_10.png", "20d7ad009ff2a804684180e437657b33.png", 526, 672, 171, 159),
    
    # Symbol 08 - 9 - s_symbol08_win_00: x=185, y=179, w=183, h=167
    ("symbol_9.png", "20d7ad009ff2a804684180e437657b33.png", 185, 179, 183, 167),
    
    # Symbol 09 - might be another card - s_symbol09_win_00: x=204, y=2, w=199, h=177
    ("symbol09.png", "20d7ad009ff2a804684180e437657b33.png", 204, 2, 199, 177),
    
    # Symbol 10 - from 790a6ca683676d443a6b84175a48333b.png - s_symbol10_win_00: x=169, y=521, w=167, h=171
    ("symbol10.png", "790a6ca683676d443a6b84175a48333b.png", 169, 521, 167, 171),
    
    # Symbol 11 - from 790a6ca683676d443a6b84175a48333b.png - s_symbol11_win_00: x=0, y=175, w=199, h=171
    ("symbol11.png", "790a6ca683676d443a6b84175a48333b.png", 0, 175, 199, 171),
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
    print("=== Extracting All Slot Symbols ===\n")
    
    for name, tex, x, y, w, h in SYMBOLS:
        extract_sprite(tex, x, y, w, h, name)
    
    print("\n✓ Done!")

if __name__ == "__main__":
    main()
