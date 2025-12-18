# Tony Tough 2: A Rake's Progress - Text and Font Tools

Extraction and repacking tools for text and font files used in Tony Tough 2: A Rake's Progress.

## Overview

This repository contains two Python tools for modding Tony Tough 2:

- **TextTool**: Extracts and repacks translation text files
- **FontTool**: Extracts and repacks font texture files

Both tools support bidirectional conversion, allowing you to extract game files for editing and repack them back into the game's format.

## Requirements

- Python 3.6 or higher
- No external dependencies (uses Python standard library only)

## Tools

### TextTool Tony Tough 2.py

Extracts and repacks `translation.dat` files used for game text localization.

**Features:**
- Extracts translation files from compressed archives
- Supports both gzip and tar.gz formats
- Automatically detects archive format
- Repacks edited text files back into game format

**Usage:**

```bash
# Extract translation.dat to translation.txt
py "TextTool Tony Tough 2.py" extract

# Extract with custom filenames
py "TextTool Tony Tough 2.py" extract translation.dat translation.txt

# Repack translation.txt back to translation.dat
py "TextTool Tony Tough 2.py" repack

# Repack with custom filenames
py "TextTool Tony Tough 2.py" repack translation.txt translation.dat
```

### FontTool Tony Tough 2.py

Extracts and repacks `.fnt` font files containing DDS texture images.

**Features:**
- Extracts DDS images from compressed font files
- Automatically removes FRM/TEX headers during extraction
- Restores headers when repacking
- Supports FontObj.fnt and FontSpeak.fnt files

**Usage:**

```bash
# Extract FontObj.fnt to FontObj.dds
py "FontTool Tony Tough 2.py" extract FontObj.fnt

# Extract with custom output filename
py "FontTool Tony Tough 2.py" extract FontObj.fnt FontObj.dds

# Repack DDS file back to .fnt format
py "FontTool Tony Tough 2.py" repack FontObj.dds

# Repack with original file to preserve exact header
py "FontTool Tony Tough 2.py" repack FontObj.dds FontObj.fnt FontObj.fnt
```

## File Formats

### Translation Files

The `translation.dat` file is a compressed archive (gzip or tar.gz) containing a single file named `translation` (no extension). This file contains all game text strings in a structured format.

### Font Files

Font files (`.fnt`) are gzip-compressed archives containing:
- A 14-byte FRM/TEX header
- A DDS texture image (DirectDraw Surface format)

The tool automatically handles header removal during extraction and restoration during repacking.

## Workflow Example

1. Extract game files:
   ```bash
   py "TextTool Tony Tough 2.py" extract
   py "FontTool Tony Tough 2.py" extract FontObj.fnt
   ```

2. Edit the extracted files:
   - Edit `translation.txt` with your text editor
   - Edit `FontObj.dds` with an image editor that supports DDS format

3. Repack the files:
   ```bash
   py "TextTool Tony Tough 2.py" repack
   py "FontTool Tony Tough 2.py" repack FontObj.dds FontObj.fnt
   ```

4. Replace the original files in your game directory

## Technical Details

### TextTool

- Detects file format by reading magic bytes
- Handles both plain gzip and tar.gz archives
- Preserves file metadata when repacking
- Case-insensitive file matching

### FontTool

- Removes 14-byte FRM/TEX header during extraction
- Extracts pure DDS image data
- Restores header structure when repacking
- Can use original file header or default header

## Notes

- Always backup your original game files before modifying them
- The tools preserve the original file structure and compression
- Repacked files are byte-compatible with the original game format
- Font files require DDS-compatible image editors for modification

## License

Free to use and modify for personal and non-commercial purposes.

## Credits

Coded by Ameer Xoshnaw

---

For issues, questions, or contributions, please refer to the repository's issue tracker.

