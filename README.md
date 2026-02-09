# CTB to Excel Converter

A simple, robust tool to convert AutoCAD `.ctb` plot style files into Excel format.

## Features
- **100% Accurate**: Reads the internal lineweight tables directly from the file to ensure values match your specific configuration.
- **Complete Data**: Extracts all 255 colors and their properties (Screen, Lineweight, Linetype, etc.).
- **Hex Codes**: Includes a column for the standard Hex color code of each ACI color.
- **Easy to Use**: Interactive script prompt.

## Requirements
- Python must be installed on your machine.
- Required Python libraries: `pandas`, `openpyxl`.

To install dependencies:
```bash
pip install pandas openpyxl
```

## How to Use
1.  Run the script `CTB_Converter.py`.
2.  Paste the full path to your `.ctb` file when prompted.
    - Example: `C:\Users\Name\Desktop\JVC1.ctb`
3.  The script will generate an Excel file in the **same folder** as your input file.
    - Output: `C:\Users\Name\Desktop\JVC1.xlsx`

## Troubleshooting
- **Permission Denied**: If the script fails to save the Excel file, ensure you have the Excel file **CLOSED** before running the conversion.
- **File Not Found**: Make sure you have the correct path to your `.ctb` file (remove quotes if you copied them).
