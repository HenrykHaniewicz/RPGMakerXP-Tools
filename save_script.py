import os
import sys
from utils import load_scripts, iter_decompressed_scripts, save_script_to_file

def save_script_by_name(scripts, target_name, output_dir="./saved"):
    """Save a decompressed script with the given name to a .rb file in the specified output directory.

    Args:
        scripts (list): List of compressed script entries.
        target_name (str): The name of the script to search for.
        output_dir (str): Directory to save the script file. Defaults to "./saved".
    """
    for script_name, script_code in iter_decompressed_scripts(scripts):
        if script_name == target_name:
            output_path = save_script_to_file(script_name, script_code, output_dir)
            if output_path:
                print(f"Script saved as: {output_path}")
            return
    print(f"Script named '{target_name}' not found.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python save_script.py <path_to_rxdata> <script_name>")
        return

    rxdata_path = sys.argv[1]
    script_name = sys.argv[2]

    if not os.path.isfile(rxdata_path):
        print(f"File not found: {rxdata_path}")
        return

    print(f"Loading scripts from: {rxdata_path}")
    scripts = load_scripts(rxdata_path)

    save_script_by_name(scripts, script_name)

if __name__ == "__main__":
    main()
