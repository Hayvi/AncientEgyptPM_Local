#!/usr/bin/env python3
"""
Create correctly named symbol sprites from the texture sheets.
Based on HAR analysis:
- 20d7ad009ff2a804684180e437657b33.png contains card symbols (s_symbol03-11)
- 23bfabb9d5ef72343b051b518fe1a995.png contains Pharaoh/Cleopatra transforms
"""
from PIL import Image
import os

ASSETS_DIR = "/home/supa/test22/AncientEgyptPM_Local/rebuild/assets"
SPRITES_DIR = "/home/supa/test22/AncientEgyptPM_Local/rebuild/sprites"

# Card symbols texture - 20d7ad009ff2a804684180e437657b33.png
# These are the playing card symbols (A, K, Q, J, 10, 9) in Ancient Egypt style
CARD_TEXTURE = "20d7ad009ff2a804684180e437657b33.png"

# Symbol coordinates from HAR (s_symbol03-11)
# Looking at typical slot games, higher numbers = lower value cards
CARD_SYMBOLS = {
    # s_symbol03 is likely the highest card (A) - largest sprite
    'symbol_A.png': {'x': 0, 'y': 539, 'w': 298, 'h': 290},
    # s_symbol04 - K
    'symbol_K.png': {'x': 0, 'y': 298, 'w': 274, 'h': 239},
    # s_symbol05 - Q  
    'symbol_Q.png': {'x': 615, 'y': 612, 'w': 183, 'h': 217},
    # s_symbol06 - J
    'symbol_J.png': {'x': 583, 'y': 215, 'w': 233, 'h': 163},
    # s_symbol07 - 10
    'symbol_10.png': {'x': 158, 'y': 2, 'w': 153, 'h': 141},
    # s_symbol08 - 9
    'symbol_9.png': {'x': 653, 'y': 61, 'w': 165, 'h': 152},
}

# Pharaoh texture - 23bfabb9d5ef72343b051b518fe1a995.png
PHARAOH_TEXTURE = "23bfabb9d5ef72343b051b518fe1a995.png"

PHARAOH_SYMBOL = {
    'symbol01.png': {'x': 0, 'y': 1572, 'w': 434, 'h': 435},
}

def extract_sprite(texture_path, coords, output_name):
    """Extract a single sprite from a texture"""
    try:
        img = Image.open(texture_path)
        x, y, w, h = coords['x'], coords['y'], coords['w'], coords['h']
        
        # Crop the sprite
        sprite = img.crop((x, y, x + w, y + h))
        
        # Save
        output_path = os.path.join(SPRITES_DIR, output_name)
        sprite.save(output_path)
        print(f"  ✓ {output_name} ({w}x{h})")
        return True
    except Exception as e:
        print(f"  ✗ {output_name}: {e}")
        return False

def main():
    print("=== Creating Correct Symbol Sprites ===\n")
    
    # Extract card symbols
    print(f"From {CARD_TEXTURE}:")
    texture_path = os.path.join(ASSETS_DIR, CARD_TEXTURE)
    if os.path.exists(texture_path):
        for name, coords in CARD_SYMBOLS.items():
            extract_sprite(texture_path, coords, name)
    else:
        print(f"  ✗ Texture not found!")
    
    # Extract pharaoh
    print(f"\nFrom {PHARAOH_TEXTURE}:")
    texture_path = os.path.join(ASSETS_DIR, PHARAOH_TEXTURE)
    if os.path.exists(texture_path):
        for name, coords in PHARAOH_SYMBOL.items():
            extract_sprite(texture_path, coords, name)
    else:
        print(f"  ✗ Texture not found!")
    
    print("\n✓ Done! Sprites saved to:", SPRITES_DIR)

if __name__ == "__main__":
    main()
