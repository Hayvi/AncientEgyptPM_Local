#!/usr/bin/env python3
"""
Fix sprite extraction - extract correct symbols from sprite sheets
"""
from PIL import Image
import os

ASSETS_DIR = "/home/supa/test22/AncientEgyptPM_Local/rebuild/assets"
SPRITES_DIR = "/home/supa/test22/AncientEgyptPM_Local/rebuild/sprites"

# Texture file mappings (from HAR analysis)
# 20d7ad009ff2a804684180e437657b33.png - Card symbols (s_symbol03-11)
# 23bfabb9d5ef72343b051b518fe1a995.png - Pharaoh transforms (s_symbol01)

# Symbol definitions with correct coordinates from find_sprites.py output
CARD_SYMBOLS = {
    # From texture 20d7ad009ff2a804684180e437657b33.png
    'texture': '20d7ad009ff2a804684180e437657b33.png',
    'sprites': {
        'symbol03': {'x': 0, 'y': 539, 'w': 298, 'h': 290},   # Likely A or high card
        'symbol04': {'x': 0, 'y': 298, 'w': 274, 'h': 239},   # K
        'symbol05': {'x': 615, 'y': 612, 'w': 183, 'h': 217}, # Q
        'symbol06': {'x': 583, 'y': 215, 'w': 233, 'h': 163}, # J
        'symbol07': {'x': 158, 'y': 2, 'w': 153, 'h': 141},   # 10
        'symbol08': {'x': 653, 'y': 61, 'w': 165, 'h': 152},  # 9
        'symbol09': {'x': 276, 'y': 145, 'w': 192, 'h': 172}, # Extra
        'symbol10': {'x': 0, 'y': 136, 'w': 156, 'h': 160},   # Extra
        'symbol11': {'x': 470, 'y': 60, 'w': 181, 'h': 153},  # Extra
    }
}

PHARAOH_SYMBOLS = {
    # From texture 23bfabb9d5ef72343b051b518fe1a995.png
    'texture': '23bfabb9d5ef72343b051b518fe1a995.png',
    'sprites': {
        'symbol01': {'x': 0, 'y': 1572, 'w': 434, 'h': 435},  # Pharaoh/Cleopatra
    }
}

def extract_sprite(texture_path, sprite_def, output_name):
    """Extract a single sprite from a texture"""
    try:
        img = Image.open(texture_path)
        x, y, w, h = sprite_def['x'], sprite_def['y'], sprite_def['w'], sprite_def['h']
        
        # Crop the sprite
        sprite = img.crop((x, y, x + w, y + h))
        
        # Save
        output_path = os.path.join(SPRITES_DIR, output_name)
        sprite.save(output_path)
        print(f"  ✓ Extracted {output_name} ({w}x{h})")
        return True
    except Exception as e:
        print(f"  ✗ Failed {output_name}: {e}")
        return False

def main():
    print("=== Fixing Sprite Extraction ===\n")
    
    # Extract card symbols
    print("Extracting card symbols from", CARD_SYMBOLS['texture'])
    texture_path = os.path.join(ASSETS_DIR, CARD_SYMBOLS['texture'])
    
    if os.path.exists(texture_path):
        for name, coords in CARD_SYMBOLS['sprites'].items():
            extract_sprite(texture_path, coords, f"{name}.png")
    else:
        print(f"  ✗ Texture not found: {texture_path}")
    
    # Extract pharaoh
    print("\nExtracting pharaoh from", PHARAOH_SYMBOLS['texture'])
    texture_path = os.path.join(ASSETS_DIR, PHARAOH_SYMBOLS['texture'])
    
    if os.path.exists(texture_path):
        for name, coords in PHARAOH_SYMBOLS['sprites'].items():
            extract_sprite(texture_path, coords, f"{name}.png")
    else:
        print(f"  ✗ Texture not found: {texture_path}")
    
    # Also let's check what the actual images look like by opening the texture
    print("\n=== Checking texture dimensions ===")
    for tex in [CARD_SYMBOLS['texture'], PHARAOH_SYMBOLS['texture']]:
        path = os.path.join(ASSETS_DIR, tex)
        if os.path.exists(path):
            img = Image.open(path)
            print(f"  {tex}: {img.size[0]}x{img.size[1]}")

if __name__ == "__main__":
    main()
