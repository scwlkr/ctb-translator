import zlib
import struct
import pandas as pd
import os
import sys

# --- Standard Logic ---
ACI_HEX_LIST = [
    "#000000", "#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF", "#FFFFFF", 
    "#414141", "#808080", "#FF0000", "#FFAAAA", "#BD0000", "#BD7E7E", "#810000", "#815656", 
    "#680000", "#684545", "#450000", "#452E2E", "#FF3F00", "#FFAF95", "#BD2E00", "#BD826F", 
    "#811F00", "#81594B", "#681900", "#68483D", "#451100", "#453028", "#FF7F00", "#FFD495", 
    "#BD5E00", "#BD9D6F", "#814000", "#816B4B", "#683300", "#68563D", "#452200", "#453928", 
    "#FFBF00", "#FFFFA9", "#BD8D00", "#BDbd7d", "#816000", "#818155", "#684D00", "#686844", 
    "#453300", "#45452d", "#FFFF00", "#FFFFAA", "#BDBD00", "#BDBD7E", "#818100", "#818156", 
    "#686800", "#686845", "#454500", "#45452e", "#BFFF00", "#E4FFAA", "#8DBD00", "#A9BD7E", 
    "#608100", "#738156", "#4D6800", "#5c6845", "#334500", "#3d452e", "#7FFF00", "#D4FFAA", 
    "#5EBD00", "#9DBD7E", "#408100", "#6B8156", "#336800", "#566845", "#224500", "#39452e", 
    "#3FFF00", "#BFFFaa", "#2EBD00", "#8DBD7e", "#1F8100", "#608156", "#196800", "#4d6845", 
    "#114500", "#33452e", "#00FF00", "#AAFFAA", "#00BD00", "#7EBDBD", "#008100", "#568181", 
    "#006800", "#456868", "#004500", "#2E4545", "#00FF3F", "#AAFFBF", "#00BD2E", "#7EBD8D", 
    "#00811F", "#568160", "#006819", "#45684D", "#004511", "#2E4533", "#00FF7F", "#AAFFD4", 
    "#00BD5E", "#7EBD9D", "#008140", "#56816B", "#006833", "#456856", "#004522", "#2E4539", 
    "#00FFBF", "#AAFFFF", "#00BD8D", "#7EBDBD", "#008160", "#568181", "#00684D", "#456868", 
    "#004533", "#2E4545", "#00FFFF", "#AAFFFF", "#00BDBD", "#7EBDBD", "#008181", "#568181", 
    "#006868", "#456868", "#004545", "#2E4545", "#00BFFF", "#AAD4FF", "#008DBD", "#7EA9BD", 
    "#006081", "#567381", "#004D68", "#455C68", "#003345", "#2E3D45", "#007FFF", "#AAD4FF", 
    "#005EBD", "#7E9DBD", "#004081", "#566B81", "#003368", "#455668", "#002245", "#2E3945", 
    "#003FFF", "#AABFFF", "#002EBD", "#7E8DBD", "#001F81", "#566081", "#001968", "#454D68", 
    "#001145", "#2E3345", "#0000FF", "#AAAAFF", "#0000BD", "#7E7EBD", "#000081", "#565681", 
    "#000068", "#454568", "#000045", "#2E2E45", "#3F00FF", "#BF00FF", "#2E00BD", "#8D00BD", 
    "#1F0081", "#600081", "#190068", "#4D0068", "#110045", "#330045", "#7F00FF", "#D400FF", 
    "#5E00BD", "#9D00BD", "#400081", "#6B0081", "#330068", "#560068", "#220045", "#390045", 
    "#BF00FF", "#FF00FF", "#8D00BD", "#BD00BD", "#600081", "#810081", "#4D0068", "#680068", 
    "#330045", "#450045", "#FF00FF", "#FF00FF", "#BD00BD", "#BD00BD", "#810081", "#810081", 
    "#680068", "#680068", "#450045", "#450045", "#FF00BF", "#FF00D4", "#BD008D", "#BD009D", 
    "#810060", "#81006B", "#68004D", "#680056", "#450033", "#450039", "#FF007F", "#FF00AA", 
    "#BD005E", "#BD007E", "#810040", "#810056", "#680033", "#680045", "#450022", "#45002E", 
    "#FF003F", "#FF007F", "#BD002E", "#BD005E", "#81001F", "#810040", "#680019", "#680033", 
    "#450011", "#450022", "#333333", "#505050", "#545454", "#595959", "#5E5E5E", "#636363", 
    "#686868", "#6D6D6D", "#727272", "#777777", "#7C7C7C", "#818181"
]

