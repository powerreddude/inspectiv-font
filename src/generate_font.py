#!/usr/bin/env fontforge 
import fontforge
import psMat
import os
import sys 
import getopt 

def create_normalized_icon_font(glyph_dir, output_dir, font_name):
    font = fontforge.font()
    font.familyname = font_name
    font.fontname = font_name.replace(' ', '') + "-Regular"
    font.fullname = font_name + " Regular"
    
    TARGET_SIZE = 2000 
    font.ascent = 1600  # Adjusting to fit larger icons
    font.descent = 400
    
    readme_lines = ["# Glyph Mapping", "| Glyph Name | Unicode | Character |", "| --- | --- | --- |"]
    unicode_val = 0xE000
    
    files = sorted([f for f in os.listdir(glyph_dir) if f.lower().endswith('.svg')])

    for filename in files:
        glyph_name = os.path.splitext(filename)[0]
        glyph = font.createChar(unicode_val, glyph_name)
        glyph.importOutlines(os.path.join(glyph_dir, filename))
        
        # Calculate bounding box width and hight
        bbox = glyph.boundingBox()
        g_width = bbox[2] - bbox[0]
        g_height = bbox[3] - bbox[1]
        
        # Normalize Scale
        if g_width > 0 and g_height > 0:
            max_dim = max(g_width, g_height)
            scale_factor = float(TARGET_SIZE) / max_dim
            glyph.transform(psMat.scale(scale_factor))
            
            # Re-calculate bounding box after scaling
            bbox = glyph.boundingBox()
            current_w = bbox[2] - bbox[0]
            
            # Centering
            target_lsb = (TARGET_SIZE - current_w) / 2
            
            # Shift the glyph to the correct horizontal position
            shift_x = target_lsb - bbox[0]
            glyph.transform(psMat.translate(shift_x, 0))
            
            # Set the final advance width
            glyph.width = TARGET_SIZE
        
        readme_lines.append(f"| {glyph_name} | U+{unicode_val:04X} | {chr(unicode_val)} |")
        unicode_val += 1   

    for ext in ['otf', 'ttf', 'woff']:
        font.generate(f"{output_dir}/{font_name.replace(' ', '')}.{ext}")
    
    with open(f"{output_dir}/README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(readme_lines))

def print_help():
    help_text = """
Usage: ./script_name.py [OPTIONS]

A utility to create normalized icon fonts from SVG glyphs.

Options:
  -i, --input <path>     Path to the input directory (glyphs source)
  -o, --output <path>    Path to the output directory (build destination)
  -n, --name <string>    The name for the generated icon font
  -h, --help             Display this help message and exit

Example:
  ./script_name.py -i ./src/glyphs -o ./build -n MyFont
"""
    print(help_text)

if __name__ == '__main__':
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "i:o:n:h", ["input=", "output=", "name=", "help"]) 
    except getopt.GetoptError as err: 
        print(f"Error: {err}") 
        sys.exit(1) 

    input_dir = ''
    output_dir = ''
    font_name = ''

    for opt, arg in opts: 
        if opt in ("-i", "--input"): 
            input_dir = arg 
            if not os.path.exists(input_dir):
                print(f"Path '{input_dir}' does not exist.")
                sys.exit(2)
        elif opt in ("-o", "--output"): 
            output_dir = arg 
            if not os.path.exists(output_dir):
                print(f"Path '{output_dir}' does not exist.")
                sys.exit(3)
        elif opt in ("-n", "--name"): 
            font_name = arg 
            if '\0' in font_name or '/' in font_name or '\\' in font_name:
                print(f"Name '{font_name}' is not a valid file name.")
                sys.exit(4)
        elif opt in ("-h", "--help"): 
            print_help()
            sys.exit(0)

    create_normalized_icon_font(input_dir, output_dir, font_name)


