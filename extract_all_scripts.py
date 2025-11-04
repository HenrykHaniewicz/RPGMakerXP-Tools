import os
import sys
from datetime import datetime
from utils import load_scripts, iter_decompressed_scripts, save_script_to_file

def extract_all_scripts(rxdata_path, output_root="saved"):
    """Extract all scripts from a .rxdata file and save them as .rb files in a timestamped folder.

    Args:
        rxdata_path (str): Path to the .rxdata file containing compressed RPG Maker XP scripts.
        output_root (str): Root directory to store the extracted scripts. Defaults to "saved".
    """
    scripts = load_scripts(rxdata_path)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join(output_root, timestamp)

    count = 0
    for script_name, script_code in iter_decompressed_scripts(scripts):
        if save_script_to_file(script_name, script_code, output_dir):
            count += 1

    print(f"Extracted {count} scripts to: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_all_scripts.py <path_to_rxdata>")
        sys.exit(1)

    rxdata_path = sys.argv[1]
    extract_all_scripts(rxdata_path)