LINETYPES = {
    0: "Solid", 1: "Dashed", 2: "Dotted", 3: "Dash Dot", 4: "Short Dash",
    5: "Medium Dash", 6: "Long Dash", 7: "Short Dash X2", 8: "Medium Dash X2",
    9: "Long Dash X2", 10: "Medium Long Dash", 11: "Medium Dash Short Dash Short Dash",
    12: "Long Dash Short Dash", 13: "Long Dash Dot Dot", 14: "Long Dash Dot",
    15: "Medium Dash Dot Short Dash Dot", 16: "Sparse Dot", 17: "ISO Dash",
    18: "ISO Dash Space", 19: "ISO Long Dash Dot", 20: "ISO Long Dash Double Dot",
    21: "ISO Long Dash Triple Dot", 22: "ISO Dot", 23: "ISO Long Dash Short Dash",
    24: "ISO Long Dash Double Short Dash", 25: "ISO Dash Dot", 26: "ISO Double Dash Dot",
    27: "ISO Dash Double Dot", 28: "ISO Double Dash Double Dot", 29: "ISO Dash Triple Dot",
    30: "ISO Double Dash Triple Dot", 31: "Use object linetype"
}

END_STYLES = { 0: "Butt", 1: "Square", 2: "Round", 3: "Diamond", 4: "Use object end style" }
JOIN_STYLES = { 0: "Miter", 1: "Bevel", 2: "Round", 3: "Diamond", 5: "Use object join style" }
FILL_STYLES = { 64: "Solid", 65: "Checker", 66: "Cross", 67: "Diamond", 68: "Horizontal", 69: "Vertical", 70: "Slant Left", 71: "Slant Right", 72: "Square Dots", 73: "Use object fill style" }

