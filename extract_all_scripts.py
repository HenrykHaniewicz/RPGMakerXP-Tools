import os
import sys
from datetime import datetime
from utils import load_scripts, sanitize_filename, iter_decompressed_scripts

def extract_all_scripts(rxdata_path, output_root="saved"):
    """Extract all scripts from a .rxdata file and save them as .rb files in a timestamped folder.

    Args:
        rxdata_path (str): Path to the .rxdata file containing compressed RPG Maker XP scripts.
        output_root (str): Root directory to store the extracted scripts. Defaults to "saved".
    """
    scripts = load_scripts(rxdata_path)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join(output_root, timestamp)
    os.makedirs(output_dir, exist_ok=True)

    count = 0
    for script_name, script_code in iter_decompressed_scripts(scripts):
        filename = sanitize_filename(script_name) + ".rb"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(script_code)

        count += 1

    print(f"Extracted {count} scripts to: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_all_scripts.py <path_to_rxdata>")
        sys.exit(1)

    rxdata_path = sys.argv[1]
    extract_all_scripts(rxdata_path)
