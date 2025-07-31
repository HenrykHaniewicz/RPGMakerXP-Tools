import sys
import os
import shutil
import zlib
from utils import save_scripts, load_scripts

def update_script(scripts, script_name_to_update, new_code):
    found = False
    for entry in scripts:
        if not isinstance(entry, list) or len(entry) < 3:
            continue
        script_id, script_name, script_code = entry[0:3]

        if script_name == script_name_to_update:
            compressed_code = zlib.compress(new_code.encode('utf-8'))
            entry[2] = compressed_code
            found = True
            print(f"Updated script: {script_name}")
            break

    if not found:
        raise ValueError(f"Script '{script_name_to_update}' not found in the rxdata file.")
    
    return scripts

def main(rxdata_path, script_path):
    script_name = os.path.splitext(os.path.basename(script_path))[0]

    with open(script_path, 'r', encoding='utf-8') as f:
        new_code = f.read()

    # Load the original scripts
    scripts = load_scripts(rxdata_path)

    # Update the specified script
    updated_scripts = update_script(scripts, script_name, new_code)

    # Create new filename: e.g., Scripts_updated.rxdata
    base, ext = os.path.splitext(rxdata_path)
    updated_rxdata_path = f"{base}_updated{ext}"

    # Copy the original file as a backup
    shutil.copy(rxdata_path, updated_rxdata_path)

    # Write the updated script list into the copied file
    save_scripts(updated_rxdata_path, updated_scripts)

    print(f"Updated script '{script_name}' written to: {updated_rxdata_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compile_rxdata.py <rxdata_file> <script_file>")
        sys.exit(1)

    rxdata_file = sys.argv[1]
    script_file = sys.argv[2]

    main(rxdata_file, script_file)
