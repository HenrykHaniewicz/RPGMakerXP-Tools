# RPGMakerXP-Tools

A collection of Python utilities for **extracting, inspecting, editing, and rebuilding** `Scripts.rxdata` files used by **RPG Maker XP**.

These tools allow you to work with your game’s scripts directly from Python — view them, search through them, and even rebuild a new `rxdata` file from edited files.

---

## Features

- **Extract all scripts** from an `.rxdata` file to individual `.rb` source files.  
- **Display a single script’s contents** directly in your terminal.  
- **Search for functions** across all scripts by name.  
- **Export a specific script** to a standalone Ruby file.  
- **Recompile** modified `.rb` scripts back into a valid `.rxdata` file.  
- Works fully offline — no need for RPG Maker itself.

---

## Repository layout

```
RPGMakerXP-Tools/
├─ data/
│  └─ [your rxdata files here]          # Example or working script archive
├─ extract_all_scripts.py               # Dump every script into separate .rb files
├─ display_script.py                    # Print a single script’s source
├─ function_search.py                   # Locate which scripts define a given function
├─ save_script.py                       # Export one named script to ./saved/
├─ compile_rxdata.py                    # Rebuild Scripts.rxdata from .rb sources
├─ utils.py                             # Shared helpers for loading/decompressing data
└─ README.md
```

`format_gen4_2_gen3.py` is unrelated to RPG Maker XP script utilities and is intentionally not described here.

---

## Requirements

- **Python 3.9+**
- **rubymarshal** (`pip install rubymarshal`)

Optional:
- `zlib` (part of Python standard library)

---

## Quick start

1. Place your RPG Maker project’s `Scripts.rxdata` (or whatever you have called it) file in the `data/` directory.
2. Use one of the CLI tools as shown below.

---

### View a specific script

```bash
python display_script.py data/[your_scripts].rxdata "Main"
```

Prints the decompressed Ruby code of the script named `Main`.

---

### Search for a function

```bash
python function_search.py data/[your_scripts].rxdata "update_graphics"
```

Lists all script names that contain a function called `update_graphics`.

---

### Export a single script

```bash
python save_script.py data/[your_scripts].rxdata "Scene_Title"
```

Writes the script to `./saved/Scene_Title.rb`, creating the folder if necessary.

---

### Extract all scripts

```bash
python extract_all_scripts.py data/[your_scripts].rxdata output_folder/
```

Extracts every script into separate `.rb` files, named according to their script titles.

---

### Rebuild Scripts.rxdata

After editing your exported `.rb` scripts, recompile them into a new `[filename].rxdata` (ususally `Scripts.rxdata`):

```bash
python compile_rxdata.py input_folder/ output/[filename].rxdata
```

Each `.rb` file in the input folder will become one entry in the rebuilt archive.

---

## For developers

All tools share a common interface defined in `utils.py`.  
You can import its functions in your own scripts:

```python
from utils import load_scripts, iter_decompressed_scripts

for name, code in iter_decompressed_scripts("data/[your_scripts].rxdata"):
    print(name)
    print(code[:200])  # print first 200 chars
```

---

## Data format notes

- `[your_scripts].rxdata` is a **Ruby Marshal–encoded** array.  
- Each entry is `[id, name, zlib_compressed_bytes]`.  
- The utilities decompress and decode the bytes to plain UTF-8 Ruby code.  
- Recompilation reverses this process.

---

## Troubleshooting

- **Unicode errors** → some scripts use non-UTF-8 encodings; they’re skipped with a warning.  
- **File not found** → ensure you pass the correct path to the `rxdata` file.  
- **No output** → check script name case sensitivity and ensure rubymarshal is installed.