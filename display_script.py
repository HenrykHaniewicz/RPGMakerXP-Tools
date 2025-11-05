import os
import sys
from utils import load_scripts, iter_decompressed_scripts

def print_script_by_name(scripts, target_name):
    """Print the decompressed source code of the script with the given name.

    Args:
        scripts (list): List of compressed script entries.
        target_name (str): The name of the script to search for and print.
    """
    for script_name, script_code in iter_decompressed_scripts(scripts):
        if script_name == target_name:
            print(f"=== {script_name} ===\n")
            print(script_code)
            return
    print(f"Script named '{target_name}' not found.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python display_script.py <path_to_rxdata> <script_name>")
        return

    rxdata_path = sys.argv[1]
    script_name = sys.argv[2]

    if not os.path.isfile(rxdata_path):
        print(f"File not found: {rxdata_path}")
        return

    print(f"Loading scripts from: {rxdata_path}")
    scripts = load_scripts(rxdata_path)

    print_script_by_name(scripts, script_name)

if __name__ == "__main__":
    main()
