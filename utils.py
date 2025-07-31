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
    """Remove invalid characters for filenames, converting non-strings to strings first."""
    name = str(name)
    return "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name)

def iter_decompressed_scripts(scripts):
    """Yield (script_name, script_code) pairs from a list of compressed RPG Maker XP scripts."""
    for entry in scripts:
        if not isinstance(entry, list) or len(entry) < 3:
            continue
        script_id, script_name, script_code = entry[0:3]

        try:
            script_code = zlib.decompress(script_code).decode('utf-8')
        except Exception as e:
            print(f"Failed to decompress script: {script_name}, because of {e}")
            continue

        yield script_name, script_code