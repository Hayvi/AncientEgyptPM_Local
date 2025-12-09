#!/usr/bin/env python3
"""
Extract sprite sheet information from HAR file
"""
import json
import re

HAR_FILE = "/home/supa/test22/AncientEgyptPM_Local/demo.mortalsoft.net.har"

def find_sprites():
    with open(HAR_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all texture references with their sprite lists
    # Pattern: "textureContent".*"guid":"HASH".*"spriteList"
    
    # Find all PNG file references (escaped in JSON)
    png_pattern = r'res/([a-f0-9]{32})\.png'
    pngs = set(re.findall(png_pattern, content))
    
    print("=== PNG Textures Referenced ===")
    for png in sorted(pngs):
        print(f"  {png}.png")
    
    print(f"\nTotal: {len(pngs)} textures")
    
    # The HAR has escaped JSON, so we need to handle \" and \r\n
    # Pattern for escaped JSON: \"s_something\" : \r\n{\r\n\"x\":0
    sprite_pattern = r'\\"(s_[a-zA-Z0-9_]+)\\"[^}]*\\"x\\":(\d+)[^}]*\\"y\\":(\d+)[^}]*\\"width\\":(\d+)[^}]*\\"height\\":(\d+)'
    sprites = re.findall(sprite_pattern, content)
    
    print(f"\n=== Sprites Found ({len(sprites)} total) ===")
    seen = set()
    keywords = ['bg', 'symbol', 'frame', 'logo', 'title', 'fire', 'column', 'pillar']
    for sprite in sprites:
        name = sprite[0]
        if name not in seen:
            for kw in keywords:
                if kw in name.lower():
                    print(f"  {name}: x={sprite[1]}, y={sprite[2]}, w={sprite[3]}, h={sprite[4]}")
                    seen.add(name)
                    break
            if len(seen) > 50:
                break
    
    # Also show symbol sprites
    print("\n=== Symbol Sprites ===")
    symbol_count = 0
    for sprite in sprites:
        name = sprite[0]
        if 'symbol' in name.lower() and symbol_count < 20:
            print(f"  {name}: x={sprite[1]}, y={sprite[2]}, w={sprite[3]}, h={sprite[4]}")
            symbol_count += 1
    
    # Find texture-to-sprite mappings
    print("\n=== Texture Mappings ===")
    texture_pattern = r'\\"guid\\":\\"([a-f0-9]{32})\\"}[^}]*\\"spriteList\\"[^{]*\{([^}]+)\}'
    mappings = re.findall(texture_pattern, content)
    for guid, sprite_list in mappings[:10]:
        sprite_names = re.findall(r'\\"(s_[a-zA-Z0-9_]+)\\"', sprite_list)
        if sprite_names:
            print(f"  {guid}.png contains: {', '.join(sprite_names[:5])}...")

if __name__ == "__main__":
    find_sprites()