def parse_ctb(filepath):
    print(f"Reading file: {filepath}...")
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"Error opening file: {e}")
        return []

    start_offset = -1
    for i in range(len(data) - 1):
        if data[i] == 0x78 and data[i+1] in [0xDA, 0x9C, 0x01, 0x5E]:
            start_offset = i
            break
            
    if start_offset == -1:
        print("Error: Not a valid CTB file (Zlib signature not found).")
        return []

    try:
        decompressed_bytes = zlib.decompress(data[start_offset:])
        decompressed_text = decompressed_bytes.decode('utf-8', errors='ignore')
        lines = decompressed_text.splitlines()
    except Exception as e:
        print(f"Error during decompression: {e}")
        return []

    # 1. Parse custom_lineweight_table
    lineweight_map = {}
    in_table = False
    for line in lines:
        line = line.strip()
        if 'custom_lineweight_table{' in line:
            in_table = True
            continue
        if in_table and line == '}':
            in_table = False
            continue
        if in_table:
            if '=' in line:
                idx, val = line.split('=')
                try:
                    lineweight_map[int(idx.strip())] = float(val.strip())
                except:
                    pass
    
    print(f"Found {len(lineweight_map)} custom lineweights defined in file.")

    # 2. Parse styles
    rows = []
    current_color_data = {}
    current_color_index = -1
    in_definition = False
    
    for line in lines:
        line = line.strip()
        
        if line.endswith('{') and not line.startswith('aci_table') and not line.startswith('custom_lineweight_table'):
            try:
                idx_str = line[:-1].strip()
                if idx_str.isdigit():
                    current_color_index = int(idx_str)
                    in_definition = True
                    # Initialize default values
                    current_color_data = {
                        "Color Index": current_color_index + 1,
                        "Color": f"Color {current_color_index + 1}",
                        "Description": "",
                        "Dither": "On",
                        "Grayscale": "Off",
                        "Pen No": "Automatic",
                        "Virtual Pen": "Automatic",
                        "Screen": 100,
                        "Linetype": "Use object linetype",
                        "Adaptive": "On",
                        "Line Weight": "Use object lineweight",
                        "Line End Style": "Use object end style",
                        "Line Join Style": "Use object join style",
                        "Fill Style": "Use object fill style",
                        "Hex": "#000000",
                        "Raw Color Value": None # Capture internal value for Logic
                    }
                    
                    target_aci_index = current_color_index + 1
                    if 0 <= target_aci_index < len(ACI_HEX_LIST):
                        current_color_data["Hex"] = ACI_HEX_LIST[target_aci_index]
                    else:
                        current_color_data["Hex"] = "#000000"
                    continue
            except ValueError:
                pass

        if in_definition and line == '}':
            if current_color_index != -1:
                rows.append(current_color_data)
            in_definition = False
            current_color_index = -1
            continue

        if in_definition:
            if '=' in line:
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip().replace('"', '')

                if key == 'description': current_color_data['Description'] = val
                elif key == 'color': current_color_data['Raw Color Value'] = val # Capture Raw Color
                elif key == 'color_policy':
                    try:
                        policy = int(val)
                        current_color_data['Dither'] = "On" if (policy & 1) else "Off"
                        current_color_data['Grayscale'] = "On" if (policy & 2) else "Off"
                    except: pass
                elif key == 'physical_pen_number': current_color_data['Pen No'] = val if val != '0' else "Automatic"
                elif key == 'virtual_pen_number': current_color_data['Virtual Pen'] = val if val != '0' else "Automatic"
                elif key == 'screen': 
                    try:
                        current_color_data['Screen'] = int(val)
                    except:
                        current_color_data['Screen'] = val
                elif key == 'linetype':
                    try: current_color_data['Linetype'] = LINETYPES.get(int(val), val)
                    except: current_color_data['Linetype'] = val
                elif key == 'adaptive_linetype': current_color_data['Adaptive'] = "On" if val.upper() == 'TRUE' else "Off"
                elif key == 'lineweight':
                    try:
                        lw_idx = int(val)
                        if lw_idx == 0: current_color_data['Line Weight'] = "Specify"
                        elif lw_idx == -1: current_color_data['Line Weight'] = "Use object lineweight"
                        elif lw_idx == -2: current_color_data['Line Weight'] = "ByBlock"
                        elif lw_idx == -3: current_color_data['Line Weight'] = "Default"
                        else:
                             table_idx = lw_idx - 1
                             if table_idx in lineweight_map:
                                 mm_val = lineweight_map[table_idx]
                                 current_color_data['Line Weight'] = f"{mm_val:.2f} mm"
                             else:
                                 current_color_data['Line Weight'] = f"Idx {lw_idx}"
                    except: current_color_data['Line Weight'] = val
                elif key == 'end_style':
                    try: current_color_data['Line End Style'] = END_STYLES.get(int(val), val)
                    except: current_color_data['Line End Style'] = val
                elif key == 'join_style':
                    try: current_color_data['Line Join Style'] = JOIN_STYLES.get(int(val), val)
                    except: current_color_data['Line Join Style'] = val
                elif key == 'fill_style':
                    try: current_color_data['Fill Style'] = FILL_STYLES.get(int(val), val)
                    except: current_color_data['Fill Style'] = val

    rows.sort(key=lambda x: x['Color Index'])
    return rows

