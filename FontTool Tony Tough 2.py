#!/usr/bin/env python3
"""
Tool to extract and repack .fnt files (gzip format)
Extracts font files from FontObj.fnt and FontSpeak.fnt and can repack them back

Coded by Ameer Xoshnaw
"""

import sys
import os
import gzip
from io import BytesIO


def extract_font(fnt_file, output_file=None):
    """
    Extract the font file from .fnt archive and save it
    Removes FRM/TEX header and saves only DDS image data
    """
    if not os.path.exists(fnt_file):
        print(f"Error: {fnt_file} not found!")
        return False
    
    # Determine output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(fnt_file)[0]
        output_file = f"{base_name}.dds"
    
    try:
        print(f"Extracting from {fnt_file}...")
        
        with gzip.open(fnt_file, 'rb') as gz:
            data = gz.read()
        
        # Find DDS marker position
        dds_pos = data.find(b'DDS ')
        if dds_pos == -1:
            print("Error: DDS marker not found in file!")
            return False
        
        # Save the FRM/TEX header for later repacking
        frm_tex_header = data[:dds_pos]
        print(f"Found FRM/TEX header ({len(frm_tex_header)} bytes), removing before DDS...")
        
        # Extract only DDS data (remove FRM/TEX header)
        dds_data = data[dds_pos:]
        
        with open(output_file, 'wb') as out:
            out.write(dds_data)
        
        file_size = len(dds_data)
        print(f"Successfully extracted to {output_file} ({file_size:,} bytes, DDS image only)")
        return True
        
    except Exception as e:
        print(f"Error extracting {fnt_file}: {e}")
        import traceback
        traceback.print_exc()
        return False


def repack_font(input_file, output_file=None, original_fnt_file=None):
    """
    Repack font file back into .fnt format (gzip)
    Adds back FRM/TEX header before DDS data
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return False
    
    # Determine output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        # Remove .dds, .frm, .bin extensions if present
        for ext in ['.dds', '.frm', '.bin']:
            if base_name.endswith(ext):
                base_name = base_name[:-len(ext)]
        output_file = f"{base_name}.fnt"
    
    try:
        print(f"Repacking {input_file} into {output_file}...")
        
        # Read the DDS file
        with open(input_file, 'rb') as f:
            dds_data = f.read()
        
        # Verify it starts with DDS
        if not dds_data.startswith(b'DDS '):
            print("Warning: Input file doesn't start with 'DDS ' marker")
        
        # Get FRM/TEX header from original file if provided, otherwise use default
        if original_fnt_file and os.path.exists(original_fnt_file):
            try:
                with gzip.open(original_fnt_file, 'rb') as gz:
                    orig_data = gz.read()
                    dds_pos = orig_data.find(b'DDS ')
                    if dds_pos != -1:
                        frm_tex_header = orig_data[:dds_pos]
                        print(f"Using FRM/TEX header from original file ({len(frm_tex_header)} bytes)")
                    else:
                        raise ValueError("DDS marker not found in original")
            except:
                # Fallback to default header
                frm_tex_header = bytes.fromhex('46524d0200000054455880000100')
                print("Using default FRM/TEX header")
        else:
            # Default FRM/TEX header: FRM\x02\x00\x00\x00TEX\x80\x00\x01\x00
            frm_tex_header = bytes.fromhex('46524d0200000054455880000100')
            print(f"Using default FRM/TEX header ({len(frm_tex_header)} bytes)")
        
        # Combine header + DDS data
        full_data = frm_tex_header + dds_data
        
        # Create gzip archive
        with gzip.open(output_file, 'wb') as gz:
            gz.write(full_data)
        
        file_size = len(full_data)
        print(f"Successfully created {output_file} ({file_size:,} bytes compressed)")
        return True
        
    except Exception as e:
        print(f"Error repacking {input_file}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    # Display banner
    print("=" * 50)
    print("  Font Tool - Extract & Repack .fnt files")
    print("  Coded by Ameer Xoshnaw")
    print("=" * 50)
    print()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  py \"FontTool Tony Tough 2.py\" extract <font_file.fnt> [output_file]")
        print("  py \"FontTool Tony Tough 2.py\" repack <input_file> [output_file.fnt] [original_fnt_file.fnt]")
        print("\nExamples:")
        print("  py \"FontTool Tony Tough 2.py\" extract FontObj.fnt")
        print("  py \"FontTool Tony Tough 2.py\" extract FontObj.fnt FontObj.dds")
        print("  py \"FontTool Tony Tough 2.py\" repack FontObj.dds")
        print("  py \"FontTool Tony Tough 2.py\" repack FontObj.dds FontObj.fnt")
        print("  py \"FontTool Tony Tough 2.py\" repack FontObj.dds FontObj.fnt FontObj.fnt")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "extract":
        if len(sys.argv) < 3:
            print("Error: Please specify the .fnt file to extract")
            sys.exit(1)
        fnt_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        success = extract_font(fnt_file, output_file)
        sys.exit(0 if success else 1)
    
    elif command == "repack":
        if len(sys.argv) < 3:
            print("Error: Please specify the file to repack")
            sys.exit(1)
        input_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        original_fnt_file = sys.argv[4] if len(sys.argv) > 4 else None
        success = repack_font(input_file, output_file, original_fnt_file)
        sys.exit(0 if success else 1)
    
    else:
        print(f"Error: Unknown command '{command}'")
        print("Use 'extract' or 'repack'")
        sys.exit(1)


if __name__ == "__main__":
    main()

