import os
import re
import sys
from utils import load_scripts, iter_decompressed_scripts

def search_function(scripts, function_name):
    """Search for a function definition across all scripts and return names of scripts that define it.

    Args:
        scripts (list): List of compressed script entries.
        function_name (str): Name of the function to search for.

    Returns:
        list: Script names that contain a definition for the specified function.
    """
    pattern = re.compile(rf"\bdef\s+{re.escape(function_name)}\b")
    results = []

    for script_name, script_code in iter_decompressed_scripts(scripts):
        if pattern.search(script_code):
            results.append(script_name)

    return results

def list_all_functions(scripts):
    """Extract and return an alphabetically sorted list of all function names defined across all scripts.

    Args:
        scripts (list): List of compressed script entries.

    Returns:
        list: Alphabetically sorted list of unique function names.
    """
    function_pattern = re.compile(r"\bdef\s+([a-zA-Z_]\w*)")
    function_names = set()

    for _, script_code in iter_decompressed_scripts(scripts):
        function_names.update(function_pattern.findall(script_code))

    return sorted(function_names, key=str.lower)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 function_search.py path/to/Scripts.rxdata function_name")
        return

    rxdata_path = sys.argv[1]
    function_name = sys.argv[2]

    if not os.path.isfile(rxdata_path):
        print(f"File not found: {rxdata_path}")
        return

    print(f"Loading scripts from: {rxdata_path}")
    scripts = load_scripts(rxdata_path)

    print(f"Searching for function: '{function_name}'...")
    results = search_function(scripts, function_name)

    if results:
        print(f"\nFunction '{function_name}' found in:")
        for name in results:
            print(f" - {name}")
    else:
        print(f"\nFunction '{function_name}' not found in any script.")
        print("\nHere is a list of all functions found in the script database:\n")
        all_funcs = list_all_functions(scripts)
        for func in all_funcs:
            print(f" - {func}")

if __name__ == "__main__":
    main()