def process_data_for_output(rows):
    # 1. Enhance Data
    for row in rows:
        # Screen Color is just the Hex
        row["Screen Color"] = row["Hex"]
        
        # Plot Color Logic
        # -1023410176 appears to be "Black" (Color 7 usually, or explicitly set to Black)
        # -1006632961 appears to be "Use Object Color"
        raw_color = row.get("Raw Color Value")
        if raw_color == "-1023410176":
            row["Plot Color"] = "Black"
        elif raw_color == "-1006632961":
            row["Plot Color"] = "Color" # As requested
        else:
            row["Plot Color"] = "Color" # Default fallback
            
        # Plot Line (Just copy Line Weight for now as requested)
        row["Plot Line"] = row["Line Weight"]
        
    # 2. Convert to DataFrame
    df = pd.DataFrame(rows)
    
    # 3. Calculate "Plots Same As"
    # Group by Plot Color, Screen, Line Weight
    # We need to act on the dataframe to find these groups
    
    # Create a grouping key
    df['group_key'] = list(zip(df['Plot Color'], df['Screen'], df['Line Weight']))
    
    # Map group_key to list of Colors
    group_map = {}
    for idx, row in df.iterrows():
        key = row['group_key']
        if key not in group_map:
            group_map[key] = []
        group_map[key].append(row['Color'])
        
    # Assign "Plots Same As"
    plots_same_as_list = []
    for idx, row in df.iterrows():
        key = row['group_key']
        all_in_group = group_map.get(key, [])
        # Exclude self
        others = [c for c in all_in_group if c != row['Color']]
        if others:
            # Check length. formatting "Color 1, 2, 3"
            # The example showed "Color 60, 211, 174".
            # If we just join them, we get "Color 60, Color 211, Color 174" which is verbose.
            # Let's try to condense to "Color 60, 211, 174"
            
            # Extract numbers
            nums = []
            for c in others:
                try:
                    nums.append(str(c.split(' ')[1]))
                except:
                    nums.append(c)
            
            plots_same_as_list.append("Color " + ", ".join(nums))
        else:
            plots_same_as_list.append("")
            
    df["Plots Same As"] = plots_same_as_list
    
    # Select Final Columns
    final_columns = [
        "Color", "Screen Color", "Plot Line", "Plot Color", "Screen", "Line Weight", "Plots Same As"
    ]
    
    # Ensure all exist
    for col in final_columns:
        if col not in df.columns:
            df[col] = ""
            
    return df[final_columns]

def main():
    print("="*40)
    print("      AutoCAD CTB to Excel Converter      ")
    print("="*40)
    print("")
    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        print(f"Using file path from arguments: {input_path}")
    else:
        input_path = input("Please enter the full path to your .ctb file: ").strip()
    
    # Remove quotes if user pasted path with quotes
    if input_path.startswith('"') and input_path.endswith('"'):
        input_path = input_path[1:-1]
    
    if not os.path.exists(input_path):
        print(f"\nERROR: File not found at:\n{input_path}")
        if len(sys.argv) == 1:
            input("\nPress Enter to exit...")
        return

    if not input_path.lower().endswith('.ctb'):
        print("\nWARNING: File does not have .ctb extension. Proceeding anyway...")

    data = parse_ctb(input_path)
    
    if not data:
        print("\nFailed to extract data.")
        if len(sys.argv) == 1:
            input("\nPress Enter to exit...")
        return

    print(f"Successfully extracted {len(data)} styles.")

    # Process Data
    df_final = process_data_for_output(data)

    # Output filename
    base, ext = os.path.splitext(input_path)
    output_path = base + ".xlsx"

    print(f"\nSaving to:\n{output_path}")
    
    try:
        # Use XlsxWriter engine for formatting
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df_final.to_excel(writer, index=False, sheet_name='CTB Data')
            workbook = writer.book
            worksheet = writer.sheets['CTB Data']
            
            # Formats
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'center',
                'border': 1
            })
            
            # Apply header format
            for col_num, value in enumerate(df_final.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
            # Iterate over rows to apply conditional formatting (Screen Color)
            # Row 0 is header, data starts at Row 1
            for row_num, row_data in df_final.iterrows():
                # Get the Hex Color
                hex_color = row_data['Screen Color']
                
                # Create a format for this cell
                cell_format = workbook.add_format({
                    'bg_color': hex_color,
                    'font_color': hex_color, # Make text invisible or same as bg?
                    'border': 1
                })
                
                # Write the Screen Color cell (Column 1)
                worksheet.write(row_num + 1, 1, hex_color, cell_format)
                
            # Auto-adjust column widths (approximation)
            worksheet.set_column(0, 0, 10) # Color
            worksheet.set_column(1, 1, 15) # Screen Color
            worksheet.set_column(2, 2, 15) # Plot Line
            worksheet.set_column(3, 3, 10) # Plot Color
            worksheet.set_column(4, 4, 8)  # Screen
            worksheet.set_column(5, 5, 12) # Line Weight
            worksheet.set_column(6, 6, 50) # Plots Same As
            
        print("\nSUCCESS! Excel file created.")
    except Exception as e:
        print(f"\nERROR saving Excel file: {e}")
        print("Check if the Excel file is currently open and close it.")
    
    if len(sys.argv) == 1:
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
