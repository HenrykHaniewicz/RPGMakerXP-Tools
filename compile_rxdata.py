import sys
import os
import shutil
import zlib
import glob
from utils import save_scripts, load_scripts, find_script_by_filename

def update_script(scripts, script_name_to_update, new_code_bytes):
    found = False
    for entry in scripts:
        if not isinstance(entry, list) or len(entry) < 3:
            continue
        script_id, script_name, script_code = entry[0:3]

        if script_name == script_name_to_update:
            entry[2] = zlib.compress(new_code_bytes)
            found = True
            print(f"Updated script: {script_name}")
            break

    return found

def expand_script_paths(script_paths):
    """Expand glob patterns and return a list of all matching paths."""
    expanded_paths = []
    for path in script_paths:
        if '*' in path or '?' in path:
            expanded_paths.extend(glob.glob(path))
        else:
            expanded_paths.append(path)
    return expanded_paths

def filter_valid_rb_files(paths):
    """Filter paths to only include existing .rb files."""
    rb_files = []
    for path in paths:
        if not os.path.exists(path):
            print(f"Warning: File not found: {path}")
            continue
        if not path.endswith('.rb'):
            print(f"Warning: Skipping non-.rb file: {path}")
            continue
        rb_files.append(path)
    return rb_files

def process_single_script(script_path, scripts):
    """
    Process a single script file and update it in the scripts list.
    Returns: (success: bool, status: str)
    Status can be: 'updated', 'skipped', 'not_found', 'error'
    """
    sanitized_name = os.path.splitext(os.path.basename(script_path))[0]
    print(f"Processing: {script_path}")
    
    try:
        # Read the new code
        with open(script_path, 'rb') as f:
            new_code_bytes = f.read()

        # Find the original script name that matches the sanitized filename
        original_script_name = find_script_by_filename(scripts, sanitized_name)
        
        if original_script_name is None:
            print(f"  ✗ Could not find matching script for '{sanitized_name}.rb' in rxdata file")
            return False, 'not_found'

        # Update the specified script using the original name
        found = update_script(scripts, original_script_name, new_code_bytes)
        
        if found:
            return True, 'updated'
        else:
            return False, 'skipped'
            
    except Exception as e:
        print(f"  ✗ Error processing {script_path}: {e}")
        return False, 'error'

def process_all_scripts(rb_files, scripts):
    """
    Process all script files and return statistics.
    Returns: dict with counts for each status type
    """
    stats = {
        'updated': 0,
        'skipped': 0,
        'not_found': 0,
        'error': 0
    }
    
    for script_path in rb_files:
        success, status = process_single_script(script_path, scripts)
        stats[status] += 1
    
    return stats

def save_updated_scripts(rxdata_path, scripts):
    """Save the updated scripts to a new rxdata file."""
    base, ext = os.path.splitext(rxdata_path)
    updated_rxdata_path = f"{base}_updated{ext}"
    
    # Copy the original file as a backup
    shutil.copy(rxdata_path, updated_rxdata_path)
    
    # Write the updated script list into the copied file
    save_scripts(updated_rxdata_path, scripts)
    
    return updated_rxdata_path

def print_summary(stats, output_path=None):
    """Print a summary of the processing results."""
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {stats['updated']}")
    print(f"  Unchanged: {stats['skipped']}")
    print(f"  Not found: {stats['not_found']}")
    print(f"  Errors: {stats['error']}")
    
    if output_path:
        print(f"\nUpdated rxdata file written to: {output_path}")
    else:
        print(f"\nNo changes made - output file not created")
    
    print(f"{'='*60}")

def main(rxdata_path, script_paths):
    # Expand and filter script paths
    expanded_paths = expand_script_paths(script_paths)
    rb_files = filter_valid_rb_files(expanded_paths)
    
    if not rb_files:
        print("Error: No valid .rb files to process")
        sys.exit(1)
    
    print(f"\nProcessing {len(rb_files)} script(s)...\n")

    # Load the original scripts once
    scripts = load_scripts(rxdata_path)

    # Process all scripts and collect statistics
    stats = process_all_scripts(rb_files, scripts)
    
    # Save and print results
    output_path = None
    if stats['updated'] > 0:
        output_path = save_updated_scripts(rxdata_path, scripts)
    
    print_summary(stats, output_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compile_rxdata.py <rxdata_file> <script_file> [<script_file2> ...]")
        print("\nExamples:")
        print("  python compile_rxdata.py data/Scripts.rxdata saved/Main.rb")
        print("  python compile_rxdata.py data/Scripts.rxdata saved/Main.rb saved/UI_Bag.rb")
        print("  python compile_rxdata.py data/Scripts.rxdata saved/*.rb")
        print("  python compile_rxdata.py data/Scripts.rxdata saved/*")
        sys.exit(1)

    rxdata_file = sys.argv[1]
    script_files = sys.argv[2:]

    if not os.path.exists(rxdata_file):
        print(f"Error: rxdata file not found: {rxdata_file}")
        sys.exit(1)

    main(rxdata_file, script_files)