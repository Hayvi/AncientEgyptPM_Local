
import json
import os
import base64
from urllib.parse import urlparse, unquote

HAR_FILE = "demo.mortalsoft.net.har"
OUTPUT_DIR = "rebuild/assets"

def extract_assets():
    if not os.path.exists(HAR_FILE):
        print(f"Error: {HAR_FILE} not found. Please ensure it is in the current directory.")
        return

    print(f"Loading HAR file: {HAR_FILE}...")
    try:
        with open(HAR_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading HAR JSON: {e}")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    entries = data.get('log', {}).get('entries', [])
    print(f"Found {len(entries)} entries in HAR.")

    count = 0
    for entry in entries:
        request_url = entry['request']['url']
        response = entry['response']
        content = response.get('content', {})
        mime_type = content.get('mimeType', '')
        text = content.get('text', '')
        encoding = content.get('encoding', '')

        # Filter for interesting assets
        if 'image' in mime_type or 'audio' in mime_type or 'font' in mime_type or request_url.endswith('.json'):
            if not text:
                continue

            # Parse filename from URL
            parsed_url = urlparse(request_url)
            path = unquote(parsed_url.path)
            filename = os.path.basename(path)
            if not filename:
                filename = f"asset_{count}"
            
            # Optional: Keep directory structure? For simplicity, let's flatten or use minimal folders.
            # Let's try to match the "desktop/images" structure if possible, but for rebuild, flat might be easier initially.
            # We will save everything to output_dir, preserving subfolders relative to game root if we can detect them.
            
            # Simple approach: Save by filename. If collision, append index.
            save_path = os.path.join(OUTPUT_DIR, filename)
            if os.path.exists(save_path):
                 save_path = os.path.join(OUTPUT_DIR, f"{count}_{filename}")

            try:
                if encoding == 'base64':
                    file_data = base64.b64decode(text)
                else:
                    file_data = text.encode('utf-8')

                with open(save_path, 'wb') as f_out:
                    f_out.write(file_data)
                
                print(f"Saved: {filename} ({mime_type})")
                count += 1
            except Exception as e:
                print(f"Failed to save {filename}: {e}")

    print(f"Extraction complete. Saved {count} assets to {OUTPUT_DIR}")

if __name__ == "__main__":
    extract_assets()
