
import json
import os
import re

GAME_JSON = "rebuild/assets/game.json"
ASSETS_DIR = "rebuild/assets"

def find_symbol_texture():
    if not os.path.exists(GAME_JSON):
        print(f"Error: {GAME_JSON} not found.")
        return

    try:
        with open(GAME_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading game.json: {e}")
        return

    resources = data.get("resources", [])
    
    # Common Pragmatic Play symbol names
    symbol_pattern = re.compile(r"s_[HhLl][0-9]|s_[AKQJ]1?")

    found_texture_guid = None
    
    print("Scanning for Symbol Atlas...")
    
    for res in resources:
        if res.get("type") == "GameObject":
            root = res.get("data", {}).get("root", [])
            for go in root:
                for comp in go.get("components", []):
                    if comp.get("componentType") == "UIAtlas":
                        sprite_list = comp.get("serializableData", {}).get("spriteList", {})
                        
                        # Check if this atlas contains game symbols
                        matches = 0
                        for sprite_name in sprite_list.keys():
                            if symbol_pattern.match(sprite_name):
                                matches += 1
                        
                        if matches > 5:
                            print(f"Found potential Symbol Atlas! (Matches: {matches})")
                            texture_guid = comp.get("serializableData", {}).get("textureContent", {}).get("guid")
                            print(f"Atlas GUID: {texture_guid}")
                            found_texture_guid = texture_guid
                            break
        if found_texture_guid:
            break

    if not found_texture_guid:
        print("Could not identify symbol atlas automatically.")
        return

    # Now find the file matching this GUID
    print(f"Looking for file matching GUID: {found_texture_guid}")
    
    # The filename usually starts with the GUID or is the MD5 of it. 
    # In this case, looking at previous listings, the filenames look like MD5 hashes.
    # Let's try to verify if the GUID appears in any filename.
    
    for filename in os.listdir(ASSETS_DIR):
        if found_texture_guid in filename:
            print(f"\nSUCCESS: Found Symbol Sheet: {filename}")
            print(f"Path: {os.path.join(ASSETS_DIR, filename)}")
            return

    print("No matching file found for GUID. Trying permissive search...")
    # Fallback: Check for any large PNG that isn't the background
    # (Not implemented yet, relying on GUID match first)

if __name__ == "__main__":
    find_symbol_texture()
