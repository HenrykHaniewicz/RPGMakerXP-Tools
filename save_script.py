import os
import sys
from utils import load_scripts, iter_decompressed_scripts

def save_script_by_name(scripts, target_name, output_dir="./saved"):
    """Save a decompressed script with the given name to a .rb file in the specified output directory.

    Args:
        scripts (list): List of compressed script entries.
        target_name (str): The name of the script to search for.
        output_dir (str): Directory to save the script file. Defaults to "./saved".
    """
    for script_name, script_code in iter_decompressed_scripts(scripts):
        if script_name == target_name:
            # Ensure script_name is safe for file naming
            safe_name = "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in script_name)
            output_path = os.path.join(output_dir, f"{safe_name}.rb")
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(script_code)
                print(f"Script saved as: {output_path}")
            except IOError as e:
                print(f"Failed to save script: {e}")
            return
    print(f"Script named '{target_name}' not found.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 save_script.py <path_to_rxdata> <script_name>")
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
