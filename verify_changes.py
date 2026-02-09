
import re
import csv
import random

def verify():
    # 1. Read CSV Ground Truth
    csv_colors = {}
    with open('ACI_Autocad_Color_Index.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader); next(reader)
        for row in reader:
            if not row or len(row) < 4: continue
            try:
                aci = int(row[3])
                hex_val = f"#{row[0].strip().zfill(2)}{row[1].strip().zfill(2)}{row[2].strip().zfill(2)}"
                csv_colors[aci] = hex_val
            except: pass

    # 2. Read Python File Content
    with open('ctb-translator-web.py', 'r') as f:
        content = f.read()

    # Extract ACI_HEX_LIST
    match = re.search(r'ACI_HEX_LIST\s*=\s*(\[.*?\])', content, re.DOTALL)
    if not match:
        print("FAIL: Could not find ACI_HEX_LIST in python file.")
        return

    # Safe eval
    try:
        py_list = eval(match.group(1))
    except Exception as e:
        print(f"FAIL: Could not eval list: {e}")
        return

    # 3. Verify Color 19
    print(f"Checking Color 19...")
    expected_19 = csv_colors.get(19, "#000000") # Default if missing
    actual_19 = py_list[19]
    
    if actual_19 == "#4F3535":
        print(f"PASS: Color 19 is #4F3535")
    else:
        print(f"FAIL: Color 19 is {actual_19}, expected #4F3535")

    # 4. Verify 5 Random Colors
    indices = [i for i in range(256) if i != 19]
    sample_indices = random.sample(indices, 5)
    
    print("\nChecking 5 Random Colors:")
    all_pass = True
    for idx in sample_indices:
        expected = csv_colors.get(idx, "#000000")
        actual = py_list[idx]
        if expected == actual:
            print(f"PASS: Color {idx} matches {actual}")
        else:
            print(f"FAIL: Color {idx} mismatch! Expected {expected}, got {actual}")
            all_pass = False
            
    # 5. Verify Logic Presence
    print("\nChecking Logic:")
    if 'document.createElement("div")' in content and 'className = "color-swatch"' in content:
        print("PASS: Logic for creating color swatch divs found.")
    else:
        print("FAIL: Logic for creating color swatch divs NOT found.")
        
    if 'ACI Screen Color' in content: # Comment check
        print("PASS: 'ACI Screen Color' comment found.")

if __name__ == "__main__":
    verify()
