
import csv

def parse_colors():
    with open('ACI_Autocad_Color_Index.csv', 'r') as f:
        reader = csv.reader(f)
        # Skip headers
        next(reader) 
        next(reader)
        
        colors = {}
        for row in reader:
            if not row or len(row) < 4:
                continue
            
            try:
                aci = int(row[3])
                r = row[0].strip().zfill(2)
                g = row[1].strip().zfill(2)
                b = row[2].strip().zfill(2)
                
                hex_val = f"#{r}{g}{b}"
                colors[aci] = hex_val
            except ValueError:
                continue
                
    # Generate list 0-255
    # If 0 is missing, usually it is ByBock/ByLayer, but user wants mapping for all.
    # The file has line 3: 0,0,0,0 -> ACI 0 is Black #000000
    
    hex_list = []
    for i in range(256):
        hex_list.append(colors.get(i, "#000000"))
        
    with open('aci_hex_list.txt', 'w') as f:
        f.write(str(hex_list))

if __name__ == "__main__":
    parse_colors()
