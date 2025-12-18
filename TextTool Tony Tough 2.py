#!/usr/bin/env python3
"""
Tool to extract and repack translation.dat files (gzip/tar.gz format)
Extracts 'translation' file to 'translation.txt' and can repack it back

Coded by Ameer Xoshnaw
"""

import sys
import os
import gzip
import tarfile
from io import BytesIO
from pathlib import Path


def extract_translation(dat_file="translation.dat", output_file="translation.txt"):
    """
    Extract the 'translation' file from translation.dat and save as translation.txt
    Supports both gzip and tar.gz formats
    """
    if not os.path.exists(dat_file):
        print(f"Error: {dat_file} not found!")
        return False
    
    try:
        print(f"Extracting from {dat_file}...")
        
        # Check file signature to determine format
        with open(dat_file, 'rb') as f:
            magic = f.read(2)
            f.seek(0)
            
            # Try tar.gz first (most common for archives with filenames)
            if magic == b'\x1f\x8b':  # gzip signature
                try:
                    with tarfile.open(dat_file, 'r:gz') as tar:
                        files = tar.getnames()
                        print(f"Files in archive: {files}")
                        
                        # Look for 'translation' file (case-insensitive)
                        translation_file = None
                        for f in files:
                            if f.lower() == 'translation' or os.path.basename(f).lower() == 'translation':
                                translation_file = f
                                break
                        
                        if not translation_file:
                            print(f"Error: 'translation' file not found in archive!")
                            print(f"Available files: {files}")
                            return False
                        
                        print(f"Found translation file: {translation_file}")
                        
                        # Extract the file
                        member = tar.getmember(translation_file)
                        with tar.extractfile(member) as f:
                            with open(output_file, 'wb') as out:
                                out.write(f.read())
                        
                        print(f"Successfully extracted to {output_file}")
                        return True
                except tarfile.TarError:
                    # Not a tar.gz, try plain gzip
                    print("Not a tar.gz, trying plain gzip...")
                    with gzip.open(dat_file, 'rb') as gz:
                        with open(output_file, 'wb') as out:
                            out.write(gz.read())
                        print(f"Successfully extracted to {output_file}")
                        return True
            else:
                print(f"Error: Unknown file format (magic: {magic.hex()})")
                return False
                
    except Exception as e:
        print(f"Error extracting {dat_file}: {e}")
        import traceback
        traceback.print_exc()
        return False


def repack_translation(txt_file="translation.txt", output_file="translation.dat"):
    """
    Repack translation.txt back into translation.dat format (tar.gz)
    """
    if not os.path.exists(txt_file):
        print(f"Error: {txt_file} not found!")
        return False
    
    try:
        print(f"Repacking {txt_file} into {output_file}...")
        
        # Read the translation file
        with open(txt_file, 'rb') as f:
            translation_data = f.read()
        
        # Create tar.gz archive with the file named 'translation' (no extension)
        with tarfile.open(output_file, 'w:gz') as tar:
            # Create a TarInfo object for the file
            info = tarfile.TarInfo(name='translation')
            info.size = len(translation_data)
            info.mtime = os.path.getmtime(txt_file)
            
            # Add the file to the archive using BytesIO
            tar.addfile(info, fileobj=BytesIO(translation_data))
        
        print(f"Successfully created {output_file}")
        return True
        
    except Exception as e:
        print(f"Error repacking {txt_file}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    # Display banner
    print("=" * 50)
    print("  Translation Tool - Extract & Repack")
    print("  Coded by Ameer Xoshnaw")
    print("=" * 50)
    print()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  py \"TextTool Tony Tough 2.py\" extract [translation.dat] [translation.txt]")
        print("  py \"TextTool Tony Tough 2.py\" repack [translation.txt] [translation.dat]")
        print("\nExamples:")
        print("  py \"TextTool Tony Tough 2.py\" extract")
        print("  py \"TextTool Tony Tough 2.py\" extract translation.dat translation.txt")
        print("  py \"TextTool Tony Tough 2.py\" repack")
        print("  py \"TextTool Tony Tough 2.py\" repack translation.txt translation.dat")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "extract":
        dat_file = sys.argv[2] if len(sys.argv) > 2 else "translation.dat"
        txt_file = sys.argv[3] if len(sys.argv) > 3 else "translation.txt"
        success = extract_translation(dat_file, txt_file)
        sys.exit(0 if success else 1)
    
    elif command == "repack":
        txt_file = sys.argv[2] if len(sys.argv) > 2 else "translation.txt"
        dat_file = sys.argv[3] if len(sys.argv) > 3 else "translation.dat"
        success = repack_translation(txt_file, dat_file)
        sys.exit(0 if success else 1)
    
    else:
        print(f"Error: Unknown command '{command}'")
        print("Use 'extract' or 'repack'")
        sys.exit(1)


if __name__ == "__main__":
    main()

