import os
import re
import zlib
from rubymarshal.reader import load
from rubymarshal.writer import write

def load_scripts(rxdata_path):
    """Load and return the list of scripts from an .rxdata file."""
    with open(rxdata_path, 'rb') as f:
        scripts = load(f)
    return scripts

def save_scripts(rxdata_path, scripts):
    """Save the list of scripts to an .rxdata file."""
    with open(rxdata_path, 'wb') as f:
        write(f, scripts)

def sanitize_filename(name):
    """Remove invalid characters for filenames, converting non-strings to strings first.
    
    Decodes bytes objects and removes spaces between underscores.
    """
    # Handle bytes objects by decoding them
    if isinstance(name, bytes):
        try:
            name = name.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            name = str(name)
    else:
        name = str(name)
    
    # Replace invalid characters with underscores, but keep spaces, underscores, and hyphens
    sanitized = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name)
    
    # Remove spaces that are adjacent to underscores (e.g., "__ Name __" becomes "__Name__")
    # This handles patterns like "__ Utilities __" -> "__Utilities__"
    sanitized = re.sub(r'_\s+', '_', sanitized)  # "_ " -> "_"
    sanitized = re.sub(r'\s+_', '_', sanitized)  # " _" -> "_"
    
    return sanitized

def iter_decompressed_scripts(scripts):
    """Yield (script_name, script_code) pairs from a list of compressed RPG Maker XP scripts."""
    for entry in scripts:
        if not isinstance(entry, list) or len(entry) < 3:
            continue
        script_id, script_name, script_code = entry[0:3]
        script_name = normalize_script_name(script_name)

        try:
            script_code = zlib.decompress(script_code).decode('utf-8')
        except Exception as e:
            print(f"Failed to decompress script: {script_name}, because of {e}")
            continue

        yield script_name, script_code

def normalize_script_name(name):
    """Normalize a script name by decoding bytes and handling special cases.
    
    Args:
        name: Script name (can be str or bytes)
        
    Returns:
        str: Normalized script name
    """
    # Handle bytes objects by decoding them
    if isinstance(name, bytes):
        try:
            name = name.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            name = str(name)
    else:
        name = str(name)
    
    return name

def find_script_by_filename(scripts, filename):
    """Find the original script name that matches a sanitized filename.
    
    This handles the reverse mapping from sanitized filenames back to original script names.
    
    Args:
        scripts: List of script entries from rxdata
        filename: Sanitized filename (without .rb extension)
        
    Returns:
        Original script name if found, None otherwise
    """
    for entry in scripts:
        if not isinstance(entry, list) or len(entry) < 3:
            continue
        script_id, script_name, script_code = entry[0:3]
        
        # Normalize and sanitize the script name
        normalized_name = normalize_script_name(script_name)
        sanitized_name = sanitize_filename(normalized_name)
        
        # Check if it matches the filename
        if sanitized_name == filename:
            return script_name
    
    return None

def save_script_to_file(script_name, script_code, output_dir):
    """Save a single script to a .rb file in the specified output directory.
    
    Args:
        script_name (str): The name of the script.
        script_code (str): The decompressed script code.
        output_dir (str): Directory to save the script file.
        
    Returns:
        str: Path to the saved file if successful, None otherwise.
    """
    # Normalize the script name (decode bytes, etc.)
    script_name = normalize_script_name(script_name)
    
    safe_name = sanitize_filename(script_name)
    
    # Skip empty names or names that are only underscores/whitespace
    if not safe_name or safe_name.replace('_', '').replace('-', '').strip() == '':
        return None
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{safe_name}.rb")
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_code)
        return output_path
    except IOError as e:
        print(f"Failed to save script '{script_name}': {e}")
        return None