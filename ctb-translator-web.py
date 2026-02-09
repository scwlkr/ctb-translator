import zlib
import struct
from pyscript import document, window
import js

# --- Constants & Data ---
ACI_HEX_LIST = ['#000000', '#FF0000', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#FF00FF', '#FFFFFF', '#414141', '#808080', '#FF0000', '#FFAAAA', '#BD0000', '#BD7E7E', '#810000', '#815656', '#680000', '#684545', '#4F0000', '#4F3535', '#FF3F00', '#FFBFAA', '#BD2E00', '#BD8D7E', '#811F00', '#816056', '#681900', '#684E45', '#4F1300', '#4F3B35', '#FF7F00', '#FFD4AA', '#BD5E00', '#BD9D7E', '#814000', '#816B56', '#683400', '#685645', '#4F2700', '#4F4235', '#FFBF00', '#FFEAAA', '#BD8D00', '#BDAD7E', '#816000', '#817656', '#684E00', '#685F45', '#4F3B00', '#4F4935', '#FFFF00', '#FFFFAA', '#BDBD00', '#BDBD7E', '#818100', '#818156', '#686800', '#686845', '#4F4F00', '#4F4F35', '#BFFF00', '#EAFFAA', '#8DBD00', '#ADBD7E', '#608100', '#768156', '#4E6800', '#5F6845', '#3B4F00', '#494F35', '#7FFF00', '#D4FFAA', '#5EBD00', '#9DBD7E', '#408100', '#6B8156', '#346800', '#566845', '#274F00', '#424F35', '#3FFF00', '#BFFFAA', '#2EBD00', '#8DBD7E', '#1F8100', '#608156', '#196800', '#4E6845', '#134F00', '#3B4F35', '#00FF00', '#AAFFAA', '#00BD00', '#7EBD7E', '#008100', '#568156', '#006800', '#456845', '#004F00', '#354F35', '#00FF3F', '#AAFFBF', '#00BD2E', '#7EBD8D', '#00811F', '#568160', '#006819', '#45684E', '#004F13', '#354F3B', '#00FF7F', '#AAFFD4', '#00BD5E', '#7EBD9D', '#008140', '#56816B', '#006834', '#456856', '#004F27', '#354F42', '#00FFBF', '#AAFFEA', '#00BD8D', '#7EBDAD', '#008160', '#568176', '#00684E', '#45685F', '#004F3B', '#354F49', '#00FFFF', '#AAFFFF', '#00BDBD', '#7EBDBD', '#008181', '#568181', '#006868', '#456868', '#004F4F', '#354F4F', '#00BFFF', '#AAEAFF', '#008DBD', '#7EADBD', '#006081', '#567681', '#004E68', '#455F68', '#003B4F', '#35494F', '#007FFF', '#AAD4FF', '#005EBD', '#7E9DBD', '#004081', '#566B81', '#003468', '#455668', '#00274F', '#35424F', '#003FFF', '#AABFFF', '#002EBD', '#7E8DBD', '#001F81', '#566081', '#001968', '#454E68', '#00134F', '#353B4F', '#0000FF', '#AAAAFF', '#0000BD', '#7E7EBD', '#000081', '#565681', '#000068', '#454568', '#00004F', '#35354F', '#3F00FF', '#BFAAFF', '#2E00BD', '#8D7EBD', '#1F0081', '#605681', '#190068', '#4E4568', '#13004F', '#3B354F', '#7F00FF', '#D4AAFF', '#5E00BD', '#9D7EBD', '#400081', '#6B5681', '#340068', '#564568', '#27004F', '#42354F', '#BF00FF', '#EAAAFF', '#8D00BD', '#AD7EBD', '#600081', '#765681', '#4E0068', '#5F4568', '#3B004F', '#49354F', '#FF00FF', '#FFAAFF', '#BD00BD', '#BD7EBD', '#810081', '#815681', '#680068', '#684568', '#4F004F', '#4F354F', '#FF00BF', '#FFAAEA', '#BD008D', '#BD7EAD', '#810060', '#815676', '#68004E', '#68455F', '#4F003B', '#4F3549', '#FF007F', '#FFAAD4', '#BD005E', '#BD7E9D', '#810040', '#81566B', '#680034', '#684556', '#4F0027', '#4F3542', '#FF003F', '#FFAABF', '#BD002E', '#BD7E8D', '#81001F', '#815660', '#680019', '#68454E', '#4F0013', '#4F353B', '#333333', '#505050', '#696969', '#828282', '#BEBEBE', '#FFFFFF']

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

def parse_ctb_bytes(data):
    """Parses CTB binary data from bytes."""
    start_offset = -1
    for i in range(len(data) - 1):
        if data[i] == 0x78 and data[i+1] in [0xDA, 0x9C, 0x01, 0x5E]:
            start_offset = i
            break
            
    if start_offset == -1:
        raise ValueError("Error: Not a valid CTB file (Zlib signature not found).")

    try:
        decompressed_bytes = zlib.decompress(data[start_offset:])
        decompressed_text = decompressed_bytes.decode('utf-8', errors='ignore')
        lines = decompressed_text.splitlines()
    except Exception as e:
        raise ValueError(f"Error during decompression: {str(e)}")

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
                        "Raw Color Value": None
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
                elif key == 'color': current_color_data['Raw Color Value'] = val
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

def process_data(rows):
    """Processes extracted data into final display format (grouping, etc.)."""
    
    # 1. Enhance Data & Build processed list
    enhanced_rows = []
    for row in rows:
        processed = row.copy()
        
        # Screen Color is just the Hex
        processed["Screen Color"] = row["Hex"]
        
        # Plot Color Logic
        raw_color = row.get("Raw Color Value")
        if raw_color == "-1023410176":
            processed["Plot Color"] = "Black"
        elif raw_color == "-1006632961":
            processed["Plot Color"] = "Color"
        else:
            processed["Plot Color"] = "Color"
            
        processed["Plot Line"] = row["Line Weight"]
        enhanced_rows.append(processed)

    # 2. Calculate "Plots Same As"
    # Group by (Plot Color, Screen, Line Weight)
    group_map = {}
    
    for row in enhanced_rows:
        # Create tuple key (Plot Color, Screen, Line Weight)
        key = (row['Plot Color'], row['Screen'], row['Line Weight'])
        if key not in group_map:
            group_map[key] = []
        group_map[key].append(row['Color'])
    
    # Assign "Plots Same As"
    final_rows = []
    for row in enhanced_rows:
        final_row = row.copy()
        
        if row['Line Weight'] == "Specify":
            final_row["Plots Same As"] = ""
        else:
            key = (row['Plot Color'], row['Screen'], row['Line Weight'])
            all_in_group = group_map.get(key, [])
            others = [c for c in all_in_group if c != row['Color']]
            
            if others:
                # Format: "Color 60, 211, 174"
                nums = []
                for c in others:
                    try:
                        nums.append(str(c.split(' ')[1]))
                    except:
                        nums.append(c)
                final_row["Plots Same As"] = "Color " + ", ".join(nums)
            else:
                final_row["Plots Same As"] = ""
        
        final_rows.append(final_row)
        
    return final_rows

def render_table(data):
    """Generates HTML table rows and inserts them into the DOM."""
    table_body = document.getElementById("table-body")
    table_body.innerHTML = "" # Clear previous
    
    for row in data:
        tr = document.createElement("tr")
        
        # Color
        td_color = document.createElement("td")
        td_color.innerText = row.get("Color", "")
        tr.appendChild(td_color)
        
        # Screen Color (Visual swatch)
        td_screen_color = document.createElement("td")
        hex_val = row.get("Screen Color", "#000000")
        swatch = document.createElement("div")
        swatch.className = "color-swatch"
        swatch.style.backgroundColor = hex_val
        swatch.title = hex_val
        td_screen_color.appendChild(swatch)
        tr.appendChild(td_screen_color)
        
        # Plot Line
        td_plot_line = document.createElement("td")
        td_plot_line.innerText = str(row.get("Plot Line", ""))
        tr.appendChild(td_plot_line)
        
        # Plot Color
        td_plot_color = document.createElement("td")
        plot_color_val = str(row.get("Plot Color", ""))
        
        if plot_color_val == "Black":
            box = document.createElement("div")
            box.className = "color-swatch"
            box.style.backgroundColor = "#000000"
            box.title = "Black"
            td_plot_color.appendChild(box)
        elif plot_color_val == "Color":
            # If value is "Color", display a square box filled with the object's specific ACI Screen Color
            box = document.createElement("div")
            box.className = "color-swatch"
            box.style.backgroundColor = row.get("Screen Color", "#000000")
            box.title = row.get("Screen Color", "")
            td_plot_color.appendChild(box)
        else:
             td_plot_color.innerText = plot_color_val
             
        tr.appendChild(td_plot_color)
        
        # Screen
        td_screen = document.createElement("td")
        td_screen.innerText = str(row.get("Screen", ""))
        tr.appendChild(td_screen)
        
        # Line Weight
        td_lw = document.createElement("td")
        td_lw.innerText = str(row.get("Line Weight", ""))
        tr.appendChild(td_lw)
        
        # Plots Same As
        td_same = document.createElement("td")
        td_same.className = "plots-same-as" # for specific styling if needed
        td_same.innerText = str(row.get("Plots Same As", ""))
        tr.appendChild(td_same)
        
        table_body.appendChild(tr)

    # Show results, hide placeholder/error
    document.getElementById("results-area").classList.remove("hidden")
    document.getElementById("print-btn").classList.remove("hidden")

def process_file_content(file_content_js):
    """Entry point called from JS. Recieves JS Uint8Array."""
    try:
        # Convert JS Uint8Array to Python bytes
        file_bytes = bytes(file_content_js)
        
        rows = parse_ctb_bytes(file_bytes)
        if not rows:
             window.alert("Failed to parse CTB file.")
             return

        final_data = process_data(rows)
        render_table(final_data)
        
    except Exception as e:
        print(f"Error processing file: {e}")
        window.alert(f"Error processing file: {e}")

# Expose function to global window so JS can call it
window.process_file_content = process_file_content
print("CTB Translator Logic Loaded")
